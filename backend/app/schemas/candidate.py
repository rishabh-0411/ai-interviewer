from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CandidateCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr


class CandidateResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)