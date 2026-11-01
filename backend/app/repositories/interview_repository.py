from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.interview import Interview
from app.schemas.interview import InterviewCreate


class InterviewRepository:

    @staticmethod
    def create(
        db: Session,
        interview_data: InterviewCreate,
    ) -> Interview:
        interview = Interview(
            candidate_id=interview_data.candidate_id,
            interview_type=interview_data.interview_type,
            job_title=interview_data.job_title,
        )

        db.add(interview)
        db.commit()
        db.refresh(interview)

        return interview

    @staticmethod
    def get_by_id(
        db: Session,
        interview_id: UUID,
    ) -> Interview | None:
        statement = select(Interview).where(
            Interview.id == interview_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Interview]:
        statement = (
            select(Interview)
            .order_by(Interview.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(db.scalars(statement).all())