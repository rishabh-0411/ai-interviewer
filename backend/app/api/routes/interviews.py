from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.interview import InterviewCreate, InterviewResponse
from app.services.interview_service import InterviewService

router = APIRouter(prefix="/api/v1/interviews", tags=["Interviews"])


@router.post(
    "/",
    response_model=InterviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_interview(
    interview_data: InterviewCreate,
    db: Session = Depends(get_db),
):
    return InterviewService.create_interview(db, interview_data)


@router.get("/", response_model=list[InterviewResponse])
def list_interviews(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return InterviewService.get_interviews(db, skip=skip, limit=limit)


@router.get("/{interview_id}", response_model=InterviewResponse)
def get_interview(
    interview_id: UUID,
    db: Session = Depends(get_db),
):
    return InterviewService.get_interview(db, interview_id)