from fastapi import APIRouter, HTTPException, Body
from models.civic_twin import (
    CivicTwinCreateRequest,
    CivicTwinQueryRequest,
    CivicTwinUpdateRequest,
)
from typing import Optional, Dict, Any
import logging

from agents.intent_context_agent import intent_context_agent
from agents.policy_retrieval_agent import policy_retrieval_agent
from agents.consistency_verification_agent import consistency_verification_agent
from agents.safety_agent import safety_agent
from agents.evidence_logger_agent import evidence_logger_agent
from services.firebase_service import firebase_service
from services.bigquery_service import bigquery_service
from utils.helpers import build_response, get_timestamp
from utils.validators import validate_user_input, validate_query_input

# Setup logging
logger = logging.getLogger(__name__)

# Router
router = APIRouter()


# ─────────────────────────────────────────────
# REQUEST MODELS
# ─────────────────────────────────────────────



# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@router.post("/create")
async def create_civic_twin(request: CivicTwinCreateRequest):
    """
    Create a new Civic Twin profile from user input.
    This is the entry point of the entire journey.
    """
    try:
        # Validate input
        is_valid, error_msg = validate_user_input(request.user_input)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        # Safety check on input
        safety_result = safety_agent.check_content_safety(request.user_input)
        if safety_result.get("data", {}).get("risk_level") == "high":
            raise HTTPException(
                status_code=400,
                detail="Input contains unsafe content. Please rephrase."
            )

        # Build Civic Twin profile
        profile_result = intent_context_agent.build_civic_twin_profile(
            user_input=request.user_input
        )

        if not profile_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=profile_result.get("error", "Failed to create profile")
            )

        session_id = profile_result["session_id"]
        profile = profile_result["profile"]

        # Verify profile consistency
        verification = consistency_verification_agent.verify_civic_twin_profile(
            profile=profile
        )

        # Log creation event to Firebase
        evidence_logger_agent.log_action(
            session_id=session_id,
            action="civic_twin_created",
            details={
                "location": profile.get("personal_info", {}).get("location"),
                "voter_status": profile.get("voter_profile", {}).get("voter_status"),
                "profile_completeness": profile.get("profile_completeness")
            }
        )

        # Log to BigQuery analytics (non-critical)
        bigquery_service.log_civic_twin_created(
            session_id=session_id,
            location=profile.get("personal_info", {}).get("location"),
            language=request.language,
            voter_status=profile.get("voter_profile", {}).get("voter_status"),
        )

        return build_response(
            success=True,
            data={
                "session_id": session_id,
                "profile": profile,
                "verification": verification.get("data", {}),
                "requires_clarification": profile.get(
                    "profile_completeness", 100
                ) < 60
            },
            message="Civic Twin profile created successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create civic twin error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}")
async def get_civic_twin(session_id: str):
    """
    Get an existing Civic Twin profile by session ID.
    """
    try:
        profile = firebase_service.get_civic_twin(session_id)

        if not profile:
            raise HTTPException(
                status_code=404,
                detail=f"Civic Twin not found for session: {session_id}"
            )

        return build_response(
            success=True,
            data={"profile": profile},
            message="Civic Twin retrieved successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get civic twin error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update")
async def update_civic_twin(request: CivicTwinUpdateRequest):
    """
    Update existing Civic Twin profile with new information.
    """
    try:
        # Validate input
        is_valid, error_msg = validate_user_input(request.new_input)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        # Check session exists
        existing = firebase_service.get_civic_twin(request.session_id)
        if not existing:
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )

        # Update profile
        update_result = intent_context_agent.update_civic_twin_profile(
            session_id=request.session_id,
            new_input=request.new_input
        )

        if not update_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=update_result.get("error", "Update failed")
            )

        # Log update
        evidence_logger_agent.log_action(
            session_id=request.session_id,
            action="civic_twin_updated",
            details={"new_input_length": len(request.new_input)}
        )

        return build_response(
            success=True,
            data={"profile": update_result["profile"]},
            message="Civic Twin profile updated successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update civic twin error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query")
async def answer_query(request: CivicTwinQueryRequest):
    """
    Answer a specific election query with optional session context.
    """
    try:
        # Validate query length
        is_valid, error_msg = validate_query_input(request.query)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        # Safety check
        safety_result = safety_agent.check_content_safety(request.query)
        if safety_result.get("data", {}).get("risk_level") == "high":
            raise HTTPException(
                status_code=400,
                detail="Query contains unsafe content"
            )

        # Get profile if session provided
        profile = None
        if request.session_id:
            profile = firebase_service.get_civic_twin(request.session_id)

        # Analyze intent
        intent_result = intent_context_agent.analyze_user_input(
            user_input=request.query,
            session_id=request.session_id,
            existing_profile=profile
        )

        # Get policy answer
        answer_result = policy_retrieval_agent.answer_specific_query(
            query=request.query,
            user_profile=profile
        )

        # Log query
        if request.session_id:
            evidence_logger_agent.log_action(
                session_id=request.session_id,
                action="query_answered",
                details={"query": request.query[:100]}
            )
            firebase_service.save_message(
                request.session_id, "user", request.query
            )

        return build_response(
            success=True,
            data={
                "intent": intent_result.get("analysis", {}).get("intent"),
                "answer": answer_result.get("data", {}),
                "source": answer_result.get("source")
            },
            message="Query answered successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Answer query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/eligibility")
async def check_eligibility(session_id: str):
    """
    Check voter eligibility for a session.
    """
    try:
        profile = firebase_service.get_civic_twin(session_id)

        if not profile:
            raise HTTPException(status_code=404, detail="Session not found")

        # Get eligibility rules
        eligibility = policy_retrieval_agent.get_eligibility_rules(
            user_profile=profile
        )

        # Cross check
        if eligibility["success"]:
            cross_check = consistency_verification_agent.cross_check_eligibility(
                profile=profile,
                eligibility_rules=eligibility.get("data", {})
            )
        else:
            cross_check = {"success": False}

        return build_response(
            success=True,
            data={
                "eligibility_rules": eligibility.get("data", {}),
                "cross_check": cross_check.get("data", {}),
                "source": "Election Commission of India"
            },
            message="Eligibility check completed"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Check eligibility error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{session_id}")
async def delete_civic_twin(session_id: str):
    """
    Delete a Civic Twin session and all associated data.
    """
    try:
        deleted = firebase_service.delete_session(session_id)

        return build_response(
            success=deleted,
            message="Session deleted successfully" if deleted else "Delete failed"
        )

    except Exception as e:
        logger.error(f"Delete civic twin error: {e}")
        raise HTTPException(status_code=500, detail=str(e))