"""
Local file storage service.
Handles saving uploaded files into per-session folders and basic validation.
"""

import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile, HTTPException

from app.config import get_settings
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)


def create_session_id() -> str:
    """Generate a unique session id for a batch of uploads."""
    return uuid.uuid4().hex[:12]


def validate_file(file: UploadFile) -> None:
    """Validate file extension and (approximate) size constraints."""
    suffix = Path(file.filename).suffix.lower()
    if suffix not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{suffix}'. Allowed: {sorted(settings.ALLOWED_EXTENSIONS)}",
        )


def get_session_dir(session_id: str) -> Path:
    """Return (and create if missing) the upload directory for a session."""
    session_dir = settings.UPLOAD_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


async def save_upload(file: UploadFile, session_id: str) -> Path:
    """Persist a single uploaded file to disk under its session folder."""
    validate_file(file)
    session_dir = get_session_dir(session_id)
    destination = session_dir / file.filename

    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()

    logger.info(f"Saved file '{file.filename}' for session '{session_id}' -> {destination}")
    return destination


def list_session_files(session_id: str) -> list[Path]:
    """List every file stored for a given session."""
    session_dir = get_session_dir(session_id)
    return sorted(p for p in session_dir.iterdir() if p.is_file())


def get_output_path(session_id: str, filename: str) -> Path:
    """Resolve (and create) the output directory path for a session's generated files."""
    out_dir = settings.OUTPUT_DIR / session_id
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / filename
