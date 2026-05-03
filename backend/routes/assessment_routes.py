from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging

from agents.assessment_agent import assessment_agent
from agents.prediction_agent import prediction_agent
from agents.evidence_logger_agent import evidence_logger_agent
from services.firebase_service import firebase_service
from services.bigquery_service import bigquery_service
from utils.helpers import build_response

# Setup logging
logger = logging.getLogger(__name__)

# Router
router = APIRouter()


# ─────────────────────────────────────────────
# REQUEST MODELS
# ─────────────────────────────────────────────

class ReadinessRequest(BaseModel):
    session_id: str


class MissionScoreRequest(BaseModel):
    session_id: str
    mission_results: List[Dict[str, Any]]


class ProofRequest(BaseModel):
    session_id: str


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@router.post("/readiness")
async def calculate_readiness(request: ReadinessRequest):
    """
    Calculate overall readiness score for a user.
    """
    try:
        # Get profile
        profile = firebase_service.get_civic_twin(request.session_id)
        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Civic Twin not found"
            )

        # Get journey progress
        journey = firebase_service.get_journey(request.session_id)
        completed_steps = 0
        total_steps = 14

        if journey:
            phases = journey.get("phases", [])
            completed_steps = sum(
                len([s for s in p.get("steps", []) if s.get("is_completed")])
                for p in phases
            )
            total_steps = sum(
                len(p.get("steps", [])) for p in phases
            )

        # Calculate score
        score_result = assessment_agent.calculate_readiness_score(
            session_id=request.session_id,
            profile=profile,
            completed_steps=completed_steps,
            total_steps=total_steps
        )

        if not score_result["success"]:
            raise HTTPException(
                status_code=500,
                detail="Score calculation failed"
            )

        # Get predictions
        prediction_result = prediction_agent.predict_failure_risks(
            profile=profile,
            journey=journey
        )

        # Log assessment
        evidence_logger_agent.log_agent_response(
            session_id=request.session_id,
            agent_name="assessment_agent",
            response_data=score_result["data"],
            sources=["Election Commission of India - eci.gov.in"]
        )

        # Log to BigQuery analytics (non-critical)
        overall_score = score_result["data"].get("overall_score", 0)
        bigquery_service.log_readiness_assessed(
            session_id=request.session_id,
            overall_score=overall_score,
            location=profile.get("personal_info", {}).get("location"),
            voter_status=profile.get("voter_profile", {}).get("voter_status"),
            user_id=profile.get("user_id"),
        )

        return build_response(
            success=True,
            data={
                "readiness_score": score_result["data"],
                "predictions": prediction_result.get("data", {}),
                "journey_progress": {
                    "completed_steps": completed_steps,
                    "total_steps": total_steps,
                    "percentage": round(
                        (completed_steps / total_steps) * 100, 1
                    ) if total_steps > 0 else 0
                }
            },
            message="Readiness assessment completed"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Calculate readiness error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/score")
async def get_readiness_score(session_id: str):
    """
    Get the latest saved readiness score.
    """
    try:
        score = firebase_service.get_readiness_score(session_id)

        if not score:
            raise HTTPException(
                status_code=404,
                detail="No readiness score found. Run assessment first."
            )

        return build_response(
            success=True,
            data={"score": score},
            message="Readiness score retrieved"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get score error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mission-score")
async def calculate_mission_score(request: MissionScoreRequest):
    """
    Calculate score from completed mission questions.
    """
    try:
        score_result = assessment_agent.calculate_mission_score(
            mission_results=request.mission_results
        )

        if not score_result["success"]:
            raise HTTPException(
                status_code=500,
                detail="Mission score calculation failed"
            )

        # Log mission score
        evidence_logger_agent.log_action(
            session_id=request.session_id,
            action="mission_score_calculated",
            details={
                "score": score_result["data"].get("score_percentage"),
                "correct": score_result["data"].get("correct_answers")
            }
        )

        return build_response(
            success=True,
            data=score_result["data"],
            message="Mission score calculated"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Mission score error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/proof-of-readiness")
async def generate_proof_of_readiness(request: ProofRequest):
    """
    Generate Proof of Readiness certificate.
    """
    try:
        # Get all required data
        profile = firebase_service.get_civic_twin(request.session_id)
        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Civic Twin not found"
            )

        journey = firebase_service.get_journey(request.session_id)
        score = firebase_service.get_readiness_score(request.session_id)

        # Build journey summary for proof
        journey_summary = {}
        if journey:
            phases = journey.get("phases", [])
            completed_steps = sum(
                len([s for s in p.get("steps", []) if s.get("is_completed")])
                for p in phases
            )
            total_steps = sum(len(p.get("steps", [])) for p in phases)
            journey_summary = {
                "completed_steps": completed_steps,
                "total_steps": total_steps
            }

        # Generate proof
        proof_result = assessment_agent.get_proof_of_readiness(
            session_id=request.session_id,
            profile=profile,
            journey=journey_summary,
            score=score or {}
        )

        if not proof_result["success"]:
            raise HTTPException(
                status_code=500,
                detail="Proof generation failed"
            )

        # Log proof generation
        evidence_logger_agent.log_readiness_proof(
            session_id=request.session_id,
            proof_data=proof_result["data"]
        )

        # Log to BigQuery analytics (non-critical)
        bigquery_service.log_proof_generated(
            session_id=request.session_id,
            certificate_id=proof_result["data"].get("certificate_id"),
            confidence_level=proof_result["data"].get("confidence_level"),
            user_id=profile.get("user_id"),
        )

        return build_response(
            success=True,
            data={"proof": proof_result["data"]},
            message="Proof of Readiness generated successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Generate proof error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/predictions")
async def get_predictions(session_id: str):
    """
    Get failure risk predictions for a user.
    """
    try:
        profile = firebase_service.get_civic_twin(session_id)
        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Civic Twin not found"
            )

        prediction_result = prediction_agent.predict_failure_risks(
            profile=profile
        )

        return build_response(
            success=True,
            data=prediction_result.get("data", {}),
            message="Predictions generated"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get predictions error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/logs")
async def get_session_logs(session_id: str):
    """
    Get all evidence logs for a session.
    """
    try:
        logs_result = evidence_logger_agent.get_session_logs(
            session_id=session_id,
            limit=20
        )

        return build_response(
            success=True,
            data=logs_result,
            message="Session logs retrieved"
        )

    except Exception as e:
        logger.error(f"Get logs error: {e}")
        raise HTTPException(status_code=500, detail=str(e))