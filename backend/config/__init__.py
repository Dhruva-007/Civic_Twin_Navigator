"""
Civic Twin Navigator - Config Package

Contains application configuration:
- settings: Pydantic Settings with environment variable loading
"""

from config.settings import settings

__all__ = [
    "settings",
]