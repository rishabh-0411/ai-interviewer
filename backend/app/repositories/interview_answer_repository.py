from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.interview_answer import InterviewAnswer


class InterviewAnswerRepository:

    @staticmethod
    def create(
        db: Session,
        *,
        question_id: UUID,
        answer_text: str,
        sequence_number: int,
        answered_at,
    ) -> InterviewAnswer:
        answer = InterviewAnswer(
            question_id=question_id,
            answer_text=answer_text,
            sequence_number=sequence_number,
            answered_at=answered_at,
        )
        db.add(answer)
        db.commit()
        db.refresh(answer)
        return answer

    @staticmethod
    def get_by_id(
        db: Session,
        answer_id: UUID,
    ) -> InterviewAnswer | None:
        return db.get(InterviewAnswer, answer_id)

    @staticmethod
    def get_by_question_id(
        db: Session,
        question_id: UUID,
    ) -> list[InterviewAnswer]:
        statement = (
            select(InterviewAnswer)
            .where(InterviewAnswer.question_id == question_id)
            .order_by(InterviewAnswer.sequence_number)
        )
        return list(db.scalars(statement).all())