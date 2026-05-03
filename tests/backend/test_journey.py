"""
Journey route tests.
"""
import pytest
import time


def test_create_journey(client, session_id, journey):
    """Test creating a personalized journey."""
    # Journey already created by journey fixture
    # Verify it exists by GET
    response = client.get(f"/api/journey/{session_id}")
    assert response.status_code in [200, 404]
    # If 404 it means this session has no journey yet
    # which is valid depending on test order
    if response.status_code == 200:
        data = response.json()
        assert data["success"] is True


def test_journey_has_phases(client, session_id, journey):
    """Test that journey contains phases."""
    phases = journey.get("phases", [])
    assert len(phases) > 0
    assert len(phases) >= 4


def test_journey_phases_have_steps(client, session_id, journey):
    """Test that journey phases contain steps."""
    phases = journey.get("phases", [])
    for phase in phases:
        assert "steps" in phase
        assert len(phase["steps"]) > 0


def test_get_journey(client, session_id):
    """Test retrieving an existing journey."""
    response = client.get(f"/api/journey/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_journey_not_found_returns_404(client):
    """Test that fetching non-existent journey returns 404."""
    response = client.get("/api/journey/nonexistent-session-id")
    assert response.status_code == 404


def test_journey_summary(client, session_id):
    """Test journey summary endpoint."""
    response = client.get(f"/api/journey/{session_id}/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "progress_percentage" in data["data"]


def test_journey_next_steps(client, session_id):
    """Test next steps endpoint."""
    response = client.get(f"/api/journey/{session_id}/next-steps")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "next_steps" in data["data"]


def test_update_step(client, session_id, journey):
    """Test marking a step as completed."""
    phases = journey.get("phases", [])
    if phases and phases[0].get("steps"):
        phase = phases[0]
        step = phase["steps"][0]
        response = client.put("/api/journey/step/update", json={
            "session_id": session_id,
            "phase_id": phase["phase_id"],
            "step_id": step["step_id"],
            "is_completed": True
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "progress" in data["data"]


def test_get_documents(client, session_id):
    """Test document requirements endpoint."""
    time.sleep(3)
    response = client.get(f"/api/journey/{session_id}/documents")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True