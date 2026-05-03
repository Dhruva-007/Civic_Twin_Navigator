import uuid
from datetime import datetime, timezone
from typing import Any, Dict


def generate_id() -> str:
    """Generate unique ID for sessions and profiles"""
    return str(uuid.uuid4())


def get_timestamp() -> str:
    """Get current timestamp in ISO format (timezone-aware)"""
    return datetime.now(timezone.utc).isoformat()


def build_response(
    success: bool,
    data: Any = None,
    message: str = "",
    error: str = ""
) -> Dict:
    """Standard API response builder"""
    return {
        "success": success,
        "timestamp": get_timestamp(),
        "message": message,
        "data": data,
        "error": error
    }


def sanitize_input(text: str) -> str:
    """Basic input sanitization"""
    if not text:
        return ""
    # Remove potential injection patterns
    dangerous = ["<script>", "</script>", "DROP TABLE", "--", ";--"]
    for pattern in dangerous:
        text = text.replace(pattern, "")
    return text.strip()


def calculate_percentage(completed: int, total: int) -> float:
    """Safe percentage calculation"""
    if total == 0:
        return 0.0
    return round((completed / total) * 100, 2)