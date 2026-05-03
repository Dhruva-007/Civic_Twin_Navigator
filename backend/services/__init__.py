"""
Civic Twin Navigator - Services Package

Contains Google Cloud service integrations:
- VertexAIService: Gemini 2.5 Flash AI generation
- FirebaseService: Firestore database operations
- AuthService: Firebase Authentication verification
- MapsService: Google Maps Platform integration
- TranslationService: Cloud Translation API
- SpeechService: Text-to-Speech and Speech-to-Text
- BigQueryService: Analytics event logging
"""

from services.vertex_ai_service import vertex_ai_service
from services.firebase_service import firebase_service
from services.auth_service import auth_service
from services.maps_service import maps_service
from services.translation_service import translation_service
from services.speech_service import speech_service
from services.bigquery_service import bigquery_service

__all__ = [
    "vertex_ai_service",
    "firebase_service",
    "auth_service",
    "maps_service",
    "translation_service",
    "speech_service",
    "bigquery_service",
]