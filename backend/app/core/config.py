"""Core configuration for MapleCMS backend."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API
    api_v1_prefix: str = "/api/v1"
    project_name: str = "MapleCMS"
    version: str = "1.0.0"

    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/maplecms"

    # CORS
    backend_cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
