import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.interview_answer import InterviewAnswer

from app.db.base import Base


class QuestionType(str, enum.Enum):
    MAIN = "MAIN"
    FOLLOW_UP = "FOLLOW_UP"
    CLARIFICATION = "CLARIFICATION"
    DEEP_DIVE = "DEEP_DIVE"
    BEHAVIORAL = "BEHAVIORAL"
    SCENARIO = "SCENARIO"
    RESUME = "RESUME"
    JOB_SPECIFIC = "JOB_SPECIFIC"


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    interview_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("interviews.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    question_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    question_type: Mapped[QuestionType] = mapped_column(
        Enum(QuestionType),
        nullable=False,
    )

    sequence_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    interview: Mapped["Interview"] = relationship(
        back_populates="questions",
    )

    answers: Mapped[list["InterviewAnswer"]] = relationship(
    back_populates="question",
    cascade="all, delete-orphan",
    )