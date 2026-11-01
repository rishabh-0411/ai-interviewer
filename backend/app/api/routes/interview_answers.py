from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.interview import (
    InterviewAnswerCreate,
    InterviewAnswerResponse,
)
from app.services.interview_answer_service import InterviewAnswerService

router = APIRouter(
    prefix="/api/v1/questions/{question_id}/answers",
    tags=["Interview Answers"],
)


@router.post(
    "/",
    response_model=InterviewAnswerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_answer(
    question_id: UUID,
    answer_data: InterviewAnswerCreate,
    db: Session = Depends(get_db),
):
    return InterviewAnswerService.create_answer(
        db,
        question_id,
        answer_data,
    )


@router.get(
    "/",
    response_model=list[InterviewAnswerResponse],
)
def get_answers(
    question_id: UUID,
    db: Session = Depends(get_db),
):
    return InterviewAnswerService.get_answers(db, question_id)


@router.get(
    "/{answer_id}",
    response_model=InterviewAnswerResponse,
)
def get_answer(
    question_id: UUID,
    answer_id: UUID,
    db: Session = Depends(get_db),
):
    answer = InterviewAnswerService.get_answer(db, answer_id)

    if answer.question_id != question_id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview answer not found.",
        )

    return answer