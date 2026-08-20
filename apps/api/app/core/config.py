"""Application settings loaded from the environment."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "10sPilot API"
    version: str = "0.1.0"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/tenspilot"
    api_cors_origins: str = "http://localhost:3000"
    api_secret_key: str = "change-me"

    # Free SERP data sources.
    serper_api_key: str | None = None
    gsc_access_token: str | None = None
    gsc_site_url: str | None = None

    # Free-tier LLM providers used by the content / AEO / GEO engines.
    ai_provider: str = "groq"
    groq_api_key: str | None = None
    groq_model: str = "llama-3.3-70b-versatile"
    google_api_key: str | None = None
    google_model: str = "gemini-2.0-flash"

    # Optional paid answer engines probed by the citation monitor.
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    perplexity_api_key: str | None = None
    perplexity_model: str = "sonar"

    request_timeout_seconds: float = 30.0

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.api_cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
