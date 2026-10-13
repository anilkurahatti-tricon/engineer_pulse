"""Data-service layer for the Welcome controller (static dummy content).

Kept as its own module so the landing page copy can be swapped out later
(e.g. sourced from a CMS or database) without touching the controller.
"""
from app.models.welcome import FeatureHighlight

_FEATURES: list[FeatureHighlight] = [
    FeatureHighlight(
        title="Top N Match",
        description="Find the best matches for your project.",
        path="/top-n-match",
    ),
    FeatureHighlight(
        title="Skill Match",
        description="Match skills to project requirements.",
        path="/gap-analysis",
    ),
    FeatureHighlight(
        title="AI Chatbot",
        description="Ask questions and get AI-assisted answers (pluggable provider).",
        path="/chatbot",
    ),
    # FeatureHighlight(
    #     title="Demo Sandbox",
    #     description="Full CRUD playground used to validate the layered setup.",
    #     path="/demo",
    # ),
]


class WelcomeRepository:
    """Data-access operations for the welcome/landing page content."""

    def get_features(self) -> list[FeatureHighlight]:
        return list(_FEATURES)


welcome_repository = WelcomeRepository()
