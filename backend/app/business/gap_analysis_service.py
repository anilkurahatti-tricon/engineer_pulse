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

    def get_options(self) -> dict:
        return self._repository.get_options()

    def analyze(self, employee_id: int, project_ids: list[int]) -> dict:
        if not project_ids:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="project_ids must contain at least one project ID",
            )

        # --- Fetch employee from DB, fallback to sample data if unavailable ---
        employee = self._repository.get_employee(employee_id)
        if employee is None:
            from agents.top_n_match_agent import SAMPLE_EMPLOYEES
            for e in SAMPLE_EMPLOYEES:
                if e.employee_id == employee_id:
                    employee = e
                    break
        if employee is None:
            from agents.gap_analysis_agent import SAMPLE_EMPLOYEE
            employee = SAMPLE_EMPLOYEE

        # --- Fetch projects from DB, fallback to sample data if unavailable ---
        projects = self._repository.get_projects(project_ids)
        if not projects:
            from agents.top_n_match_agent import sample_project_for_id
            projects = [sample_project_for_id(pid) for pid in project_ids]

        try:
            return run_gap_analysis(employee, projects)
        except RuntimeError as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


def get_gap_analysis_service(db: Session = Depends(get_db)) -> GapAnalysisService:
    """FastAPI dependency factory for `GapAnalysisService`."""
    repository = GapAnalysisRepository(db)
    return GapAnalysisService(repository)
