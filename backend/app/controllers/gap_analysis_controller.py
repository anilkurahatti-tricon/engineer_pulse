"""Gap Analysis controller: AI-powered employee vs. project skill-gap report."""
from fastapi import APIRouter, Depends

from app.business.gap_analysis_service import GapAnalysisService, get_gap_analysis_service
from app.models.gap_analysis import GapAnalysisRequest, GapAnalysisResponse

router = APIRouter(prefix="/api/gap-analysis", tags=["Gap Analysis"])


@router.post(
    "/analyze",
    response_model=GapAnalysisResponse,
    summary="Run an AI skill-gap analysis for an employee against a set of target projects",
)
def analyze_gap(
    payload: GapAnalysisRequest,
    service: GapAnalysisService = Depends(get_gap_analysis_service),
) -> dict:
    return service.analyze(payload.employee_id, payload.project_ids)
