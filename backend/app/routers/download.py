"""
Download endpoint.
Streams generated PDFs (Smart Summary, Solved Exam, Revision Notes) back
to the frontend — fetching them from Kaggle if not already cached locally.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.services.kaggle_client import kaggle_client
from app.services.file_storage import get_output_path
from app.utils.logger import get_logger

router = APIRouter(prefix="/api/download", tags=["Download"])
logger = get_logger(__name__)

VALID_TYPES = {"summary", "solved_exam", "revision_notes"}


@router.get("")
async def download_file(session_id: str, file_type: str) -> Response:
    """Download a generated PDF for the given session and file type."""
    if file_type not in VALID_TYPES:
        raise HTTPException(status_code=400, detail=f"file_type must be one of {VALID_TYPES}")

    local_path = get_output_path(session_id, f"{file_type}.pdf")

    if local_path.exists():
        pdf_bytes = local_path.read_bytes()
    else:
        try:
            pdf_bytes = await kaggle_client.fetch_generated_pdf(session_id, file_type)
            local_path.write_bytes(pdf_bytes)
        except Exception as exc:  # noqa: BLE001
            logger.error(f"Download failed for session {session_id} ({file_type}): {exc}")
            raise HTTPException(status_code=502, detail="Could not retrieve file from AI service.") from exc

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{file_type}_{session_id}.pdf"'},
    )
