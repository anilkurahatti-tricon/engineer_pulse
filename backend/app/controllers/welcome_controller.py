"""Welcome controller: landing-page content for the front end.

Placeholder content today; replace `app/dataservice/welcome_repository.py`
with real content/source later without touching this controller.
"""
from fastapi import APIRouter, Depends

from app.business.welcome_service import WelcomeService, get_welcome_service
from app.models.welcome import WelcomeInfo

router = APIRouter(prefix="/api/welcome", tags=["Welcome"])


@router.get("/", response_model=WelcomeInfo, summary="Get landing page welcome content")
def get_welcome(service: WelcomeService = Depends(get_welcome_service)) -> WelcomeInfo:
    return service.get_welcome_info()
