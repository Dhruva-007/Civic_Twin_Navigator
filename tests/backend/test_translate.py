"""
Translation route tests.
"""
import pytest


def test_translate_text(client):
    """Test basic text translation."""
    response = client.post("/api/translate", json={
        "text": "Hello, I want to vote.",
        "target_language": "hi",
        "source_language": "en"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "translated_text" in data["data"]


def test_translate_same_language(client):
    """Test that same language returns original text."""
    response = client.post("/api/translate", json={
        "text": "Hello, I want to vote.",
        "target_language": "en",
        "source_language": "en"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["translated_text"] == "Hello, I want to vote."


def test_translate_to_marathi(client):
    """Test translation to Marathi."""
    response = client.post("/api/translate", json={
        "text": "Voter registration",
        "target_language": "mr",
        "source_language": "en"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["translated_text"]) > 0


def test_translate_to_tamil(client):
    """Test translation to Tamil."""
    response = client.post("/api/translate", json={
        "text": "Election day",
        "target_language": "ta",
        "source_language": "en"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_translate_empty_text_returns_400(client):
    """Test that empty text returns 400."""
    response = client.post("/api/translate", json={
        "text": "",
        "target_language": "hi",
        "source_language": "en"
    })
    assert response.status_code == 400


def test_translate_batch(client):
    """Test batch translation."""
    response = client.post("/api/translate/batch", json={
        "texts": ["Vote", "Election", "Registration"],
        "target_language": "hi",
        "source_language": "en"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "translations" in data["data"]
    assert len(data["data"]["translations"]) == 3


def test_translate_batch_empty_returns_400(client):
    """Test that empty batch returns 400."""
    response = client.post("/api/translate/batch", json={
        "texts": [],
        "target_language": "hi",
        "source_language": "en"
    })
    assert response.status_code == 400