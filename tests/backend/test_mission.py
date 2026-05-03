"""
Mission route tests.
"""
import pytest
import time


def test_start_mission(client, session_id):
    """Test starting an interactive mission."""
    time.sleep(3)
    response = client.post("/api/mission/start", json={
        "session_id": session_id,
        "mission_number": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "mission" in data["data"]


def test_mission_has_questions(client, session_id):
    """Test that mission contains questions."""
    time.sleep(3)
    response = client.post("/api/mission/start", json={
        "session_id": session_id,
        "mission_number": 2
    })
    assert response.status_code == 200
    data = response.json()
    mission = data["data"]["mission"]
    assert "questions" in mission
    assert len(mission["questions"]) > 0


def test_invalid_mission_number_returns_400(client, session_id):
    """Test that invalid mission number returns 400."""
    response = client.post("/api/mission/start", json={
        "session_id": session_id,
        "mission_number": 99
    })
    assert response.status_code == 400


def test_mission_number_zero_returns_400(client, session_id):
    """Test that mission number 0 returns 400."""
    response = client.post("/api/mission/start", json={
        "session_id": session_id,
        "mission_number": 0
    })
    assert response.status_code == 400


def test_run_scenario(client, session_id):
    """Test running a what-if scenario."""
    time.sleep(5)
    response = client.post("/api/mission/scenario", json={
        "session_id": session_id,
        "scenario": "What if I miss the voter registration deadline?"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "scenario" in data["data"]


def test_scenario_has_recovery_steps(client, session_id):
    """Test that scenario response contains recovery steps."""
    time.sleep(5)
    response = client.post("/api/mission/scenario", json={
        "session_id": session_id,
        "scenario": "What if my name is not on the voter list?"
    })
    assert response.status_code == 200
    data = response.json()
    scenario = data["data"]["scenario"]
    assert "recovery_steps" in scenario


def test_mission_progress(client, session_id):
    """Test mission progress endpoint."""
    response = client.get(f"/api/mission/{session_id}/progress")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "total_missions" in data["data"]