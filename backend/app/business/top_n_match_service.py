"""Business logic layer for the Top-N Employee Match controller."""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from agents.top_n_match_agent import SAMPLE_EMPLOYEES, run_top_n_match, sample_project_for_id
from app.core.database import get_db
from app.dataservice.top_n_match_repository import TopNMatchRepository


class TopNMatchService:
    """Fetches project + employee data (DB-first, sample-data fallback) and runs the match agent."""

    def __init__(self, repository: TopNMatchRepository) -> None:
        self._repository = repository

    def match(self, project_id: int, top_n: int) -> dict:
        # --- Fetch project from DB, falling back to sample data if unavailable/not found ---
        project = self._repository.get_project(project_id)
        if project is None:
            project = sample_project_for_id(project_id)

        # --- Fetch employees from DB, falling back to sample data if unavailable/empty ---
        employees = self._repository.get_all_employees()
        if not employees:
            employees = SAMPLE_EMPLOYEES

        try:
            return run_top_n_match(project, employees, top_n)
        except RuntimeError as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


def get_top_n_match_service(db: Session = Depends(get_db)) -> TopNMatchService:
    """FastAPI dependency factory for `TopNMatchService`."""
    repository = TopNMatchRepository(db)
    return TopNMatchService(repository)
