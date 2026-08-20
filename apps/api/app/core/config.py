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

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.api_cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
