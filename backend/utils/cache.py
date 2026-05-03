"""
Simple in-memory response cache for Civic Twin Navigator.
Caches static or semi-static responses to reduce API calls
and improve response times for repeated requests.
"""
import time
import threading
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)


class SimpleCache:
    """
    Thread-safe in-memory cache with TTL expiration.

    Used for caching:
    - Policy data (eligibility rules, document requirements)
    - Translation results
    - Safety check results
    """

    def __init__(self):
        self._cache: dict = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        """
        Get cached value by key.

        Args:
            key: Cache key string

        Returns:
            Cached value or None if expired or missing
        """
        with self._lock:
            entry = self._cache.get(key)
            if not entry:
                return None

            # Check TTL expiration
            if time.time() > entry["expires_at"]:
                del self._cache[key]
                return None

            return entry["value"]

    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        """
        Set cached value with TTL.

        Args:
            key: Cache key string
            value: Value to cache
            ttl_seconds: Time to live in seconds (default 5 minutes)
        """
        with self._lock:
            self._cache[key] = {
                "value": value,
                "expires_at": time.time() + ttl_seconds,
                "cached_at": time.time()
            }

    def delete(self, key: str) -> None:
        """
        Delete cached value by key.

        Args:
            key: Cache key string
        """
        with self._lock:
            self._cache.pop(key, None)

    def clear(self) -> None:
        """Clear all cached values."""
        with self._lock:
            self._cache.clear()
            logger.info("Cache cleared completely")

    def cleanup_expired(self) -> int:
        """
        Remove all expired entries from cache.

        Returns:
            Number of entries removed
        """
        now = time.time()
        removed = 0
        with self._lock:
            expired_keys = [
                k for k, v in self._cache.items()
                if now > v["expires_at"]
            ]
            for key in expired_keys:
                del self._cache[key]
                removed += 1
        if removed:
            logger.info(f"Cache cleanup: removed {removed} expired entries")
        return removed

    def stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        with self._lock:
            now = time.time()
            active = sum(
                1 for v in self._cache.values()
                if now <= v["expires_at"]
            )
            return {
                "total_entries": len(self._cache),
                "active_entries": active,
                "expired_entries": len(self._cache) - active,
            }


# Single global instance used across all services
response_cache = SimpleCache()