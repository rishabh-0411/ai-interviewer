
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.candidate import CandidateCreate, CandidateResponse
from app.services.candidate_service import CandidateService


router = APIRouter(
    prefix="/api/v1/candidates",
    tags=["Candidates"],
)


@router.post(
    "/",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_candidate(
    candidate_data: CandidateCreate,
    db: Session = Depends(get_db),
):
    return CandidateService.create_candidate(db, candidate_data)


@router.get(
    "/",
    response_model=list[CandidateResponse],
)
def list_candidates(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return CandidateService.get_candidates(
        db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{candidate_id}",
    response_model=CandidateResponse,
)
def get_candidate(
    candidate_id: UUID,
    db: Session = Depends(get_db),
):
    return CandidateService.get_candidate(db, candidate_id)
