from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate


class CandidateRepository:

    @staticmethod
    def create(db: Session, candidate_data: CandidateCreate) -> Candidate:
        candidate = Candidate(
            full_name=candidate_data.full_name,
            email=str(candidate_data.email),
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        return candidate

    @staticmethod
    def get_by_id(db: Session, candidate_id: UUID) -> Candidate | None:
        statement = select(Candidate).where(
            Candidate.id == candidate_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_by_email(db: Session, email: str) -> Candidate | None:
        statement = select(Candidate).where(
            Candidate.email == email
        )

        return db.scalar(statement)

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Candidate]:
        statement = (
            select(Candidate)
            .order_by(Candidate.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(db.scalars(statement).all())