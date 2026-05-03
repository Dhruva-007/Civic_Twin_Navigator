"""
Health and root endpoint tests.
"""
import pytest


def test_root_endpoint(client):
    """Test root endpoint returns correct response."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["status"] == "running"
    assert "app" in data
    assert "version" in data


def test_health_endpoint(client):
    """Test health endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["status"] == "healthy"
    assert "project" in data
    assert "model" in data


def test_root_has_app_name(client):
    """Test root endpoint includes app name."""
    response = client.get("/")
    data = response.json()
    assert data["app"] == "Civic Twin Navigator"


def test_health_has_model(client):
    """Test health endpoint includes model name."""
    response = client.get("/health")
    data = response.json()
    assert "gemini" in data["model"].lower()