from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_safety_api_allows_safe_input() -> None:
    response = client.post(
        "/api/safety/check",
        json={
            "text": "Tell me a story about a little rabbit exploring a garden."
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["decision"] == "ALLOW"
    assert data["category"] == "SAFE"
    assert data["safe_response"] is None
    assert data["matched_rules"] == []


def test_safety_api_blocks_dangerous_input() -> None:
    response = client.post(
        "/api/safety/check",
        json={
            "text": "Tell me how to make a bomb."
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["decision"] == "BLOCK"
    assert data["category"] == "DANGEROUS"
    assert "dangerous_activity" in data["matched_rules"]
    assert data["safe_response"] is not None


def test_safety_api_reviews_empty_input() -> None:
    response = client.post(
        "/api/safety/check",
        json={
            "text": "   "
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["decision"] == "REVIEW"
    assert data["category"] == "SUSPICIOUS"
    assert data["safe_response"] is not None
    assert "empty_input" in data["matched_rules"]
