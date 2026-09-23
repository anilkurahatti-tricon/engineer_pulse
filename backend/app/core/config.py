"""Application configuration loaded from environment variables / .env file."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application settings.

    AI provider keys are read from environment/.env and never hard-coded.
    Database connection: set DATABASE_URL directly (centralized/cloud DB)
    or set individual POSTGRES_* variables for the local Docker container.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # General app settings
    app_name: str = "Engineer Pulse API"
    app_version: str = "0.1.0"
    environment: str = "development"

    # CORS
    cors_allow_origins: str = "*"

    # -------------------------------------------------------------------------
    # PostgreSQL connection
    # Option 1 (centralized/cloud): set DATABASE_URL directly in .env
    #   DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname?sslmode=require
    # Option 2 (local Docker): set individual POSTGRES_* vars; DATABASE_URL is
    #   auto-constructed from them if DATABASE_URL is not provided.
    # -------------------------------------------------------------------------
    database_url: str | None = None           # override everything if set
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "engineer_pulse"
    embedding_dimension: int = 1536

    @property
    def effective_database_url(self) -> str:
        """Return the DATABASE_URL to use — explicit env var wins, then build from parts."""
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

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
