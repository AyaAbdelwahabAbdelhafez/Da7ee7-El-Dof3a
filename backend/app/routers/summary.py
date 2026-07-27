"""
Summary endpoint.
Requests the Smart Summary, Important Topics and Final Revision Notes
from the Kaggle AI RAG pipeline for a given session.
"""

from fastapi import APIRouter, HTTPException

from app.models.schemas import SummaryRequest, SummaryResponse
from app.services.kaggle_client import kaggle_client
from app.utils.logger import get_logger

router = APIRouter(prefix="/api/summary", tags=["Summary"])
logger = get_logger(__name__)


@router.post("", response_model=SummaryResponse)
async def generate_summary(payload: SummaryRequest) -> SummaryResponse:
    """Generate Smart Summary / Important Topics / Revision Notes for a session."""
    try:
        result = await kaggle_client.generate_summary(payload.session_id)
    except Exception as exc:  # noqa: BLE001
        logger.error(f"Summary generation failed for session {payload.session_id}: {exc}")
        raise HTTPException(status_code=502, detail="AI service unreachable or failed.") from exc

    return SummaryResponse(
        session_id=payload.session_id,
        smart_summary=result.get("smart_summary", ""),
        important_topics=result.get("important_topics", []),
        revision_notes=result.get("revision_notes", ""),
        pdf_url=result.get("pdf_url"),
    )
