"""
Da7ee7-El-Dof3a — FastAPI Backend Entrypoint.

Responsibilities:
- Expose Upload / Summary / Solve-Exam / Download / Health APIs.
- Handle CORS so the static frontend can call the backend from any origin.
- Centralized logging and validation via Pydantic schemas.
- Forward heavy AI work to the Kaggle GPU service through ngrok.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time

from app.config import get_settings
from app.utils.logger import get_logger
from app.routers import upload, summary, solve_exam, download, health

settings = get_settings()
logger = get_logger("main")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered exam preparation system — backend API.",
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request logging middleware
# ---------------------------------------------------------------------------
class LoggingMiddleware(BaseHTTPMiddleware):
    """Logs every request with method, path, status code and duration."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms:.1f}ms)"
        )
        return response


app.add_middleware(LoggingMiddleware)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(health.router)
app.include_router(upload.router)
app.include_router(summary.router)
app.include_router(solve_exam.router)
app.include_router(download.router)


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    """Basic root route confirming the API is running."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.on_event("startup")
async def on_startup() -> None:
    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} starting up (env={settings.ENV})")
    logger.info(f"Kaggle AI base URL: {settings.KAGGLE_AI_BASE_URL}")


@app.on_event("shutdown")
async def on_shutdown() -> None:
    logger.info("Backend shutting down.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
