from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.interview import Interview
from app.repositories.interview_repository import InterviewRepository
from app.schemas.interview import InterviewCreate


class InterviewService:

    @staticmethod
    def create_interview(
        db: Session,
        interview_data: InterviewCreate,
    ) -> Interview:
        candidate = db.get(Candidate, interview_data.candidate_id)

        if candidate is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate not found.",
            )

        return InterviewRepository.create(db, interview_data)

    @staticmethod
    def get_interview(
        db: Session,
        interview_id: UUID,
    ) -> Interview:
        interview = InterviewRepository.get_by_id(db, interview_id)

        if interview is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found.",
            )

        return interview

    @staticmethod
    def get_interviews(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Interview]:
        return InterviewRepository.get_all(
            db,
            skip=skip,
            limit=limit,
        )