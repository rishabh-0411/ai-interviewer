
def test_create_candidate(client):
    response = client.post(
        "/api/v1/candidates/",
        json={
            "full_name": "Test Candidate",
            "email": "api.test@example.com",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["full_name"] == "Test Candidate"
    assert data["email"] == "api.test@example.com"
    assert "id" in data
    assert "created_at" in data


def test_create_candidate_duplicate_email(client):
    payload = {
        "full_name": "Test Candidate",
        "email": "duplicate@example.com",
    }

    first_response = client.post(
        "/api/v1/candidates/",
        json=payload,
    )

    second_response = client.post(
        "/api/v1/candidates/",
        json=payload,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_create_candidate_invalid_input(client):
    response = client.post(
        "/api/v1/candidates/",
        json={
            "full_name": "R",
            "email": "invalid-email",
        },
    )

    assert response.status_code == 422


def test_list_candidates(client):
    client.post(
        "/api/v1/candidates/",
        json={
            "full_name": "List Test Candidate",
            "email": "list.test@example.com",
        },
    )

    response = client.get("/api/v1/candidates/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(
        candidate["email"] == "list.test@example.com"
        for candidate in response.json()
    )


def test_get_candidate(client):
    create_response = client.post(
        "/api/v1/candidates/",
        json={
            "full_name": "Lookup Candidate",
            "email": "lookup.test@example.com",
        },
    )

    candidate_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/candidates/{candidate_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == candidate_id
    assert response.json()["email"] == "lookup.test@example.com"


def test_get_missing_candidate(client):
    response = client.get(
        "/api/v1/candidates/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404
