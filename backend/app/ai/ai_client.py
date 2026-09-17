"""AI integration layer.

Pluggable client used by the chatbot (and future AI features). Reads provider
configuration/API keys from environment variables via `app.core.config.Settings`.
When no API key is configured the client falls back to a deterministic dummy
response so the rest of the application can be developed/tested without
real AI provider credentials.
"""
from app.core.config import Settings, get_settings


class AIClient:
    """Thin wrapper around configured AI providers (OpenAI, Azure OpenAI, ...).

    Extraction of provider settings happens here so controllers only deal with
    plain request/response objects and never touch raw environment variables.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    @property
    def provider(self) -> str:
        return self._settings.ai_provider

    def _has_real_credentials(self) -> bool:
        if self._settings.ai_provider == "openai":
            return bool(self._settings.openai_api_key)
        if self._settings.ai_provider == "azure_openai":
            return bool(self._settings.azure_openai_api_key and self._settings.azure_openai_endpoint)
        return False

    def generate_response(self, prompt: str) -> tuple[str, bool]:
        """Return (reply, is_dummy_response).

        Real provider calls (OpenAI/Azure OpenAI SDK) should be implemented in
        the branches below once API keys are supplied via `.env`.
        """
        if not self._has_real_credentials():
            return (
                f"[dummy-response] Echoing your message since no {self._settings.ai_provider} "
                f"API key is configured: '{prompt}'",
                True,
            )

        if self._settings.ai_provider == "openai":
            # TODO: call OpenAI SDK using self._settings.openai_api_key / openai_model
            return f"[openai:{self._settings.openai_model}] {prompt}", False

        if self._settings.ai_provider == "azure_openai":
            # TODO: call Azure OpenAI SDK using self._settings.azure_openai_* fields
            return f"[azure_openai:{self._settings.azure_openai_deployment}] {prompt}", False

        return "AI provider not supported.", True


def get_ai_client() -> AIClient:
    """FastAPI dependency factory for `AIClient`."""
    return AIClient(get_settings())
