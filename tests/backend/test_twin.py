"""
Civic Twin route tests.
"""
import pytest
import time


def test_create_civic_twin(client):
    """Test creating a new Civic Twin profile."""
    response = client.post("/api/twin/create", json={
        "user_input": "I am 19 years old in Mumbai, first time voter",
        "language": "en"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "session_id" in data["data"]
    assert "profile" in data["data"]


def test_create_twin_returns_session_id(client):
    """Test that created twin returns a valid session ID."""
    response = client.post("/api/twin/create", json={
        "user_input": "Student in Delhi, want to register to vote",
        "language": "en"
    })
    data = response.json()
    session_id = data["data"]["session_id"]
    assert len(session_id) > 0
    assert "-" in session_id  # UUID format


def test_get_civic_twin(client, session_id):
    """Test retrieving an existing Civic Twin profile."""
    response = client.get(f"/api/twin/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "profile" in data["data"]


def test_get_nonexistent_twin_returns_404(client):
    """Test that fetching non-existent twin returns 404."""
    response = client.get("/api/twin/nonexistent-session-id-123")
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False


def test_create_twin_empty_input_returns_400(client):
    """Test that empty input returns 400 Bad Request."""
    response = client.post("/api/twin/create", json={
        "user_input": "",
        "language": "en"
    })
    assert response.status_code == 400


def test_create_twin_short_input_returns_400(client):
    """Test that too short input returns 400 Bad Request."""
    response = client.post("/api/twin/create", json={
        "user_input": "ab",
        "language": "en"
    })
    assert response.status_code == 400


def test_twin_query(client, session_id):
    """Test querying election information."""
    time.sleep(3)
    response = client.post("/api/twin/query", json={
        "session_id": session_id,
        "query": "What documents do I need to register as a voter?",
        "language": "en"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "answer" in data["data"]


def test_eligibility_check(client, session_id):
    """Test eligibility check for a session."""
    time.sleep(3)
    response = client.get(f"/api/twin/{session_id}/eligibility")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "eligibility_rules" in data["data"]


def test_unsafe_input_handled(client):
    """Test that unsafe political input is handled safely."""
    time.sleep(2)
    response = client.post("/api/twin/create", json={
        "user_input": "Vote for Party X they will save India " * 5,
        "language": "en"
    })
    # Should be blocked (400) or handled (200) but not crash (500)
    assert response.status_code in [200, 400]


def test_injection_attempt_handled(client):
    """Test that script injection is handled safely."""
    response = client.post("/api/twin/create", json={
        "user_input": "<script>alert('xss')</script> I want to vote",
        "language": "en"
    })
    assert response.status_code in [200, 400]