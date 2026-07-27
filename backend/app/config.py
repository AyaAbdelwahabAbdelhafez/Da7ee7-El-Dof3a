"""
Application configuration.
Loads environment variables and exposes typed settings for the whole backend.
"""

import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Central configuration object, populated from environment variables / .env file."""

    APP_NAME: str = "Da7ee7-El-Dof3a Backend"
    APP_VERSION: str = "1.0.0"
    ENV: str = os.getenv("ENV", "development")

    # ngrok URL of the Kaggle AI service. Updated each time a new Kaggle session starts.
    KAGGLE_AI_BASE_URL: str = os.getenv("KAGGLE_AI_BASE_URL", "https://CHANGE-ME.ngrok-free.app")
    KAGGLE_REQUEST_TIMEOUT: int = int(os.getenv("KAGGLE_REQUEST_TIMEOUT", "600"))

    # Storage paths
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    OUTPUT_DIR: Path = BASE_DIR / "outputs"

    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]

    # Upload constraints
    MAX_UPLOAD_SIZE_MB: int = 300
    ALLOWED_EXTENSIONS: set[str] = {
        ".pdf", ".ppt", ".pptx", ".doc", ".docx",
        ".mp3", ".wav", ".m4a", ".mp4", ".mov", ".mkv",
    }

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance (singleton pattern)."""
    settings = Settings()
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return settings
