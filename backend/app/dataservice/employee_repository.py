"""Database access layer for Employee profiles."""
import logging
from sqlalchemy import select
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import Session

from app.models.db_models import EmployeeModel, EmployeeSkillModel
from app.models.employee import EmployeeRead

logger = logging.getLogger(__name__)


class EmployeeRepository:
    """Data-access operations for employees (PostgreSQL with fallback)."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[EmployeeRead]:
        try:
            employee_models = self.db.scalars(select(EmployeeModel)).all()
            if employee_models:
                result: list[EmployeeRead] = []
                for emp in employee_models:
                    skill_stmt = select(EmployeeSkillModel.skill_name).where(
                        EmployeeSkillModel.employee_id == emp.id
                    )
                    skills = list(self.db.scalars(skill_stmt).all())
                    result.append(
                        EmployeeRead(
                            id=emp.id,
                            name=emp.name,
                            email=emp.email,
                            title=emp.title,
                            department=emp.department,
                            total_experience_years=float(emp.total_experience_years),
                            bio=emp.bio,
                            skills=skills,
                        )
                    )
                return result
        except (OperationalError, ProgrammingError, Exception) as exc:
            self.db.rollback()
            logger.warning("Error fetching employees from database: %s", exc)

        # Fallback to SAMPLE_EMPLOYEES if DB is unseeded or down
        from agents.top_n_match_agent import SAMPLE_EMPLOYEES
        return [
            EmployeeRead(
                id=e.employee_id or idx + 1,
                name=e.name,
                email=f"{e.name.lower().replace(' ', '.')}@example.com",
                title=e.role,
                department="Engineering",
                total_experience_years=float(e.experience_years),
                bio=f"Experienced {e.role} specializing in modern software development.",
                skills=e.current_skills,
            )
            for idx, e in enumerate(SAMPLE_EMPLOYEES)
        ]

    def get_by_id(self, employee_id: int) -> EmployeeRead | None:
        try:
            emp = self.db.get(EmployeeModel, employee_id)
            if emp:
                skill_stmt = select(EmployeeSkillModel.skill_name).where(
                    EmployeeSkillModel.employee_id == emp.id
                )
                skills = list(self.db.scalars(skill_stmt).all())
                return EmployeeRead(
                    id=emp.id,
                    name=emp.name,
                    email=emp.email,
                    title=emp.title,
                    department=emp.department,
                    total_experience_years=float(emp.total_experience_years),
                    bio=emp.bio,
                    skills=skills,
                )
        except (OperationalError, ProgrammingError, Exception) as exc:
            self.db.rollback()
            logger.warning("Error fetching employee %s from database: %s", employee_id, exc)

        from agents.top_n_match_agent import SAMPLE_EMPLOYEES
        for idx, e in enumerate(SAMPLE_EMPLOYEES):
            eid = e.employee_id or idx + 1
            if eid == employee_id:
                return EmployeeRead(
                    id=eid,
                    name=e.name,
                    email=f"{e.name.lower().replace(' ', '.')}@example.com",
                    title=e.role,
                    department="Engineering",
                    total_experience_years=float(e.experience_years),
                    bio=f"Experienced {e.role}.",
                    skills=e.current_skills,
                )
        return None
