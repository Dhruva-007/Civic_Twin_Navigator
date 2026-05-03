from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Google Cloud
    google_cloud_project_id: str
    google_cloud_location: str = "us-central1"

    # Vertex AI
    vertex_ai_model: str = "gemini-2.5-flash"
    vertex_ai_max_tokens: int = 2048
    vertex_ai_temperature: float = 0.7

    # Google Maps
    google_maps_api_key: str

    # Firebase
    firebase_project_id: str

    # App
    app_name: str = "Civic Twin Navigator"
    app_version: str = "1.0.0"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = True

    # CORS
    frontend_url: str = "http://localhost:5173"

    # Safety
    max_requests_per_minute: int = 60

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


# Single instance to use everywhere
settings = Settings()