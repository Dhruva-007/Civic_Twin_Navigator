import sys
import os
import pytest

# Fix path so pytest can find backend modules
backend_path = os.path.join(os.path.dirname(__file__), '../../backend')
sys.path.insert(0, os.path.abspath(backend_path))

# Load .env before anything imports settings
from dotenv import load_dotenv
load_dotenv(os.path.abspath(os.path.join(backend_path, '.env')))

from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="session")
def client():
    """
    Session-scoped FastAPI test client.
    Created once and reused across all tests.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def session_id(client):
    """
    Session-scoped fixture that creates one Civic Twin
    and reuses the session_id across all tests.
    """
    response = client.post("/api/twin/create", json={
        "user_input": "I am a 20 year old student in Pune, first time voter, living in hostel",
        "language": "en"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    return data["data"]["session_id"]


@pytest.fixture(scope="session")
def journey(client, session_id):
    """
    Session-scoped fixture that creates one Journey
    and reuses it across all journey tests.
    """
    import time
    time.sleep(2)
    response = client.post("/api/journey/create", json={
        "session_id": session_id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    return data["data"]["journey"]