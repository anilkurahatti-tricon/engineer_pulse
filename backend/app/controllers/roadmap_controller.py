"""Roadmap controller: AI-generated 6-month employee upskilling roadmap."""
from fastapi import APIRouter, Depends

from app.business.roadmap_service import RoadmapService, get_roadmap_service
from app.models.roadmap import RoadmapRequest, RoadmapResponse

router = APIRouter(prefix="/api/roadmap", tags=["Roadmap"])


@router.post(
    "/generate",
    response_model=RoadmapResponse,
    summary="Generate and persist a 6-month AI upskilling roadmap from a gap-analysis result",
)
def generate_roadmap(
    payload: RoadmapRequest,
    service: RoadmapService = Depends(get_roadmap_service),
) -> dict:
    return service.generate(payload.employee_id, payload.to_gap_analysis())


@router.get(
    "/{roadmap_id}",
    response_model=RoadmapResponse,
    summary="Fetch a previously generated roadmap by id",
)
def get_roadmap(
    roadmap_id: int,
    service: RoadmapService = Depends(get_roadmap_service),
) -> dict:
    return service.get(roadmap_id)


@router.get(
    "/employee/{employee_id}",
    response_model=list[RoadmapResponse],
    summary="List all roadmaps generated for an employee, most recent first",
)
def list_roadmaps_for_employee(
    employee_id: int,
    service: RoadmapService = Depends(get_roadmap_service),
) -> list[dict]:
    return service.get_by_employee(employee_id)
