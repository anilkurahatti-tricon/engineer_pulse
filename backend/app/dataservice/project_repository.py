"""Database access layer for Project profiles."""
import logging
from sqlalchemy import select
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import Session

from app.models.db_models import EmployeeProjectModel
from app.models.project import ProjectRead

logger = logging.getLogger(__name__)


class ProjectRepository:
    """Data-access operations for projects (PostgreSQL with fallback)."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[ProjectRead]:
        try:
            models = self.db.scalars(select(EmployeeProjectModel)).all()
            if models:
                return [
                    ProjectRead(
                        id=m.id,
                        project_name=m.project_name,
                        description=m.description,
                        technologies=m.technologies,
                        required_skills=[s.strip() for s in m.technologies.split(",") if s.strip()],
                        role=m.role,
                        duration_months=m.duration_months,
                    )
                    for m in models
                ]
        except (OperationalError, ProgrammingError, Exception) as exc:
            self.db.rollback()
            logger.warning("Error fetching projects from database: %s", exc)

        # Fallback to SAMPLE_PROJECTS_BY_ID if DB is unseeded or down
        from agents.top_n_match_agent import SAMPLE_PROJECTS_BY_ID
        return [
            ProjectRead(
                id=p.project_id or pid,
                project_name=p.project_name,
                description=p.description,
                technologies=p.tech_stack_summary or ", ".join(p.required_skills),
                required_skills=p.required_skills,
                role="Core Contributor",
                duration_months=6,
            )
            for pid, p in SAMPLE_PROJECTS_BY_ID.items()
        ]

    def get_by_id(self, project_id: int) -> ProjectRead | None:
        try:
            m = self.db.get(EmployeeProjectModel, project_id)
            if m:
                return ProjectRead(
                    id=m.id,
                    project_name=m.project_name,
                    description=m.description,
                    technologies=m.technologies,
                    required_skills=[s.strip() for s in m.technologies.split(",") if s.strip()],
                    role=m.role,
                    duration_months=m.duration_months,
                )
        except (OperationalError, ProgrammingError, Exception) as exc:
            self.db.rollback()
            logger.warning("Error fetching project %s from database: %s", project_id, exc)

        from agents.top_n_match_agent import SAMPLE_PROJECTS_BY_ID
        if project_id in SAMPLE_PROJECTS_BY_ID:
            p = SAMPLE_PROJECTS_BY_ID[project_id]
            return ProjectRead(
                id=project_id,
                project_name=p.project_name,
                description=p.description,
                technologies=p.tech_stack_summary or ", ".join(p.required_skills),
                required_skills=p.required_skills,
                role="Core Contributor",
                duration_months=6,
            )
        return None
