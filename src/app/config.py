"""Configuration management using Pydantic settings."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "Exoplanet AI Validator"
    api_prefix: str = "/api"
    debug: bool = False
    qdrant_url: str | None = None
    qdrant_host: str | None = "localhost"
    qdrant_port: int = 6333
    qdrant_api_key: str | None = None
    model_checkpoint_path: str | None = None
    rag_corpus_dir: str | None = None
    rag_collection_name: str = "exoai_corpus"
    jwt_secret_key: str = "super-secret-key"
    jwt_algorithm: str = "HS256"
    log_level: str = "INFO"
    database_url: str = "sqlite:///app.db"
    earthdata_username: str | None = None
    earthdata_password: str | None = None
    earthdata_token: str | None = None

    model_config = SettingsConfigDict(env_file=(".env",), env_file_encoding="utf-8", env_prefix="EXOAI_")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()


__all__ = ["Settings", "get_settings"]
