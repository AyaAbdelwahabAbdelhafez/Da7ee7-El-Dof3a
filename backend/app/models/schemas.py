"""
Pydantic models used for request validation and response serialization.
"""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    """Response returned right after files are stored and forwarded to Kaggle."""
    session_id: str
    files_received: list[str]
    status: str
    message: str


class ProcessingStatus(BaseModel):
    """Status of an in-flight processing job."""
    session_id: str
    stage: str
    progress: int = Field(ge=0, le=100)
    status: str


class SummaryRequest(BaseModel):
    session_id: str


class SummaryResponse(BaseModel):
    session_id: str
    smart_summary: str
    important_topics: list[str]
    revision_notes: str
    pdf_url: Optional[str] = None


class SolveExamRequest(BaseModel):
    session_id: str
    exam_filename: Optional[str] = None
    question_text: Optional[str] = None


class SolvedQuestion(BaseModel):
    question: str
    answer: str
    confidence: Optional[float] = None


class SolveExamResponse(BaseModel):
    session_id: str
    solved_questions: list[SolvedQuestion]
    pdf_url: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    backend_version: str
    kaggle_ai_reachable: bool
    kaggle_url: str


class DownloadRequest(BaseModel):
    session_id: str
    file_type: str  # "summary" | "solved_exam" | "revision_notes"
