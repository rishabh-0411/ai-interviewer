from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.interview import Interview
from app.models.interview_question import InterviewQuestion
from app.repositories.interview_question_repository import (
    InterviewQuestionRepository,
)
from app.schemas.interview import InterviewQuestionCreate


class InterviewQuestionService:

    @staticmethod
    def create_question(
        db: Session,
        interview_id: UUID,
        question_data: InterviewQuestionCreate,
    ) -> InterviewQuestion:
        interview = db.get(Interview, interview_id)

        if interview is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found.",
            )

        return InterviewQuestionRepository.create(
            db,
            interview_id,
            question_data,
        )

    @staticmethod
    def get_questions(
        db: Session,
        interview_id: UUID,
    ) -> list[InterviewQuestion]:
        interview = db.get(Interview, interview_id)

        if interview is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found.",
            )

        return InterviewQuestionRepository.get_by_interview_id(
            db,
            interview_id,
        )

    @staticmethod
    def get_question(
        db: Session,
        question_id: UUID,
    ) -> InterviewQuestion:
        question = InterviewQuestionRepository.get_by_id(
            db,
            question_id,
        )

        if question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview question not found.",
            )

        return question