
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.interview import InterviewStatus, InterviewType


class InterviewCreate(BaseModel):
    candidate_id: UUID
    interview_type: InterviewType
    job_title: str = Field(min_length=2, max_length=200)


class InterviewResponse(BaseModel):
    id: UUID
    candidate_id: UUID
    interview_type: InterviewType
    status: InterviewStatus
    job_title: str
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
