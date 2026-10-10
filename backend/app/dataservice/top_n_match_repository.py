"""Database access layer for the Top-N Employee Match controller.

DB/table-missing errors are swallowed and logged rather than raised, so the
service layer can fall back to sample data when the database isn't reachable
yet or hasn't been seeded (see top_n_match_service.py).
"""
import logging

from sqlalchemy import select
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import Session

from agents.gap_analysis_agent import Employee, ProjectRequirement
from app.models.db_models import EmployeeModel, EmployeeProjectModel, EmployeeSkillModel

logger = logging.getLogger(__name__)


class TopNMatchRepository:
    """Builds agent-ready `ProjectRequirement` / `Employee` objects from PostgreSQL data."""

    def __init__(self, db: Session):
        self.db = db

    def get_project(self, project_id: int) -> ProjectRequirement | None:
        try:
            model = self.db.get(EmployeeProjectModel, project_id)
        except (OperationalError, ProgrammingError) as exc:
            self.db.rollback()
            logger.warning("Skipping project lookup - database/table unavailable: %s", exc)
            return None
        if not model:
            return None
        return ProjectRequirement(
            project_id=model.id,
            project_name=model.project_name,
            description=model.description,
            required_skills=[s.strip() for s in model.technologies.split(",") if s.strip()],
            tech_stack_summary=model.technologies,
        )

    def get_all_employees(self) -> list[Employee]:
        try:
            employee_models = self.db.scalars(select(EmployeeModel)).all()
        except (OperationalError, ProgrammingError) as exc:
            self.db.rollback()
            logger.warning("Skipping employee lookup - database/table unavailable: %s", exc)
            return []

        employees: list[Employee] = []
        for model in employee_models:
            skill_stmt = select(EmployeeSkillModel.skill_name).where(
                EmployeeSkillModel.employee_id == model.id
            )
            current_skills = list(self.db.scalars(skill_stmt).all())
            employees.append(
                Employee(
                    employee_id=model.id,
                    name=model.name,
                    experience_years=float(model.total_experience_years),
                    current_skills=current_skills,
                    role=model.title,
                )
            )
        return employees
