
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.interview import InterviewStatus, InterviewType
from app.models.interview_question import QuestionType


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

class InterviewQuestionCreate(BaseModel):
    question_text: str = Field(min_length=1)
    question_type: QuestionType
    sequence_number: int = Field(ge=1)


class InterviewQuestionResponse(BaseModel):
    id: UUID
    interview_id: UUID
    question_text: str
    question_type: QuestionType
    sequence_number: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class InterviewAnswerCreate(BaseModel):
    answer_text: str = Field(min_length=1)
    sequence_number: int = Field(ge=1)


class InterviewAnswerResponse(BaseModel):
    id: UUID
    question_id: UUID
    answer_text: str
    sequence_number: int
    answered_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)