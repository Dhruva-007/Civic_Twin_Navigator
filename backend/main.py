from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager
import uvicorn
import logging
import time

from config.settings import settings
from routes.twin_routes import router as twin_router
from routes.journey_routes import router as journey_router
from routes.mission_routes import router as mission_router
from routes.assessment_routes import router as assessment_router
from routes.translate_routes import router as translate_router
from routes.auth_routes import router as auth_router
from utils.rate_limiter import rate_limit_middleware
from utils.cache import response_cache

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Project: {settings.google_cloud_project_id}")
    logger.info(f"Location: {settings.google_cloud_location}")
    logger.info(f"Model: {settings.vertex_ai_model}")
    logger.info("Response cache initialized")
    yield
    # Shutdown
    removed = response_cache.cleanup_expired()
    logger.info(f"Cache cleanup on shutdown: {removed} entries removed")
    logger.info("Shutting down Civic Twin Navigator")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered election learning and readiness assistant",
    lifespan=lifespan
)

# ─────────────────────────────────────────────
# MIDDLEWARE
# ─────────────────────────────────────────────

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting
app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limit_middleware)


# Request Body Size Limit Middleware
@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    """
    Limit request body size to 1MB.
    Prevents large payload attacks.
    """
    max_body_size = 1_048_576  # 1MB in bytes
    content_length = request.headers.get("content-length")

    if content_length and int(content_length) > max_body_size:
        return JSONResponse(
            status_code=413,
            content={
                "success": False,
                "error": "Request too large",
                "message": "Request body must be less than 1MB"
            }
        )
    return await call_next(request)


# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """
    Add comprehensive security headers to all responses.
    Protects against XSS, clickjacking, MIME sniffing,
    and other common web vulnerabilities.
    """
    start_time = time.time()
    response = await call_next(request)

    # Prevent MIME type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"

    # Prevent clickjacking
    response.headers["X-Frame-Options"] = "DENY"

    # XSS Protection (legacy browsers)
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # Referrer policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # Permissions policy - only allow microphone for voice feature
    response.headers["Permissions-Policy"] = "microphone=self"

    # Content Security Policy
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://apis.google.com "
        "https://*.firebaseapp.com https://*.googleapis.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https: blob:; "
        "connect-src 'self' https://*.googleapis.com "
        "https://*.firebaseapp.com https://*.firebaseio.com "
        "wss://*.firebaseio.com; "
        "frame-src https://*.firebaseapp.com https://accounts.google.com"
    )

    # Performance tracking header
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 4))

    return response


# ─────────────────────────────────────────────
# EXCEPTION HANDLERS
# ─────────────────────────────────────────────

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "Something went wrong"
        }
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "Route not found",
            "path": str(request.url.path)
        }
    )


# ─────────────────────────────────────────────
# HEALTH ROUTES
# ─────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "success": True,
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {
        "success": True,
        "status": "healthy",
        "project": settings.google_cloud_project_id,
        "model": settings.vertex_ai_model,
        "location": settings.google_cloud_location
    }


# ─────────────────────────────────────────────
# ROUTERS
# ─────────────────────────────────────────────

app.include_router(twin_router, prefix="/api/twin", tags=["Civic Twin"])
app.include_router(journey_router, prefix="/api/journey", tags=["Journey"])
app.include_router(mission_router, prefix="/api/mission", tags=["Mission"])
app.include_router(assessment_router, prefix="/api/assessment", tags=["Assessment"])
app.include_router(translate_router, prefix="/api/translate", tags=["Translation"])
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])


# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug
    )