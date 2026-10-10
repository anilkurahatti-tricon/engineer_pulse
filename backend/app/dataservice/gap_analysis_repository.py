"""Database access layer for the Gap Analysis controller."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from agents.gap_analysis_agent import Employee, ProjectRequirement
from app.models.db_models import EmployeeModel, EmployeeProjectModel, EmployeeSkillModel


class GapAnalysisRepository:
    """Builds agent-ready `Employee` / `ProjectRequirement` objects from PostgreSQL data."""

    def __init__(self, db: Session):
        self.db = db

    def get_employee(self, employee_id: int) -> Employee | None:
        model = self.db.get(EmployeeModel, employee_id)
        if not model:
            return None

        skill_stmt = select(EmployeeSkillModel.skill_name).where(
            EmployeeSkillModel.employee_id == employee_id
        )
        current_skills = [row for row in self.db.scalars(skill_stmt).all()]

        return Employee(
            name=model.name,
            experience_years=float(model.total_experience_years),
            current_skills=current_skills,
            role=model.title,
            employee_id=model.id,
        )

    def get_projects(self, project_ids: list[int]) -> list[ProjectRequirement]:
        stmt = select(EmployeeProjectModel).where(EmployeeProjectModel.id.in_(project_ids))
        models = self.db.scalars(stmt).all()
        return [
            ProjectRequirement(
                project_name=m.project_name,
                description=m.description,
                required_skills=[s.strip() for s in m.technologies.split(",") if s.strip()],
                tech_stack_summary=m.technologies,
                project_id=m.id,
            )
            for m in models
        ]
