"""Business logic layer for the Gap Analysis controller."""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from agents.gap_analysis_agent import run_gap_analysis
from app.core.database import get_db
from app.dataservice.gap_analysis_repository import GapAnalysisRepository


class GapAnalysisService:
    """Fetches real employee and project data from the DB and runs the gap-analysis agent."""

    def __init__(self, repository: GapAnalysisRepository) -> None:
        self._repository = repository

    def analyze(self, employee_id: int, project_ids: list[int]) -> dict:
        # --- Fetch employee from DB ---
        employee = self._repository.get_employee(employee_id)
        if employee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee {employee_id} not found",
            )

        # --- Fetch projects from DB ---
        if not project_ids:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="project_ids must contain at least one project ID",
            )
        projects = self._repository.get_projects(project_ids)
        if not projects:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No projects found for ids {project_ids}",
            )

        try:
            return run_gap_analysis(employee, projects)
        except RuntimeError as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


def get_gap_analysis_service(db: Session = Depends(get_db)) -> GapAnalysisService:
    """FastAPI dependency factory for `GapAnalysisService`."""
    repository = GapAnalysisRepository(db)
    return GapAnalysisService(repository)
