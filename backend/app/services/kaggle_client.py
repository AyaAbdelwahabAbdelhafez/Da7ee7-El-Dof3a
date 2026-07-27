"""
Client responsible for all communication between the local FastAPI backend
and the AI service running on Kaggle GPU, exposed through an ngrok tunnel.
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional, Any

import httpx

from app.config import get_settings
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)


class KaggleAIClient:
    """Thin async HTTP client wrapping the Kaggle AI service endpoints."""

    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        self.base_url = (base_url or settings.KAGGLE_AI_BASE_URL).rstrip("/")
        self.timeout = timeout or settings.KAGGLE_REQUEST_TIMEOUT

    async def health_check(self) -> bool:
        """Ping the Kaggle AI /health endpoint to check the tunnel is alive."""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(f"{self.base_url}/health")
                return resp.status_code == 200
        except httpx.HTTPError as exc:
            logger.warning(f"Kaggle AI health check failed: {exc}")
            return False

    async def process_files(self, session_id: str, file_paths: list[Path]) -> dict[str, Any]:
        """
        Upload the session's raw files to the Kaggle AI service.
        The Kaggle service will run: text extraction, Whisper transcription,
        chunking, embeddings, FAISS indexing and RAG pipeline construction.
        """
        files = [
            ("files", (p.name, p.open("rb"), "application/octet-stream"))
            for p in file_paths
        ]
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    f"{self.base_url}/ingest",
                    data={"session_id": session_id},
                    files=files,
                )
                resp.raise_for_status()
                return resp.json()
        finally:
            for _, (_, fh, _) in files:
                fh.close()

    async def generate_summary(self, session_id: str) -> dict[str, Any]:
        """Request Smart Summary + Important Topics + Revision Notes from Kaggle."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                f"{self.base_url}/generate-summary",
                json={"session_id": session_id},
            )
            resp.raise_for_status()
            return resp.json()

    async def solve_exam(
        self, session_id: str, exam_filename: Optional[str] = None, question_text: Optional[str] = None
    ) -> dict[str, Any]:
        """Ask the Kaggle RAG pipeline to solve a previous exam / question."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                f"{self.base_url}/solve-exam",
                json={
                    "session_id": session_id,
                    "exam_filename": exam_filename,
                    "question_text": question_text,
                },
            )
            resp.raise_for_status()
            return resp.json()

    async def fetch_generated_pdf(self, session_id: str, file_type: str) -> bytes:
        """Download a generated PDF (summary / solved exam / revision notes) from Kaggle."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(
                f"{self.base_url}/download",
                params={"session_id": session_id, "file_type": file_type},
            )
            resp.raise_for_status()
            return resp.content


kaggle_client = KaggleAIClient()
