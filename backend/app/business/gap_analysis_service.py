"""Business logic layer for the Gap Analysis controller."""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from agents.gap_analysis_agent import SAMPLE_EMPLOYEE, SAMPLE_PROJECTS, run_gap_analysis
from app.core.database import get_db
from app.dataservice.gap_analysis_repository import GapAnalysisRepository


class GapAnalysisService:
    """Resolves employee/project inputs (DB lookup or sample defaults) and runs the agent."""

    def __init__(self, repository: GapAnalysisRepository) -> None:
        self._repository = repository

    def analyze(self, employee_id: int | None, project_ids: list[int] | None) -> dict:
        employee = SAMPLE_EMPLOYEE
        if employee_id is not None:
            employee = self._repository.get_employee(employee_id)
            if employee is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Employee {employee_id} not found",
                )

        projects = SAMPLE_PROJECTS
        if project_ids:
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
