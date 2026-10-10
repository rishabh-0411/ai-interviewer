import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.candidate import Candidate
from app.db.base import Base
from app.models.interview_question import InterviewQuestion

class InterviewType(str, enum.Enum):
    AI = "AI"
    HUMAN = "HUMAN"


class InterviewStatus(str, enum.Enum):
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Interview(Base):
    __tablename__ = "interviews"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    interview_type: Mapped[InterviewType] = mapped_column(
        Enum(InterviewType),
        nullable=False,
    )

    status: Mapped[InterviewStatus] = mapped_column(
        Enum(InterviewStatus),
        nullable=False,
        default=InterviewStatus.SCHEDULED,
    )

    job_title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    candidate: Mapped["Candidate"] = relationship(
        back_populates="interviews",
    )

    questions: Mapped[list["InterviewQuestion"]] = relationship(
    back_populates="interview",
    cascade="all, delete-orphan",
    )