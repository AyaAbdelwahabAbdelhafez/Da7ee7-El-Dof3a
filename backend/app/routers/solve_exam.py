 
"""
Solve Exam endpoint.
Sends a previous exam (or a free-text question) to the Kaggle RAG pipeline
and returns model-generated answers grounded in the lecture material.
"""

from fastapi import APIRouter, HTTPException

from app.models.schemas import SolveExamRequest, SolveExamResponse, SolvedQuestion
from app.services.kaggle_client import kaggle_client
from app.utils.logger import get_logger

router = APIRouter(prefix="/api/solve-exam", tags=["Solve Exam"])
logger = get_logger(__name__)


@router.post("", response_model=SolveExamResponse)
async def solve_exam(payload: SolveExamRequest) -> SolveExamResponse:
    """Solve a previously uploaded exam file, or answer a specific question."""
    if not payload.exam_filename and not payload.question_text:
        raise HTTPException(
            status_code=400,
            detail="Provide either 'exam_filename' or 'question_text'.",
        )

    try:
        result = await kaggle_client.solve_exam(
            session_id=payload.session_id,
            exam_filename=payload.exam_filename,
            question_text=payload.question_text,
        )
    except Exception as exc:  # noqa: BLE001
        logger.error(f"Solve-exam failed for session {payload.session_id}: {exc}")
        raise HTTPException(status_code=502, detail="AI service unreachable or failed.") from exc

    solved = [
        SolvedQuestion(
            question=item.get("question", ""),
            answer=item.get("answer", ""),
            confidence=item.get("confidence"),
        )
        for item in result.get("solved_questions", [])
    ]

    return SolveExamResponse(
        session_id=payload.session_id,
        solved_questions=solved,
        pdf_url=result.get("pdf_url"),
    )

 