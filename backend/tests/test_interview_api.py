def test_create_interview(client):
    candidate_response = client.post(
        "/api/v1/candidates/",
        json={
            "full_name": "Interview Test Candidate",
            "email": "interview.test@example.com",
        },
    )
    candidate_id = candidate_response.json()["id"]

    response = client.post(
        "/api/v1/interviews/",
        json={
            "candidate_id": candidate_id,
            "interview_type": "AI",
            "job_title": "Software Engineer",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["candidate_id"] == candidate_id
    assert data["interview_type"] == "AI"
    assert data["status"] == "SCHEDULED"
    assert data["job_title"] == "Software Engineer"
    assert "id" in data
    assert "created_at" in data


def test_create_interview_missing_candidate(client):
    response = client.post(
        "/api/v1/interviews/",
        json={
            "candidate_id": "00000000-0000-0000-0000-000000000000",
            "interview_type": "AI",
            "job_title": "Software Engineer",
        },
    )

    assert response.status_code == 404


def test_list_interviews(client):
    candidate_response = client.post(
        "/api/v1/candidates/",
        json={
            "full_name": "Interview List Candidate",
            "email": "interview.list@example.com",
        },
    )
    candidate_id = candidate_response.json()["id"]

    client.post(
        "/api/v1/interviews/",
        json={
            "candidate_id": candidate_id,
            "interview_type": "HUMAN",
            "job_title": "Backend Engineer",
        },
    )

    response = client.get("/api/v1/interviews/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(
        interview["candidate_id"] == candidate_id
        for interview in response.json()
    )


def test_get_interview(client):
    candidate_response = client.post(
        "/api/v1/candidates/",
        json={
            "full_name": "Interview Lookup Candidate",
            "email": "interview.lookup@example.com",
        },
    )
    candidate_id = candidate_response.json()["id"]

    create_response = client.post(
        "/api/v1/interviews/",
        json={
            "candidate_id": candidate_id,
            "interview_type": "AI",
            "job_title": "Data Engineer",
        },
    )
    interview_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/interviews/{interview_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == interview_id
    assert response.json()["job_title"] == "Data Engineer"


def test_get_missing_interview(client):
    response = client.get(
        "/api/v1/interviews/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404