"""
Upload endpoint.
Accepts lecture slides, PowerPoint, previous exams, audio and video files,
stores them locally, then forwards them to the Kaggle AI service for
extraction, transcription, chunking, embeddings and FAISS indexing.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.models.schemas import UploadResponse
from app.services.file_storage import create_session_id, save_upload, list_session_files
from app.services.kaggle_client import kaggle_client
from app.utils.logger import get_logger

router = APIRouter(prefix="/api/upload", tags=["Upload"])
logger = get_logger(__name__)


@router.post("", response_model=UploadResponse)
async def upload_files(files: list[UploadFile] = File(...)) -> UploadResponse:
    """
    Upload one or more files (PDF, PPTX, DOCX, audio, video).
    Returns a session_id used by every subsequent API call.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided.")

    session_id = create_session_id()
    saved_names: list[str] = []

    for file in files:
        await save_upload(file, session_id)
        saved_names.append(file.filename)

    logger.info(f"Session '{session_id}' created with files: {saved_names}")

    # Forward files to the Kaggle AI service (ingestion + RAG index build).
    try:
        file_paths = list_session_files(session_id)
        await kaggle_client.process_files(session_id, file_paths)
        status = "processing_started"
        message = "Files uploaded and sent to the AI service for processing."
    except Exception as exc:  # noqa: BLE001 - surfaced to the client below
        logger.error(f"Failed to reach Kaggle AI service: {exc}")
        status = "stored_locally_only"
        message = (
            "Files were stored locally, but the AI service (Kaggle/ngrok) "
            "could not be reached. Please verify the ngrok URL and try again."
        )

    return UploadResponse(
        session_id=session_id,
        files_received=saved_names,
        status=status,
        message=message,
    )
