from typing import Dict, Any, List, Optional
import logging

from services.vertex_ai_service import vertex_ai_service
from services.firebase_service import firebase_service
from utils.helpers import get_timestamp

logger = logging.getLogger(__name__)


class AssessmentAgent:
    """
    Agent 6 – Assessment Agent

    Responsibilities:
    - Calculate overall readiness score
    - Breakdown: legal, document, timeline, poll-day readiness
    - Provide explainable scoring
    - Track score improvement over missions
    """

    SYSTEM_INSTRUCTION = """
    You are the Assessment Agent for Civic Twin Navigator.
    You evaluate voter readiness and provide explainable scores.

    Rules:
    - Use 0-100 scale for all scores
    - Explain each sub-score with reasoning
    - Base scores on user profile, completed steps, and documents
    - Be encouraging but honest
    - Always return valid JSON with no trailing commas
    """

    def calculate_readiness_score(
        self,
        session_id: str,
        profile: Dict[str, Any],
        completed_steps: int = 0,
        total_steps: int = 14
    ) -> Dict[str, Any]:
        """
        Calculate readiness score for a user.

        Args:
            session_id: User session ID
            profile: Civic Twin profile
            completed_steps: Steps already completed
            total_steps: Total steps in journey

        Returns:
            Readiness score with breakdown
        """
        try:
            prompt = f"""
Calculate overall voter readiness score for this Indian voter.

User Profile:
- Age: {profile.get('personal_info', {}).get('age')}
- Location: {profile.get('personal_info', {}).get('location')}
- Voter Status: {profile.get('voter_profile', {}).get('voter_status')}
- Has Aadhar: {profile.get('document_status', {}).get('has_aadhar')}
- Document Concerns: {profile.get('document_status', {}).get('document_concerns')}

Journey Progress:
- Steps Completed: {completed_steps} / {total_steps}
- Profile Completeness: {profile.get('profile_completeness', 0)}%

Return this exact JSON:
{{
  "session_id": "{session_id}",
  "overall_score": 65,
  "scores": {{
    "legal_readiness": {{
      "score": 85,
      "explanation": "User meets age and citizenship requirements. No legal barriers detected.",
      "max_score": 100,
      "status": "good"
    }},
    "document_readiness": {{
      "score": 50,
      "explanation": "Has age proof and Aadhar but missing clear address proof for hostel. Need hostel certificate.",
      "max_score": 100,
      "status": "needs_attention"
    }},
    "timeline_readiness": {{
      "score": 35,
      "explanation": "Journey just started. No registration steps completed yet. Deadline awareness is low.",
      "max_score": 100,
      "status": "needs_improvement"
    }},
    "poll_day_readiness": {{
      "score": 20,
      "explanation": "Not yet registered. Poll day preparation cannot begin until registration is confirmed.",
      "max_score": 100,
      "status": "early_stage"
    }}
  }},
  "overall_status": "needs_improvement",
  "key_improvement_areas": [
    "Arrange hostel address proof (certificate from warden)",
    "Complete Form 6 registration online",
    "Track application after submission"
  ],
  "quick_wins": [
    "Age proof already available",
    "Aadhar card ready for alternate use"
  ],
  "improvement_tips": [
    "Start with document collection – it's your biggest gap",
    "Use Voter Helpline App for easy registration"
  ],
  "generated_at": "{get_timestamp()}"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION,
                temperature=0.3
            )

            # Save score to Firebase
            firebase_service.save_readiness_score(session_id, result)

            return {
                "success": True,
                "data": result,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Calculate readiness score error: {e}")
            # Fallback score
            fallback = {
                "session_id": session_id,
                "overall_score": 50,
                "scores": {
                    "legal_readiness": {"score": 80, "status": "good"},
                    "document_readiness": {"score": 40, "status": "needs_attention"},
                    "timeline_readiness": {"score": 30, "status": "needs_improvement"},
                    "poll_day_readiness": {"score": 0, "status": "early_stage"}
                },
                "overall_status": "needs_improvement"
            }
            return {
                "success": True,
                "data": fallback,
                "timestamp": get_timestamp()
            }

    def calculate_mission_score(
        self,
        mission_results: List[Dict]
    ) -> Dict[str, Any]:
        """
        Calculate score from completed mission questions.

        Args:
            mission_results: List of {question_id, is_correct, points_earned}

        Returns:
            Mission score summary
        """
        try:
            total = len(mission_results)
            correct = sum(1 for r in mission_results if r.get("is_correct"))
            points = sum(r.get("points_earned", 0) for r in mission_results)

            return {
                "success": True,
                "data": {
                    "total_questions": total,
                    "correct_answers": correct,
                    "score_percentage": round((correct / total) * 100, 1) if total > 0 else 0,
                    "points_earned": points,
                    "performance": "excellent" if correct == total else ("good" if correct >= total/2 else "needs_review"),
                    "suggestions": ["Review mission content for missed questions"] if correct < total else []
                },
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Mission score error: {e}")
            return {"success": False, "error": str(e)}

    def get_proof_of_readiness(
        self,
        session_id: str,
        profile: Dict[str, Any],
        journey: Dict[str, Any],
        score: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate 'Proof of Readiness' document.

        Args:
            session_id: Session ID
            profile: Civic Twin profile
            journey: Journey data
            score: Readiness score

        Returns:
            Readiness certificate summary
        """
        try:
            prompt = f"""
Generate a 'Proof of Readiness' summary for this voter.

Session: {session_id}
Profile: {profile}
Journey: {journey}
Score: {score}

Return this exact JSON:
{{
  "certificate_id": "READY-{session_id[:8]}",
  "generated_for": "voter at {profile.get('personal_info', {}).get('location')}",
  "readiness_summary": {{
    "overall_score": score.get('overall_score', 0),
    "status": score.get('overall_status', 'unknown'),
    "completed_steps": journey.get('completed_steps', 0),
    "total_steps": journey.get('total_steps', 0)
  }},
  "verified_areas": [
    "Legal eligibility check passed",
    "Age proof verified",
    "Aadhar card present"
  ],
  "pending_actions": [
    "Arrange hostel address proof",
    "Submit Form 6 online"
  ],
  "confidence_level": "moderate",
  "issued_at": "{get_timestamp()}",
  "official_references": ["voters.eci.gov.in", "1950 helpline"]
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION,
                temperature=0.3
            )

            return {
                "success": True,
                "data": result,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Proof of readiness error: {e}")
            return {"success": False, "error": str(e)}


assessment_agent = AssessmentAgent()