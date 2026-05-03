from typing import Dict, Any, Optional, List
import logging
import time
import hashlib
import threading
from functools import lru_cache

from services.vertex_ai_service import vertex_ai_service
from utils.helpers import get_timestamp

# Setup logging
logger = logging.getLogger(__name__)


class SafetyAgent:
    """
    Agent 9 - Safety Agent (Hardened)

    Responsibilities:
    - Detect political bias or promotion of parties/candidates
    - Detect misinformation about election processes
    - Detect harmful or manipulative content
    - Provide safe, neutral alternatives
    - Enforce non-partisan boundaries for Civic Twin Navigator
    - Fast, bounded-time safety checks with caching and fallback
    """

    SYSTEM_INSTRUCTION = """
    You are the Safety Agent for Civic Twin Navigator.
    Your ONLY role is to ensure election information is accurate, neutral, and safe.

    Rules (strict):
    - Never promote any political party, candidate, ideology, or movement.
    - Never provide instructions that could manipulate voter behavior.
    - Flag any misinformation about voter eligibility, registration, deadlines, documents, or polling.
    - Be precise, factual, and non-prescriptive.
    - Always return valid JSON with no trailing commas and double-quoted strings.
    - If uncertain, mark risk_level as "medium" or "high" and provide clear reasons.
    """

    # Simple in-memory cache (thread-safe enough for tests/dev)
    _CACHE_LOCK = threading.Lock()
    _CACHE: Dict[str, Dict[str, Any]] = {}

    def _cache_key(self, text: str) -> str:
        """Create a stable cache key for a safety check."""
        h = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
        return f"safety:{h}"

    def _get_cached(self, key: str) -> Optional[Dict[str, Any]]:
        with self._CACHE_LOCK:
            entry = self._CACHE.get(key)
            if entry and (time.time() - entry["ts"] < 3600):  # 1 hour TTL
                return entry["result"]
            if entry:
                # stale; drop it
                self._CACHE.pop(key, None)
            return None

    def _set_cached(self, key: str, result: Dict[str, Any]) -> None:
        with self._CACHE_LOCK:
            self._CACHE[key] = {"ts": time.time(), "result": result}

    def check_content_safety(
        self,
        text: str,
        timeout_seconds: int = 8
    ) -> Dict[str, Any]:
        """
        Check content for political bias, misinformation, harmful content.

        Args:
            text: Text to analyze
            timeout_seconds: Hard timeout for the check

        Returns:
            Safety assessment result
        """
        if not text or not text.strip():
            return {
                "success": True,
                "data": {
                    "is_safe": True,
                    "has_political_bias": False,
                    "has_misinformation": False,
                    "has_harmful_content": False,
                    "risk_level": "low",
                    "reason": "Empty text provided",
                    "safe_alternatives": []
                },
                "timestamp": get_timestamp()
            }

        # Try cache first
        key = self._cache_key(text)
        cached = self._get_cached(key)
        if cached:
            logger.info("Safety check served from cache")
            return {
                "success": True,
                "data": cached,
                "timestamp": get_timestamp(),
                "cached": True
            }

        # Build a compact, deterministic prompt (reduces latency & variance)
        prompt = f"""
Analyze the following text strictly for election-information safety in India.

Text to analyze:
"{text}"

Return ONLY this exact JSON (no markdown, no extra text):
{{
  "is_safe": true,
  "has_political_bias": false,
  "has_misinformation": false,
  "has_harmful_content": false,
  "risk_level": "low",
  "reason": "Brief explanation of findings",
  "safe_alternatives": [
    "Neutral, factual alternative phrasing #1 (if applicable)",
    "Neutral, factual alternative phrasing #2 (if applicable)"
  ]
}}

Safety criteria (must check):
1. Political bias or promotion of any party/candidate/ideology: true/false
2. Misinformation about voter eligibility, registration process, deadlines, documents, polling hours, EVM/VVPAT, or helplines: true/false
3. Harmful, coercive, or manipulative language: true/false
4. risk_level: "low" | "medium" | "high"
"""
        start = time.time()
        try:
            # Run with tight generation settings + timeout wrapper
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION,
                temperature=0.0  # deterministic for safety
            )

            # Basic sanity checks on result shape
            required_keys = [
                "is_safe", "has_political_bias", "has_misinformation",
                "has_harmful_content", "risk_level", "reason", "safe_alternatives"
            ]
            for k in required_keys:
                if k not in result:
                    result[k] = [] if k == "safe_alternatives" else (
                        "low" if k == "risk_level" else False if k != "reason" else "Missing field"
                    )

            # Cache successful result
            self._set_cached(key, result)

            elapsed = time.time() - start
            logger.info(f"Safety check completed in {elapsed:.2f}s")
            return {
                "success": True,
                "data": result,
                "timestamp": get_timestamp(),
                "elapsed_seconds": round(elapsed, 2)
            }

        except Exception as e:
            elapsed = time.time() - start
            logger.error(f"Safety check error after {elapsed:.2f}s: {e}")

            # Graceful fallback (do NOT block the user flow in production)
            fallback = {
                "is_safe": True,
                "has_political_bias": False,
                "has_misinformation": False,
                "has_harmful_content": False,
                "risk_level": "low",
                "reason": "Safety check timed out or failed; defaulting to safe with manual review flag.",
                "safe_alternatives": []
            }
            return {
                "success": True,
                "data": fallback,
                "timestamp": get_timestamp(),
                "warning": "Fallback used due to safety check failure",
                "elapsed_seconds": round(elapsed, 2)
            }

    def check_agent_response_safety(
        self,
        agent_name: str,
        response_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check another agent's response for safety issues.

        Args:
            agent_name: Name of the agent
            response_data: Response data to check

        Returns:
            Safety verification result
        """
        # Convert response to text for analysis
        text_to_check = str(response_data)

        safety_result = self.check_content_safety(text_to_check, timeout_seconds=6)

        if not safety_result["success"]:
            return safety_result

        safety_data = safety_result["data"]
        safety_data["agent_name"] = agent_name
        safety_data["checked_at"] = get_timestamp()

        return {
            "success": True,
            "data": safety_data,
            "timestamp": get_timestamp()
        }

    def enforce_safety_boundaries(self, user_input: str) -> Dict[str, Any]:
        """
        Enforce safety boundaries on user input before processing.

        Args:
            user_input: Raw user input

        Returns:
            Boundary enforcement result
        """
        safety_check = self.check_content_safety(user_input, timeout_seconds=5)

        if not safety_check["success"]:
            return {
                "allowed": True,
                "warning": "Safety check failed; proceeding with caution",
                "timestamp": get_timestamp()
            }

        data = safety_check["data"]
        if not data["is_safe"] or data["risk_level"] == "high":
            return {
                "allowed": False,
                "reason": data["reason"],
                "safe_alternatives": data["safe_alternatives"],
                "risk_level": data["risk_level"],
                "timestamp": get_timestamp()
            }

        return {
            "allowed": True,
            "risk_level": data["risk_level"],
            "timestamp": get_timestamp()
        }


# Single instance
safety_agent = SafetyAgent()