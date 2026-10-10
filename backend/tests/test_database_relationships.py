from datetime import datetime, timezone

from app.db.session import SessionLocal
from app.models import (
    Candidate,
    Interview,
    InterviewAnswer,
    InterviewQuestion,
    InterviewStatus,
    InterviewType,
    QuestionType,
)


def main():
    db = SessionLocal()

    try:
        # 1. Create candidate
        candidate = Candidate(
            full_name="Database Test Candidate",
            email="database-test@example.com",
        )

        db.add(candidate)
        db.flush()

        # 2. Create interview
        interview = Interview(
            candidate=candidate,
            interview_type=InterviewType.AI,
            status=InterviewStatus.SCHEDULED,
            job_title="Software Engineer",
        )

        db.add(interview)
        db.flush()

        # 3. Create question
        question = InterviewQuestion(
            interview=interview,
            question_text="Tell me about your experience with Python.",
            question_type=QuestionType.MAIN,
            sequence_number=1,
        )

        db.add(question)
        db.flush()

        # 4. Create answer
        answer = InterviewAnswer(
            question=question,
            answer_text="I have used Python for backend development and AI projects.",
            sequence_number=1,
            answered_at=datetime.now(timezone.utc),
        )

        db.add(answer)
        db.commit()

        print("Candidate ID:", candidate.id)
        print("Interview ID:", interview.id)
        print("Question ID:", question.id)
        print("Answer ID:", answer.id)

        # 5. Test relationships
        print("\nRelationship checks:")
        print("Candidate interviews:", len(candidate.interviews))
        print("Interview questions:", len(interview.questions))
        print("Question answers:", len(question.answers))

        # 6. Clean up test data
        db.delete(candidate)
        db.commit()

        print("\nDatabase relationship test PASSED.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()