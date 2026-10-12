"""Business logic layer for Project operations."""
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dataservice.project_repository import ProjectRepository
from app.models.project import ProjectRead


class ProjectService:
    """Provides business logic and queries for Project profiles."""

    def __init__(self, repository: ProjectRepository) -> None:
        self._repository = repository

    def list_projects(self) -> list[ProjectRead]:
        return self._repository.get_all()

    def get_project(self, project_id: int) -> ProjectRead | None:
        return self._repository.get_by_id(project_id)


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    """FastAPI dependency factory for `ProjectService`."""
    repository = ProjectRepository(db)
    return ProjectService(repository)
