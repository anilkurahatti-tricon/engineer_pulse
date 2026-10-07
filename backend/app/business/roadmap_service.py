"""Business logic layer for the Roadmap controller."""
import json
from datetime import datetime, timezone

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from agents.roadmap_agent import run_roadmap_generation
from app.core.database import get_db
from app.dataservice.roadmap_repository import RoadmapRepository
from app.models.db_models import RoadmapModel


class RoadmapService:
    """Runs the upskilling roadmap agent against a gap-analysis payload and persists the result."""

    def __init__(self, repository: RoadmapRepository) -> None:
        self._repository = repository

    def generate(self, employee_id: int | None, gap_analysis: dict) -> dict:
        try:
            roadmap = run_roadmap_generation(gap_analysis)
        except RuntimeError as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

        model = self._repository.save(
            employee_id=employee_id,
            employee_name=roadmap.get("employee_name") or gap_analysis.get("employee_name", "Unknown"),
            role=roadmap.get("role"),
            overall_goal=roadmap.get("overall_goal"),
            gap_analysis=gap_analysis,
            roadmap=roadmap,
        )
        if model is None:
            # Database/table not available yet - still return the generated roadmap, unsaved.
            return {
                "id": None,
                "employee_id": employee_id,
                "created_at": datetime.now(timezone.utc).isoformat(),
                **roadmap,
            }
        return self._to_dict(model)

    def get(self, roadmap_id: int) -> dict:
        model = self._repository.get_by_id(roadmap_id)
        if model is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Roadmap {roadmap_id} not found")
        return self._to_dict(model)

    def get_by_employee(self, employee_id: int) -> list[dict]:
        models = self._repository.get_by_employee(employee_id)
        return [self._to_dict(m) for m in models]

    @staticmethod
    def _to_dict(model: RoadmapModel) -> dict:
        return {
            "id": model.id,
            "employee_id": model.employee_id,
            "created_at": model.created_at.isoformat(),
            **json.loads(model.roadmap_json),
        }


def get_roadmap_service(db: Session = Depends(get_db)) -> RoadmapService:
    """FastAPI dependency factory for `RoadmapService`."""
    repository = RoadmapRepository(db)
    return RoadmapService(repository)
