"""Top-N Employee Match controller: AI-ranked shortlist of employees best matching a project."""
from fastapi import APIRouter, Depends

from app.business.top_n_match_service import TopNMatchService, get_top_n_match_service
from app.models.top_n_match import TopNMatchRequest, TopNMatchResponse

router = APIRouter(prefix="/api/top-n-match", tags=["Top N Match"])


@router.post(
    "/",
    response_model=TopNMatchResponse,
    summary="Rank employees by AI-generated readiness score for a project and return the top N",
)
def match_top_n_employees(
    payload: TopNMatchRequest,
    service: TopNMatchService = Depends(get_top_n_match_service),
) -> dict:
    return service.match(payload.project_id, payload.top_n)
