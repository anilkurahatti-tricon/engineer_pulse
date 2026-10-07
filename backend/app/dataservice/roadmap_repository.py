"""Database access layer for the Roadmap controller."""
import json
import logging

from sqlalchemy import select
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import Session

from app.models.db_models import RoadmapModel

logger = logging.getLogger(__name__)


class RoadmapRepository:
    """Persists and retrieves AI-generated employee upskilling roadmaps.

    Database/table-missing errors are swallowed and logged rather than raised, so the
    roadmap can still be generated and returned before the "roadmaps" table/migration exists.
    """

    def __init__(self, db: Session):
        self.db = db

    def save(
        self,
        employee_id: int | None,
        employee_name: str,
        role: str | None,
        overall_goal: str | None,
        gap_analysis: dict,
        roadmap: dict,
    ) -> RoadmapModel | None:
        model = RoadmapModel(
            employee_id=employee_id,
            employee_name=employee_name,
            role=role,
            overall_goal=overall_goal,
            gap_analysis_json=json.dumps(gap_analysis),
            roadmap_json=json.dumps(roadmap),
        )
        try:
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return model
        except (OperationalError, ProgrammingError) as exc:
            self.db.rollback()
            logger.warning("Skipping roadmap persistence - database/table unavailable: %s", exc)
            return None

    def get_by_id(self, roadmap_id: int) -> RoadmapModel | None:
        try:
            return self.db.get(RoadmapModel, roadmap_id)
        except (OperationalError, ProgrammingError) as exc:
            self.db.rollback()
            logger.warning("Skipping roadmap lookup - database/table unavailable: %s", exc)
            return None

    def get_by_employee(self, employee_id: int) -> list[RoadmapModel]:
        stmt = (
            select(RoadmapModel)
            .where(RoadmapModel.employee_id == employee_id)
            .order_by(RoadmapModel.created_at.desc())
        )
        try:
            return list(self.db.scalars(stmt).all())
        except (OperationalError, ProgrammingError) as exc:
            self.db.rollback()
            logger.warning("Skipping roadmap lookup - database/table unavailable: %s", exc)
            return []

