from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.interview_question import InterviewQuestion
from app.models.interview_answer import InterviewAnswer
from app.repositories.interview_answer_repository import (
    InterviewAnswerRepository,
)
from app.schemas.interview import InterviewAnswerCreate


class InterviewAnswerService:

    @staticmethod
    def create_answer(
        db: Session,
        question_id: UUID,
        answer_data: InterviewAnswerCreate,
    ) -> InterviewAnswer:
        question = db.get(InterviewQuestion, question_id)

        if question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview question not found.",
            )

        return InterviewAnswerRepository.create(
            db,
            question_id=question_id,
            answer_text=answer_data.answer_text,
            sequence_number=answer_data.sequence_number,
            answered_at=datetime.now(timezone.utc),
        )

    @staticmethod
    def get_answers(
        db: Session,
        question_id: UUID,
    ) -> list[InterviewAnswer]:
        question = db.get(InterviewQuestion, question_id)

        if question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview question not found.",
            )

        return InterviewAnswerRepository.get_by_question_id(
            db,
            question_id,
        )

    @staticmethod
    def get_answer(
        db: Session,
        answer_id: UUID,
    ) -> InterviewAnswer:
        answer = InterviewAnswerRepository.get_by_id(db, answer_id)

        if answer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview answer not found.",
            )

        return answer