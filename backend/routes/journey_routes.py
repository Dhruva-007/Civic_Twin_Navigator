from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from agents.journey_planner_agent import journey_planner_agent
from agents.policy_retrieval_agent import policy_retrieval_agent
from agents.evidence_logger_agent import evidence_logger_agent
from services.firebase_service import firebase_service
from services.maps_service import maps_service
from utils.helpers import build_response

# Setup logging
logger = logging.getLogger(__name__)

# Router
router = APIRouter()


# ─────────────────────────────────────────────
# REQUEST MODELS
# ─────────────────────────────────────────────

class CreateJourneyRequest(BaseModel):
    session_id: str


class UpdateStepRequest(BaseModel):
    session_id: str
    phase_id: str
    step_id: str
    is_completed: bool


class PollingStationRequest(BaseModel):
    session_id: str
    user_address: Optional[str] = None


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@router.post("/create")
async def create_journey(request: CreateJourneyRequest):
    """
    Create a personalized election journey for a session.
    """
    try:
        # Get profile
        profile = firebase_service.get_civic_twin(request.session_id)
        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Civic Twin not found. Create profile first."
            )

        # Check if journey already exists
        existing_journey = firebase_service.get_journey(request.session_id)
        if existing_journey:
            return build_response(
                success=True,
                data={"journey": existing_journey},
                message="Journey already exists"
            )

        # Create journey
        journey_result = journey_planner_agent.create_personalized_journey(
            session_id=request.session_id,
            profile=profile
        )

        if not journey_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=journey_result.get("error", "Journey creation failed")
            )

        # Log journey creation
        evidence_logger_agent.log_action(
            session_id=request.session_id,
            action="journey_created",
            details={
                "total_phases": journey_result["data"].get("total_phases"),
                "estimated_days": journey_result["data"].get("estimated_completion_days")
            }
        )

        return build_response(
            success=True,
            data={"journey": journey_result["data"]},
            message="Personalized journey created successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create journey error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}")
async def get_journey(session_id: str):
    """
    Get the full journey for a session.
    """
    try:
        journey = firebase_service.get_journey(session_id)

        if not journey:
            raise HTTPException(
                status_code=404,
                detail="Journey not found. Create journey first."
            )

        return build_response(
            success=True,
            data={"journey": journey},
            message="Journey retrieved successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get journey error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/summary")
async def get_journey_summary(session_id: str):
    """
    Get journey progress summary.
    """
    try:
        summary = journey_planner_agent.get_journey_summary(session_id)

        if not summary["success"]:
            raise HTTPException(
                status_code=404,
                detail="Journey not found"
            )

        return build_response(
            success=True,
            data=summary,
            message="Journey summary retrieved"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get journey summary error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/next-steps")
async def get_next_steps(session_id: str):
    """
    Get next pending steps for the user.
    """
    try:
        next_steps = journey_planner_agent.get_next_steps(session_id)

        if not next_steps["success"]:
            raise HTTPException(
                status_code=404,
                detail="Journey not found"
            )

        return build_response(
            success=True,
            data=next_steps,
            message="Next steps retrieved"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get next steps error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/step/update")
async def update_step(request: UpdateStepRequest):
    """
    Mark a journey step as completed or pending.
    """
    try:
        # Update step
        result = journey_planner_agent.update_step_status(
            session_id=request.session_id,
            phase_id=request.phase_id,
            step_id=request.step_id,
            is_completed=request.is_completed
        )

        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Step update failed")
            )

        # Log step completion
        if request.is_completed:
            evidence_logger_agent.log_action(
                session_id=request.session_id,
                action="step_completed",
                details={
                    "phase_id": request.phase_id,
                    "step_id": request.step_id,
                    "progress": result.get("progress")
                }
            )

        return build_response(
            success=True,
            data={
                "updated": result["updated"],
                "progress": result["progress"]
            },
            message="Step updated successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update step error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/documents")
async def get_document_requirements(session_id: str):
    """
    Get document requirements for the journey.
    """
    try:
        profile = firebase_service.get_civic_twin(session_id)

        docs = policy_retrieval_agent.get_document_requirements(
            user_profile=profile
        )

        return build_response(
            success=True,
            data=docs.get("data", {}),
            message="Document requirements retrieved"
        )

    except Exception as e:
        logger.error(f"Get documents error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/polling-station")
async def find_polling_station(request: PollingStationRequest):
    """
    Find nearest polling stations for the user.
    """
    try:
        profile = firebase_service.get_civic_twin(request.session_id)

        # Get location from profile or request
        location = request.user_address
        if not location and profile:
            location = profile.get("personal_info", {}).get("location", "")

        if not location:
            raise HTTPException(
                status_code=400,
                detail="Location not found. Please provide address."
            )

        # Find polling stations
        stations = maps_service.get_polling_stations(location)

        # Geocode location
        geocoded = maps_service.geocode_location(location)

        return build_response(
            success=True,
            data={
                "location": geocoded,
                "polling_stations": stations,
                "note": "These are government offices near your location. Exact polling booth details are available on voters.eci.gov.in"
            },
            message="Polling stations found"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Find polling station error: {e}")
        raise HTTPException(status_code=500, detail=str(e))