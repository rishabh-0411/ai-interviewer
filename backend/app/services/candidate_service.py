
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.repositories.candidate_repository import CandidateRepository
from app.schemas.candidate import CandidateCreate


class CandidateService:

    @staticmethod
    def create_candidate(
        db: Session,
        candidate_data: CandidateCreate,
    ) -> Candidate:
        existing_candidate = CandidateRepository.get_by_email(
            db,
            str(candidate_data.email),
        )

        if existing_candidate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A candidate with this email already exists.",
            )

        try:
            return CandidateRepository.create(db, candidate_data)
        except IntegrityError as exc:
            db.rollback()

            # Handles a duplicate email submitted concurrently.
            if CandidateRepository.get_by_email(
                db,
                str(candidate_data.email),
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A candidate with this email already exists.",
                ) from exc

            raise

    @staticmethod
    def get_candidate(
        db: Session,
        candidate_id: UUID,
    ) -> Candidate:
        candidate = CandidateRepository.get_by_id(db, candidate_id)

        if candidate is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate not found.",
            )

        return candidate

    @staticmethod
    def get_candidates(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Candidate]:
        return CandidateRepository.get_all(
            db,
            skip=skip,
            limit=limit,
        )
