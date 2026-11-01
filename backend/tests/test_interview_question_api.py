def create_interview(client, email):
    candidate_response = client.post(
        "/api/v1/candidates/",
        json={
            "full_name": "Question API Candidate",
            "email": email,
        },
    )
    candidate_id = candidate_response.json()["id"]

    interview_response = client.post(
        "/api/v1/interviews/",
        json={
            "candidate_id": candidate_id,
            "interview_type": "AI",
            "job_title": "Software Engineer",
        },
    )

    return interview_response.json()["id"]


def test_create_question(client):
    interview_id = create_interview(client, "question.create@example.com")

    response = client.post(
        f"/api/v1/interviews/{interview_id}/questions/",
        json={
            "question_text": "Explain object-oriented programming.",
            "question_type": "MAIN",
            "sequence_number": 1,
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["interview_id"] == interview_id
    assert data["question_text"] == "Explain object-oriented programming."
    assert data["question_type"] == "MAIN"
    assert data["sequence_number"] == 1
    assert "id" in data
    assert "created_at" in data


def test_create_question_missing_interview(client):
    response = client.post(
        "/api/v1/interviews/00000000-0000-0000-0000-000000000000/questions/",
        json={
            "question_text": "A question?",
            "question_type": "MAIN",
            "sequence_number": 1,
        },
    )

    assert response.status_code == 404


def test_list_questions(client):
    interview_id = create_interview(client, "question.list@example.com")

    client.post(
        f"/api/v1/interviews/{interview_id}/questions/",
        json={
            "question_text": "First question?",
            "question_type": "MAIN",
            "sequence_number": 1,
        },
    )
    client.post(
        f"/api/v1/interviews/{interview_id}/questions/",
        json={
            "question_text": "Follow-up question?",
            "question_type": "FOLLOW_UP",
            "sequence_number": 2,
        },
    )

    response = client.get(
        f"/api/v1/interviews/{interview_id}/questions/"
    )

    assert response.status_code == 200
    questions = response.json()
    assert len(questions) == 2
    assert questions[0]["sequence_number"] == 1
    assert questions[1]["sequence_number"] == 2


def test_get_question(client):
    interview_id = create_interview(client, "question.get@example.com")

    create_response = client.post(
        f"/api/v1/interviews/{interview_id}/questions/",
        json={
            "question_text": "What is a database index?",
            "question_type": "MAIN",
            "sequence_number": 1,
        },
    )
    question_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/interviews/{interview_id}/questions/{question_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == question_id
    assert response.json()["question_text"] == "What is a database index?"


def test_get_question_from_different_interview_returns_404(client):
    first_interview_id = create_interview(
        client,
        "question.first@example.com",
    )
    second_interview_id = create_interview(
        client,
        "question.second@example.com",
    )

    create_response = client.post(
        f"/api/v1/interviews/{first_interview_id}/questions/",
        json={
            "question_text": "A question?",
            "question_type": "MAIN",
            "sequence_number": 1,
        },
    )
    question_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/interviews/{second_interview_id}/questions/{question_id}"
    )

    assert response.status_code == 404


def test_get_missing_question(client):
    interview_id = create_interview(client, "question.missing@example.com")

    response = client.get(
        f"/api/v1/interviews/{interview_id}/questions/"
        "00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404

def create_question(client, interview_id):
    response = client.post(
        f"/api/v1/interviews/{interview_id}/questions/",
        json={
            "question_text": "Explain object-oriented programming.",
            "question_type": "MAIN",
            "sequence_number": 1,
        },
    )
    return response.json()["id"]


def test_create_answer(client):
    interview_id = create_interview(client, "answer.create@example.com")
    question_id = create_question(client, interview_id)

    response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "answer_text": "OOP organizes code around objects and classes.",
            "sequence_number": 1,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["question_id"] == question_id
    assert data["answer_text"] == "OOP organizes code around objects and classes."
    assert data["sequence_number"] == 1
    assert "answered_at" in data
    assert "id" in data


def test_create_answer_missing_question(client):
    response = client.post(
        "/api/v1/questions/00000000-0000-0000-0000-000000000000/answers/",
        json={
            "answer_text": "An answer.",
            "sequence_number": 1,
        },
    )

    assert response.status_code == 404


def test_list_answers(client):
    interview_id = create_interview(client, "answer.list@example.com")
    question_id = create_question(client, interview_id)

    for sequence_number, answer_text in [
        (2, "Second answer"),
        (1, "First answer"),
    ]:
        client.post(
            f"/api/v1/questions/{question_id}/answers/",
            json={
                "answer_text": answer_text,
                "sequence_number": sequence_number,
            },
        )

    response = client.get(
        f"/api/v1/questions/{question_id}/answers/"
    )

    assert response.status_code == 200
    answers = response.json()
    assert len(answers) == 2
    assert answers[0]["sequence_number"] == 1
    assert answers[1]["sequence_number"] == 2


def test_get_answer(client):
    interview_id = create_interview(client, "answer.get@example.com")
    question_id = create_question(client, interview_id)

    create_response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "answer_text": "A sample answer.",
            "sequence_number": 1,
        },
    )
    answer_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/questions/{question_id}/answers/{answer_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == answer_id
    assert response.json()["answer_text"] == "A sample answer."


def test_get_answer_from_different_question_returns_404(client):
    interview_id = create_interview(client, "answer.cross@example.com")
    first_question_id = create_question(client, interview_id)

    second_question_response = client.post(
        f"/api/v1/interviews/{interview_id}/questions/",
        json={
            "question_text": "A second question?",
            "question_type": "FOLLOW_UP",
            "sequence_number": 2,
        },
    )
    second_question_id = second_question_response.json()["id"]

    create_response = client.post(
        f"/api/v1/questions/{first_question_id}/answers/",
        json={
            "answer_text": "An answer.",
            "sequence_number": 1,
        },
    )
    answer_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/questions/{second_question_id}/answers/{answer_id}"
    )

    assert response.status_code == 404


def test_get_missing_answer(client):
    interview_id = create_interview(client, "answer.missing@example.com")
    question_id = create_question(client, interview_id)

    response = client.get(
        f"/api/v1/questions/{question_id}/answers/"
        "00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404