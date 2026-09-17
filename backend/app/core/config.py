"""Application configuration loaded from environment variables / .env file."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application settings.

    AI provider keys are read from environment/.env and never hard-coded.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # General app settings
    app_name: str = "Engineer Pulse API"
    app_version: str = "0.1.0"
    environment: str = "development"

    # CORS
    cors_allow_origins: str = "*"

    # AI framework configuration (populated from .env, empty by default)
    ai_provider: str = "openai"  # openai | azure_openai | none
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    azure_openai_api_key: str | None = None
    azure_openai_endpoint: str | None = None
    azure_openai_deployment: str | None = None
    azure_openai_api_version: str = "2024-02-15-preview"


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance so the .env file is parsed once."""
    return Settings()
