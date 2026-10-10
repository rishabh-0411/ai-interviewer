import pytest
from pydantic import ValidationError

from app.schemas.candidate import CandidateCreate


def test_valid_candidate():
    candidate = CandidateCreate(
        full_name="Rishabh Karjee",
        email="rishabh@example.com",
    )

    assert candidate.full_name == "Rishabh Karjee"
    assert candidate.email == "rishabh@example.com"


def test_invalid_email():
    with pytest.raises(ValidationError):
        CandidateCreate(
            full_name="Rishabh Karjee",
            email="invalid-email",
        )


def test_name_too_short():
    with pytest.raises(ValidationError):
        CandidateCreate(
            full_name="R",
            email="rishabh@example.com",
        )