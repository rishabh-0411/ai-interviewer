from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.interview import (
    InterviewQuestionCreate,
    InterviewQuestionResponse,
)
from app.services.interview_question_service import (
    InterviewQuestionService,
)

router = APIRouter(
    prefix="/api/v1/interviews/{interview_id}/questions",
    tags=["Interview Questions"],
)


@router.post(
    "/",
    response_model=InterviewQuestionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_question(
    interview_id: UUID,
    question_data: InterviewQuestionCreate,
    db: Session = Depends(get_db),
):
    return InterviewQuestionService.create_question(
        db,
        interview_id,
        question_data,
    )


@router.get("/", response_model=list[InterviewQuestionResponse])
def list_questions(
    interview_id: UUID,
    db: Session = Depends(get_db),
):
    return InterviewQuestionService.get_questions(db, interview_id)


@router.get("/{question_id}", response_model=InterviewQuestionResponse)
def get_question(
    interview_id: UUID,
    question_id: UUID,
    db: Session = Depends(get_db),
):
    question = InterviewQuestionService.get_question(db, question_id)

    if question.interview_id != interview_id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview question not found.",
        )

    return question