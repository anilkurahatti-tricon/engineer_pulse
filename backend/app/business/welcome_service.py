"""Business logic layer for the Welcome controller."""
from app.core.config import Settings, get_settings
from app.dataservice.welcome_repository import WelcomeRepository, welcome_repository
from app.models.welcome import WelcomeInfo


class WelcomeService:
    """Combines app settings with dummy landing-page content."""

    def __init__(self, repository: WelcomeRepository, settings: Settings) -> None:
        self._repository = repository
        self._settings = settings

    def get_welcome_info(self) -> WelcomeInfo:
        return WelcomeInfo(
            app_name=self._settings.app_name,
            version=self._settings.app_version,
            tagline="Understand, support, and grow your engineering team.",
            description=(
                "Engineer Pulse brings employee feedback, skills tracking, and an "
                "AI-powered chatbot together in one place. This screen is a placeholder "
                "welcome experience - swap in real content whenever you're ready."
            ),
            features=self._repository.get_features(),
        )


def get_welcome_service() -> WelcomeService:
    """FastAPI dependency factory for `WelcomeService`."""
    return WelcomeService(welcome_repository, get_settings())
