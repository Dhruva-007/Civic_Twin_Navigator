"""
Assessment route tests.
"""
import pytest
import time


def test_calculate_readiness(client, session_id):
    """Test readiness score calculation."""
    time.sleep(5)
    response = client.post("/api/assessment/readiness", json={
        "session_id": session_id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "readiness_score" in data["data"]


def test_readiness_score_has_overall(client, session_id):
    """Test that readiness score contains overall score."""
    time.sleep(5)
    response = client.post("/api/assessment/readiness", json={
        "session_id": session_id
    })
    data = response.json()
    score = data["data"]["readiness_score"]
    assert "overall_score" in score
    assert 0 <= score["overall_score"] <= 100


def test_readiness_score_has_breakdown(client, session_id):
    """Test that readiness score has score breakdown."""
    time.sleep(5)
    response = client.post("/api/assessment/readiness", json={
        "session_id": session_id
    })
    data = response.json()
    score = data["data"]["readiness_score"]
    assert "scores" in score


def test_get_score(client, session_id):
    """Test retrieving saved readiness score."""
    response = client.get(f"/api/assessment/{session_id}/score")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert data["success"] is True


def test_get_predictions(client, session_id):
    """Test failure risk predictions."""
    time.sleep(3)
    response = client.get(f"/api/assessment/{session_id}/predictions")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_generate_proof(client, session_id):
    """Test proof of readiness generation."""
    time.sleep(5)
    response = client.post("/api/assessment/proof-of-readiness", json={
        "session_id": session_id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "proof" in data["data"]


def test_get_session_logs(client, session_id):
    """Test session evidence logs retrieval."""
    response = client.get(f"/api/assessment/{session_id}/logs")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True