from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from agents.simulation_agent import simulation_agent
from agents.accessibility_agent import accessibility_agent
from agents.evidence_logger_agent import evidence_logger_agent
from services.firebase_service import firebase_service
from services.bigquery_service import bigquery_service
from utils.helpers import build_response
from utils.validators import validate_scenario_input

# Setup logging
logger = logging.getLogger(__name__)

# Router
router = APIRouter()


# ─────────────────────────────────────────────
# REQUEST MODELS
# ─────────────────────────────────────────────

class StartMissionRequest(BaseModel):
    session_id: str
    mission_number: int


class AnswerRequest(BaseModel):
    session_id: str
    mission_id: str
    question_id: str
    user_answer: str
    correct_answer: str
    explanation: str


class ScenarioRequest(BaseModel):
    session_id: str
    scenario: str


class PollDayRequest(BaseModel):
    session_id: str


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@router.post("/start")
async def start_mission(request: StartMissionRequest):
    """
    Start an interactive mission for the user.
    Mission numbers: 1 to 5
    """
    try:
        # Validate mission number
        if request.mission_number < 1 or request.mission_number > 5:
            raise HTTPException(
                status_code=400,
                detail="Mission number must be between 1 and 5"
            )

        # Get profile
        profile = firebase_service.get_civic_twin(request.session_id)
        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Civic Twin not found. Create profile first."
            )

        # Generate mission
        mission_result = simulation_agent.generate_mission(
            mission_number=request.mission_number,
            profile=profile
        )

        if not mission_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=mission_result.get("error", "Mission generation failed")
            )

        mission_data = mission_result["data"]
        mission_id = mission_data.get(
            "mission_id", f"mission_{request.mission_number}"
        )

        # Save mission progress to Firebase
        firebase_service.save_mission_progress(
            session_id=request.session_id,
            mission_id=mission_id,
            progress_data={
                "status": "started",
                "mission_number": request.mission_number,
                "total_questions": len(mission_data.get("questions", [])),
                "answered_questions": 0,
                "score": 0
            }
        )

        # Log mission start
        evidence_logger_agent.log_action(
            session_id=request.session_id,
            action="mission_started",
            details={
                "mission_number": request.mission_number,
                "mission_id": mission_id
            }
        )

        return build_response(
            success=True,
            data={"mission": mission_data},
            message=f"Mission {request.mission_number} started successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Start mission error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/answer")
async def submit_answer(request: AnswerRequest):
    """
    Submit an answer for a mission question.
    """
    try:
        # Check answer
        answer_result = simulation_agent.check_answer(
            question_id=request.question_id,
            user_answer=request.user_answer,
            correct_answer=request.correct_answer,
            explanation=request.explanation
        )

        if not answer_result["success"]:
            raise HTTPException(
                status_code=500,
                detail="Answer check failed"
            )

        answer_data = answer_result["data"]

        # Update mission progress
        existing_progress = firebase_service.get_mission_progress(
            session_id=request.session_id,
            mission_id=request.mission_id
        )

        if existing_progress:
            answered = existing_progress.get("answered_questions", 0) + 1
            current_score = existing_progress.get("score", 0)
            new_score = current_score + answer_data.get("points_earned", 0)

            firebase_service.save_mission_progress(
                session_id=request.session_id,
                mission_id=request.mission_id,
                progress_data={
                    "answered_questions": answered,
                    "score": new_score,
                    "last_answered": request.question_id
                }
            )

        # Log answer
        evidence_logger_agent.log_action(
            session_id=request.session_id,
            action="question_answered",
            details={
                "mission_id": request.mission_id,
                "question_id": request.question_id,
                "is_correct": answer_data.get("is_correct"),
                "points": answer_data.get("points_earned")
            }
        )

        return build_response(
            success=True,
            data={"result": answer_data},
            message="Answer submitted successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Submit answer error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scenario")
async def run_scenario(request: ScenarioRequest):
    """
    Run a what-if scenario simulation.
    """
    try:
        # Validate scenario input length and content
        is_valid, error_msg = validate_scenario_input(request.scenario)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        # Get profile
        profile = firebase_service.get_civic_twin(request.session_id)
        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Civic Twin not found"
            )

        # Run scenario
        scenario_result = simulation_agent.run_what_if_scenario(
            scenario=request.scenario,
            profile=profile
        )

        if not scenario_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=scenario_result.get("error", "Scenario failed")
            )

        # Log scenario to Firebase
        evidence_logger_agent.log_action(
            session_id=request.session_id,
            action="scenario_run",
            details={"scenario": request.scenario[:100]}
        )

        # Log to BigQuery analytics (non-critical)
        scenario_data = scenario_result["data"]
        bigquery_service.log_scenario_run(
            session_id=request.session_id,
            scenario_type=scenario_data.get("scenario_type"),
            is_recoverable=scenario_data.get("is_recoverable"),
            user_id=profile.get("user_id"),
        )

        return build_response(
            success=True,
            data={"scenario": scenario_data},
            message="Scenario simulation completed"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Run scenario error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/poll-day-simulation")
async def simulate_poll_day(request: PollDayRequest):
    """
    Run a complete poll day simulation.
    """
    try:
        # Get profile
        profile = firebase_service.get_civic_twin(request.session_id)
        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Civic Twin not found"
            )

        # Run simulation
        poll_result = simulation_agent.simulate_poll_day(profile)

        if not poll_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=poll_result.get("error", "Poll day simulation failed")
            )

        # Log simulation
        evidence_logger_agent.log_action(
            session_id=request.session_id,
            action="poll_day_simulated",
            details={
                "location": profile.get(
                    "personal_info", {}
                ).get("location")
            }
        )

        return build_response(
            success=True,
            data={"simulation": poll_result["data"]},
            message="Poll day simulation completed"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Poll day simulation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/progress")
async def get_mission_progress(session_id: str):
    """
    Get all mission progress for a session.
    """
    try:
        all_progress = firebase_service.get_all_missions_progress(session_id)

        total_missions = 5
        completed = len([
            p for p in all_progress
            if p.get("status") == "completed"
        ])

        return build_response(
            success=True,
            data={
                "session_id": session_id,
                "total_missions": total_missions,
                "completed_missions": completed,
                "progress_percentage": round(
                    (completed / total_missions) * 100, 1
                ),
                "missions": all_progress
            },
            message="Mission progress retrieved"
        )

    except Exception as e:
        logger.error(f"Get mission progress error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{session_id}/complete/{mission_id}")
async def complete_mission(session_id: str, mission_id: str):
    """
    Mark a mission as fully completed.
    """
    try:
        # Get profile for BigQuery logging
        profile = firebase_service.get_civic_twin(session_id)

        # Update mission status
        firebase_service.save_mission_progress(
            session_id=session_id,
            mission_id=mission_id,
            progress_data={"status": "completed"}
        )

        # Log completion to Firebase
        evidence_logger_agent.log_action(
            session_id=session_id,
            action="mission_completed",
            details={"mission_id": mission_id}
        )

        # Extract mission number from mission_id (e.g. "mission_1" -> 1)
        try:
            mission_number = int(mission_id.split("_")[-1])
        except (ValueError, IndexError):
            mission_number = None

        # Get mission progress for score
        progress = firebase_service.get_mission_progress(
            session_id=session_id,
            mission_id=mission_id
        )
        mission_score = progress.get("score", 0) if progress else None

        # Log to BigQuery analytics (non-critical)
        bigquery_service.log_mission_completed(
            session_id=session_id,
            mission_number=mission_number,
            score=mission_score,
            user_id=profile.get("user_id") if profile else None,
        )

        return build_response(
            success=True,
            data={"mission_id": mission_id, "status": "completed"},
            message="Mission completed successfully"
        )

    except Exception as e:
        logger.error(f"Complete mission error: {e}")
        raise HTTPException(status_code=500, detail=str(e))