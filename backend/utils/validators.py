from typing import Optional
import re


def validate_location(location: str) -> bool:
    """Validate location input"""
    if not location or len(location) < 2:
        return False
    if len(location) > 100:
        return False
    return True


def validate_age(age: int) -> bool:
    """Validate voter age eligibility"""
    return 18 <= age <= 120


def validate_language(language: str) -> bool:
    """Validate supported language codes"""
    supported = [
        "en", "hi", "mr", "ta", "te",
        "kn", "ml", "gu", "bn", "pa"
    ]
    return language.lower() in supported


def validate_user_input(text: str) -> tuple[bool, str]:
    """
    Validate free text user input.
    Returns (is_valid, error_message)
    """
    if not text:
        return False, "Input cannot be empty"
    if len(text) < 3:
        return False, "Input too short"
    if len(text) > 2000:
        return False, "Input too long. Maximum 2000 characters allowed."
    return True, ""


def validate_session_id(session_id: str) -> bool:
    """Validate UUID format session ID"""
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
    return bool(re.match(pattern, session_id, re.IGNORECASE))


def validate_translation_text(text: str) -> tuple[bool, str]:
    """
    Validate text for translation endpoint.
    Returns (is_valid, error_message)
    """
    if not text or not text.strip():
        return False, "Text cannot be empty"
    if len(text) > 5000:
        return False, "Text too long. Maximum 5000 characters allowed for translation."
    return True, ""


def validate_translation_batch(texts: list) -> tuple[bool, str]:
    """
    Validate batch texts for translation endpoint.
    Returns (is_valid, error_message)
    """
    if not texts:
        return False, "Texts list cannot be empty"
    if len(texts) > 50:
        return False, "Too many texts. Maximum 50 texts per batch."
    total_chars = sum(len(t) for t in texts)
    if total_chars > 10000:
        return False, "Total text too long. Maximum 10000 characters per batch."
    return True, ""


def validate_scenario_input(scenario: str) -> tuple[bool, str]:
    """
    Validate what-if scenario input.
    Returns (is_valid, error_message)
    """
    if not scenario or not scenario.strip():
        return False, "Scenario cannot be empty"
    if len(scenario) < 5:
        return False, "Scenario too short"
    if len(scenario) > 500:
        return False, "Scenario too long. Maximum 500 characters allowed."
    return True, ""


def validate_query_input(query: str) -> tuple[bool, str]:
    """
    Validate election query input.
    Returns (is_valid, error_message)
    """
    if not query or not query.strip():
        return False, "Query cannot be empty"
    if len(query) < 3:
        return False, "Query too short"
    if len(query) > 1000:
        return False, "Query too long. Maximum 1000 characters allowed."
    return True, ""