from fastapi import Request
from fastapi.responses import JSONResponse
from collections import defaultdict
import time
import threading

from config.settings import settings


class RateLimiter:
    """
    Simple in-memory rate limiter.
    Limits requests per IP per minute.
    """

    def __init__(self):
        self._requests: dict = defaultdict(list)
        self._lock = threading.Lock()

    def is_allowed(
        self,
        client_ip: str,
        max_requests: int = None,
        window_seconds: int = 60
    ) -> bool:
        """
        Check if request is allowed for this IP.

        Args:
            client_ip: Client IP address
            max_requests: Max requests per window
            window_seconds: Time window in seconds

        Returns:
            True if allowed, False if rate limited
        """
        max_req = max_requests or settings.max_requests_per_minute
        now = time.time()

        with self._lock:
            # Clean old requests outside window
            self._requests[client_ip] = [
                req_time for req_time in self._requests[client_ip]
                if now - req_time < window_seconds
            ]

            # Check if under limit
            if len(self._requests[client_ip]) < max_req:
                self._requests[client_ip].append(now)
                return True

            return False

    def get_retry_after(
        self,
        client_ip: str,
        window_seconds: int = 60
    ) -> int:
        """Get seconds until rate limit resets"""
        with self._lock:
            if not self._requests[client_ip]:
                return 0
            oldest = min(self._requests[client_ip])
            retry_after = int(window_seconds - (time.time() - oldest))
            return max(0, retry_after)

    def clear(self, client_ip: str = None):
        """Clear rate limit for IP or all"""
        with self._lock:
            if client_ip:
                self._requests.pop(client_ip, None)
            else:
                self._requests.clear()


# Single instance
rate_limiter = RateLimiter()


async def rate_limit_middleware(request: Request, call_next):
    """
    FastAPI middleware for rate limiting.
    Returns JSONResponse instead of raising HTTPException
    to avoid ASGI middleware exception group errors.
    """

    # ── Paths that skip rate limiting entirely ──
    skip_paths = [
        "/",
        "/health",
        "/docs",
        "/openapi.json",
        "/redoc",
    ]

    # ── Paths with higher rate limits (translation calls) ──
    high_limit_prefixes = [
        "/api/translate",
    ]

    path = request.url.path

    # Skip rate limiting for exempt paths
    if path in skip_paths:
        return await call_next(request)

    # Also skip OPTIONS preflight requests (CORS)
    if request.method == "OPTIONS":
        return await call_next(request)

    # Get client IP
    client_ip = "unknown"
    if request.client:
        client_ip = request.client.host

    # Check forwarded IP (behind proxy)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()

    # Determine rate limit based on path
    is_high_limit = any(path.startswith(prefix) for prefix in high_limit_prefixes)

    if is_high_limit:
        # Translation endpoints get 300 requests per minute
        max_requests = 300
        bucket_key = f"{client_ip}:translate"
    else:
        # All other endpoints use standard limit
        max_requests = settings.max_requests_per_minute
        bucket_key = client_ip

    # Check rate limit - return JSONResponse instead of raising
    if not rate_limiter.is_allowed(bucket_key, max_requests):
        retry_after = rate_limiter.get_retry_after(bucket_key)
        return JSONResponse(
            status_code=429,
            content={
                "success": False,
                "error": "Too many requests",
                "message": "Rate limit exceeded. Please slow down.",
                "retry_after_seconds": retry_after
            },
            headers={
                "Retry-After": str(retry_after),
                "X-RateLimit-Limit": str(max_requests),
            }
        )

    return await call_next(request)