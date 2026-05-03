from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import logging

from services.auth_service import auth_service
from services.firebase_service import firebase_service
from services.bigquery_service import bigquery_service
from utils.helpers import build_response, get_timestamp

logger = logging.getLogger(__name__)

router = APIRouter()


# ─────────────────────────────────────────────
# REQUEST MODELS
# ─────────────────────────────────────────────

class VerifyTokenRequest(BaseModel):
    id_token: str


class LinkSessionRequest(BaseModel):
    session_id: str
    id_token: str


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@router.post("/verify")
async def verify_token(request: VerifyTokenRequest):
    """
    Verify Firebase ID token and return user info.
    Called after frontend login to confirm auth on backend.
    """
    try:
        if not request.id_token:
            raise HTTPException(
                status_code=400,
                detail="ID token is required"
            )

        # Verify token with Firebase Admin
        result = auth_service.verify_token(request.id_token)

        if not result["success"]:
            raise HTTPException(
                status_code=401,
                detail=result.get("error", "Authentication failed")
            )

        user_id = result["user_id"]
        email = result.get("email", "")
        name = result.get("name", "")

        # Save or update user profile in Firestore
        user_profile = {
            "user_id": user_id,
            "email": email,
            "name": name,
            "picture": result.get("picture", ""),
            "email_verified": result.get("email_verified", False),
            "sign_in_provider": result.get("sign_in_provider", "unknown"),
            "last_login": get_timestamp()
        }

        # Check if new user
        existing = firebase_service.db.collection("users").document(user_id).get()
        is_new_user = not existing.exists

        if is_new_user:
            user_profile["created_at"] = get_timestamp()
            user_profile["sessions"] = []

        # Save user profile to Firestore
        firebase_service.db.collection("users").document(user_id).set(
            user_profile,
            merge=True
        )

        # Log to BigQuery analytics (non-critical)
        bigquery_service.log_user_login(
            user_id=user_id,
            sign_in_provider=result.get("sign_in_provider"),
            is_new_user=is_new_user,
        )

        logger.info(
            f"User verified: {user_id} "
            f"({'new' if is_new_user else 'existing'})"
        )

        return build_response(
            success=True,
            data={
                "user_id": user_id,
                "email": email,
                "name": name,
                "is_new_user": is_new_user,
            },
            message="Authentication verified successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Verify token error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/link-session")
async def link_session_to_user(request: LinkSessionRequest):
    """
    Link a Civic Twin session to an authenticated user.
    Called after creating a civic twin when user is logged in.
    """
    try:
        # Verify token
        result = auth_service.verify_token(request.id_token)

        if not result["success"]:
            raise HTTPException(
                status_code=401,
                detail="Authentication failed"
            )

        user_id = result["user_id"]
        session_id = request.session_id

        # Update civic twin with user_id
        firebase_service.db.collection("civic_twins").document(session_id).set(
            {"user_id": user_id, "updated_at": get_timestamp()},
            merge=True
        )

        # Update journey with user_id
        journey = firebase_service.get_journey(session_id)
        if journey:
            firebase_service.db.collection("journeys").document(session_id).set(
                {"user_id": user_id, "updated_at": get_timestamp()},
                merge=True
            )

        # Add session to user's sessions list
        user_ref = firebase_service.db.collection("users").document(user_id)
        user_doc = user_ref.get()

        if user_doc.exists:
            current_sessions = user_doc.to_dict().get("sessions", [])
            if session_id not in current_sessions:
                current_sessions.append(session_id)
                user_ref.update({
                    "sessions": current_sessions,
                    "updated_at": get_timestamp()
                })

        logger.info(f"Session {session_id} linked to user {user_id}")

        return build_response(
            success=True,
            data={
                "session_id": session_id,
                "user_id": user_id,
                "linked": True
            },
            message="Session linked to user successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Link session error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profile/{user_id}")
async def get_user_profile(user_id: str):
    """
    Get user profile and all their sessions.
    """
    try:
        user_doc = firebase_service.db.collection("users").document(user_id).get()

        if not user_doc.exists:
            raise HTTPException(
                status_code=404,
                detail="User profile not found"
            )

        user_data = user_doc.to_dict()
        sessions = user_data.get("sessions", [])

        # Get basic info for each session
        session_summaries = []
        for sid in sessions:
            twin = firebase_service.get_civic_twin(sid)
            if twin:
                session_summaries.append({
                    "session_id": sid,
                    "location": twin.get(
                        "personal_info", {}
                    ).get("location", ""),
                    "voter_status": twin.get(
                        "voter_profile", {}
                    ).get("voter_status", ""),
                    "profile_completeness": twin.get("profile_completeness", 0),
                    "created_at": twin.get("created_at", "")
                })

        return build_response(
            success=True,
            data={
                "user_id": user_id,
                "email": user_data.get("email", ""),
                "name": user_data.get("name", ""),
                "sessions": session_summaries,
                "total_sessions": len(sessions),
                "created_at": user_data.get("created_at", ""),
                "last_login": user_data.get("last_login", "")
            },
            message="User profile retrieved"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get user profile error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{user_id}")
async def get_user_sessions(user_id: str):
    """
    Get all Civic Twin sessions for a user.
    """
    try:
        from google.cloud.firestore_v1.base_query import FieldFilter

        docs = firebase_service.db.collection("civic_twins")\
            .where(filter=FieldFilter("user_id", "==", user_id))\
            .get()

        sessions = []
        for doc in docs:
            data = doc.to_dict()
            sessions.append({
                "session_id": doc.id,
                "location": data.get(
                    "personal_info", {}
                ).get("location", ""),
                "voter_status": data.get(
                    "voter_profile", {}
                ).get("voter_status", ""),
                "profile_completeness": data.get("profile_completeness", 0),
                "created_at": data.get("created_at", ""),
                "updated_at": data.get("updated_at", "")
            })

        # Sort by updated_at descending
        sessions.sort(
            key=lambda x: x.get("updated_at", ""),
            reverse=True
        )

        return build_response(
            success=True,
            data={
                "user_id": user_id,
                "sessions": sessions,
                "total": len(sessions)
            },
            message="User sessions retrieved"
        )

    except Exception as e:
        logger.error(f"Get user sessions error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/logout/{user_id}")
async def logout(user_id: str):
    """
    Handle logout cleanup on backend.
    """
    try:
        # Update last logout time
        firebase_service.db.collection("users").document(user_id).set(
            {"last_logout": get_timestamp()},
            merge=True
        )

        logger.info(f"User logged out: {user_id}")

        return build_response(
            success=True,
            message="Logged out successfully"
        )

    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(status_code=500, detail=str(e))