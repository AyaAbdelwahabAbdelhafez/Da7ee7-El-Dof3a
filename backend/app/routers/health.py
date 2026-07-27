"""
Health check endpoint — reports backend status and whether the Kaggle AI
service (via ngrok) is currently reachable.
"""

from fastapi import APIRouter

from app.config import get_settings
from app.models.schemas import HealthResponse
from app.services.kaggle_client import kaggle_client

router = APIRouter(prefix="/api/health", tags=["Health"])
settings = get_settings()


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Return backend health plus Kaggle AI reachability."""
    kaggle_ok = await kaggle_client.health_check()
    return HealthResponse(
        status="ok",
        backend_version=settings.APP_VERSION,
        kaggle_ai_reachable=kaggle_ok,
        kaggle_url=settings.KAGGLE_AI_BASE_URL,
    )
