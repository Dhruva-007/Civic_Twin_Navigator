"""
Civic Twin Navigator - Routes Package

Contains FastAPI route handlers:
- twin_routes: Civic Twin profile management
- journey_routes: Election journey planning
- mission_routes: Interactive missions and scenarios
- assessment_routes: Readiness scoring and proof
- translate_routes: Multilingual translation
- auth_routes: Firebase Authentication
"""

from routes.twin_routes import router as twin_router
from routes.journey_routes import router as journey_router
from routes.mission_routes import router as mission_router
from routes.assessment_routes import router as assessment_router
from routes.translate_routes import router as translate_router
from routes.auth_routes import router as auth_router

__all__ = [
    "twin_router",
    "journey_router",
    "mission_router",
    "assessment_router",
    "translate_router",
    "auth_router",
]