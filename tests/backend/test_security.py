"""
Security and edge case tests for Civic Twin Navigator.

Tests:
- Input validation boundaries
- Security headers presence
- Authentication security
- Edge cases and boundary conditions
"""
import pytest
import time


class TestInputValidation:
    """Test input validation across all endpoints."""

    def test_translate_text_too_long_returns_400(self, client):
        """Test that text exceeding 5000 chars returns 400."""
        long_text = "a" * 5001
        response = client.post("/api/translate", json={
            "text": long_text,
            "target_language": "hi",
            "source_language": "en"
        })
        assert response.status_code == 400

    def test_translate_batch_too_many_returns_400(self, client):
        """Test that batch exceeding 50 items returns 400."""
        texts = ["Vote"] * 51
        response = client.post("/api/translate/batch", json={
            "texts": texts,
            "target_language": "hi",
            "source_language": "en"
        })
        assert response.status_code == 400

    def test_twin_input_too_long_returns_400(self, client):
        """Test that user input exceeding 2000 chars returns 400."""
        long_input = "I want to vote in India " * 100
        response = client.post("/api/twin/create", json={
            "user_input": long_input,
            "language": "en"
        })
        assert response.status_code == 400

    def test_twin_input_too_short_returns_400(self, client):
        """Test that input less than 3 chars returns 400."""
        response = client.post("/api/twin/create", json={
            "user_input": "ab",
            "language": "en"
        })
        assert response.status_code == 400

    def test_twin_input_empty_returns_400(self, client):
        """Test that empty input returns 400."""
        response = client.post("/api/twin/create", json={
            "user_input": "",
            "language": "en"
        })
        assert response.status_code == 400

    def test_scenario_too_long_returns_400(self, client, session_id):
        """Test that scenario exceeding 500 chars returns 400."""
        long_scenario = "What if " * 100
        response = client.post("/api/mission/scenario", json={
            "session_id": session_id,
            "scenario": long_scenario
        })
        assert response.status_code == 400

    def test_empty_scenario_returns_400(self, client, session_id):
        """Test that empty scenario returns 400."""
        response = client.post("/api/mission/scenario", json={
            "session_id": session_id,
            "scenario": ""
        })
        assert response.status_code == 400

    def test_translate_empty_text_returns_400(self, client):
        """Test that empty translation text returns 400."""
        response = client.post("/api/translate", json={
            "text": "",
            "target_language": "hi",
            "source_language": "en"
        })
        assert response.status_code == 400

    def test_translate_batch_empty_list_returns_400(self, client):
        """Test that empty batch list returns 400."""
        response = client.post("/api/translate/batch", json={
            "texts": [],
            "target_language": "hi",
            "source_language": "en"
        })
        assert response.status_code == 400


class TestSecurityHeaders:
    """Test that all security headers are present in responses."""

    def test_x_content_type_options_header(self, client):
        """Test X-Content-Type-Options header prevents MIME sniffing."""
        response = client.get("/")
        assert "x-content-type-options" in response.headers
        assert response.headers["x-content-type-options"] == "nosniff"

    def test_x_frame_options_header(self, client):
        """Test X-Frame-Options header prevents clickjacking."""
        response = client.get("/")
        assert "x-frame-options" in response.headers
        assert response.headers["x-frame-options"] == "DENY"

    def test_x_xss_protection_header(self, client):
        """Test X-XSS-Protection header is present."""
        response = client.get("/")
        assert "x-xss-protection" in response.headers

    def test_referrer_policy_header(self, client):
        """Test Referrer-Policy header controls referrer information."""
        response = client.get("/")
        assert "referrer-policy" in response.headers

    def test_permissions_policy_header(self, client):
        """Test Permissions-Policy header restricts browser features."""
        response = client.get("/")
        assert "permissions-policy" in response.headers

    def test_content_security_policy_header(self, client):
        """Test Content-Security-Policy header prevents XSS attacks."""
        response = client.get("/")
        assert "content-security-policy" in response.headers

    def test_process_time_header(self, client):
        """Test X-Process-Time performance tracking header is present."""
        response = client.get("/")
        assert "x-process-time" in response.headers
        # Should be a valid number
        process_time = float(response.headers["x-process-time"])
        assert process_time >= 0


class TestAuthSecurity:
    """Test authentication security boundaries."""

    def test_invalid_token_returns_401(self, client):
        """Test that invalid Firebase token returns 401."""
        response = client.post("/api/auth/verify", json={
            "id_token": "completely.invalid.token.string"
        })
        assert response.status_code == 401

    def test_empty_token_returns_422(self, client):
        """Test that missing token field returns 422 validation error."""
        response = client.post("/api/auth/verify", json={})
        assert response.status_code == 422

    def test_link_session_invalid_token_returns_401(self, client, session_id):
        """Test session linking with invalid token returns 401."""
        response = client.post("/api/auth/link-session", json={
            "session_id": session_id,
            "id_token": "invalid.token.here"
        })
        assert response.status_code == 401

    def test_get_profile_nonexistent_returns_404(self, client):
        """Test that non-existent user profile returns 404."""
        response = client.get("/api/auth/profile/nonexistent_user_xyz_123")
        assert response.status_code == 404

    def test_get_sessions_nonexistent_user_returns_empty(self, client):
        """Test sessions for non-existent user returns empty list."""
        response = client.get("/api/auth/sessions/nonexistent_user_xyz_123")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["total"] == 0


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_mission_number_negative_returns_400(self, client, session_id):
        """Test that negative mission number is rejected."""
        response = client.post("/api/mission/start", json={
            "session_id": session_id,
            "mission_number": -1
        })
        assert response.status_code == 400

    def test_mission_number_too_large_returns_400(self, client, session_id):
        """Test that mission number greater than 5 is rejected."""
        response = client.post("/api/mission/start", json={
            "session_id": session_id,
            "mission_number": 100
        })
        assert response.status_code == 400

    def test_mission_number_zero_returns_400(self, client, session_id):
        """Test that mission number 0 is rejected."""
        response = client.post("/api/mission/start", json={
            "session_id": session_id,
            "mission_number": 0
        })
        assert response.status_code == 400

    def test_get_journey_wrong_session_returns_404(self, client):
        """Test that non-existent journey returns 404."""
        response = client.get("/api/journey/00000000-0000-4000-8000-000000000000")
        assert response.status_code == 404

    def test_health_response_time_is_fast(self, client):
        """Test that health check responds in under 2 seconds."""
        start = time.time()
        response = client.get("/health")
        elapsed = time.time() - start
        assert response.status_code == 200
        assert elapsed < 2.0

    def test_root_response_time_is_fast(self, client):
        """Test that root endpoint responds in under 1 second."""
        start = time.time()
        response = client.get("/")
        elapsed = time.time() - start
        assert response.status_code == 200
        assert elapsed < 1.0

    def test_api_returns_json_content_type(self, client):
        """Test that all API endpoints return JSON content type."""
        response = client.get("/")
        assert response.headers["content-type"].startswith("application/json")

    def test_health_returns_json_content_type(self, client):
        """Test that health endpoint returns JSON content type."""
        response = client.get("/health")
        assert response.headers["content-type"].startswith("application/json")

    def test_404_returns_json_not_html(self, client):
        """Test that 404 errors return JSON format not HTML."""
        response = client.get("/api/completely-nonexistent-endpoint-xyz")
        assert response.status_code == 404
        data = response.json()
        assert "success" in data
        assert data["success"] is False
        assert "error" in data

    def test_nonexistent_session_twin_returns_404(self, client):
        """Test that fetching twin with invalid session returns 404."""
        response = client.get("/api/twin/00000000-0000-4000-8000-000000000000")
        assert response.status_code == 404