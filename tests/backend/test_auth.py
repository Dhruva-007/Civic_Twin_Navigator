"""
Authentication route tests.
"""
import pytest


def test_verify_token_missing_returns_422(client):
    """Test that missing token returns 422 validation error."""
    response = client.post("/api/auth/verify", json={})
    assert response.status_code == 422


def test_verify_invalid_token_returns_401(client):
    """Test that invalid token returns 401."""
    response = client.post("/api/auth/verify", json={
        "id_token": "invalid_token_string"
    })
    assert response.status_code == 401
    # FastAPI HTTPException returns "detail" not "success"
    data = response.json()
    assert "detail" in data


def test_link_session_invalid_token_returns_401(client, session_id):
    """Test that link session with invalid token returns 401."""
    response = client.post("/api/auth/link-session", json={
        "session_id": session_id,
        "id_token": "invalid_token_string"
    })
    assert response.status_code == 401


def test_get_profile_nonexistent_returns_404(client):
    """Test that non-existent user profile returns 404."""
    response = client.get("/api/auth/profile/nonexistent_user_id_xyz")
    assert response.status_code == 404


def test_get_sessions_nonexistent_user(client):
    """Test sessions endpoint for non-existent user."""
    response = client.get("/api/auth/sessions/nonexistent_user_id_xyz")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["total"] == 0


def test_logout_nonexistent_user(client):
    """Test logout for non-existent user still succeeds."""
    response = client.delete("/api/auth/logout/nonexistent_user_id")
    assert response.status_code == 200