from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.interview_question import InterviewQuestion
from app.schemas.interview import InterviewQuestionCreate


class InterviewQuestionRepository:

    @staticmethod
    def create(
        db: Session,
        interview_id: UUID,
        question_data: InterviewQuestionCreate,
    ) -> InterviewQuestion:
        question = InterviewQuestion(
            interview_id=interview_id,
            question_text=question_data.question_text,
            question_type=question_data.question_type,
            sequence_number=question_data.sequence_number,
        )

        db.add(question)
        db.commit()
        db.refresh(question)

        return question

    @staticmethod
    def get_by_id(
        db: Session,
        question_id: UUID,
    ) -> InterviewQuestion | None:
        statement = select(InterviewQuestion).where(
            InterviewQuestion.id == question_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_by_interview_id(
        db: Session,
        interview_id: UUID,
    ) -> list[InterviewQuestion]:
        statement = (
            select(InterviewQuestion)
            .where(InterviewQuestion.interview_id == interview_id)
            .order_by(InterviewQuestion.sequence_number)
        )

        return list(db.scalars(statement).all())