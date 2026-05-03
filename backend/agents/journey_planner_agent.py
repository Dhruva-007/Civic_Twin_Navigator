from typing import Dict, Any, List, Optional
import logging

from services.vertex_ai_service import vertex_ai_service
from services.firebase_service import firebase_service
from utils.helpers import get_timestamp, generate_id

# Setup logging
logger = logging.getLogger(__name__)


class JourneyPlannerAgent:
    """
    Agent 4 - Journey Planner Agent

    Responsibilities:
    - Build personalized election journey for each user
    - Create step by step timeline
    - Remove irrelevant steps based on user profile
    - Set deadlines and dependencies
    - Track journey progress
    - Update journey based on completed steps
    """

    SYSTEM_INSTRUCTION = """
    You are the Journey Planner Agent for Civic Twin Navigator.
    You create personalized election participation journeys for Indian voters.

    Rules:
    - Create realistic and achievable step by step journeys
    - Personalize based on user profile and situation
    - Include clear deadlines and timeframes
    - Make steps actionable and specific
    - Remove steps not relevant to user situation
    - Always return valid JSON with no trailing commas
    - Use double quotes for all strings in JSON
    """


    def create_personalized_journey(
        self,
        session_id: str,
        profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a complete personalized election journey.

        Args:
            session_id: User session ID
            profile: Civic Twin profile

        Returns:
            Complete personalized journey with steps
        """
        try:
            voter_status = profile.get(
                "voter_profile", {}
            ).get("voter_status", "unknown")
            location = profile.get(
                "personal_info", {}
            ).get("location", "India")
            occupation = profile.get(
                "personal_info", {}
            ).get("occupation", "unknown")
            residence = profile.get(
                "personal_info", {}
            ).get("residence_type", "unknown")
            risk_factors = profile.get("risk_factors", [])
            doc_status = profile.get("document_status", {})

            prompt = f"""
Create a personalized election participation journey for this Indian voter.

User Profile:
- Voter Status: {voter_status}
- Location: {location}
- Occupation: {occupation}
- Residence Type: {residence}
- Risk Factors: {risk_factors}
- Document Status: {doc_status}

Create a journey with 5 to 7 phases. Each phase has specific steps.
Make it personalized based on their situation.

Return this exact JSON:
{{
  "session_id": "{session_id}",
  "journey_title": "Your Personal Voter Registration Journey",
  "total_phases": 5,
  "estimated_completion_days": 30,
  "phases": [
    {{
      "phase_id": "phase_1",
      "phase_number": 1,
      "title": "Eligibility Verification",
      "description": "Confirm you are eligible to vote",
      "status": "pending",
      "estimated_days": 1,
      "steps": [
        {{
          "step_id": "step_1_1",
          "title": "Check your age eligibility",
          "description": "Confirm you are 18 years or older",
          "action": "Verify your date of birth against voter eligibility requirements",
          "is_completed": false,
          "is_required": true,
          "resources": ["voters.eci.gov.in"]
        }},
        {{
          "step_id": "step_1_2",
          "title": "Verify citizenship status",
          "description": "Confirm you are an Indian citizen",
          "action": "Check your citizenship documents",
          "is_completed": false,
          "is_required": true,
          "resources": []
        }}
      ]
    }},
    {{
      "phase_id": "phase_2",
      "phase_number": 2,
      "title": "Document Preparation",
      "description": "Gather all required documents",
      "status": "pending",
      "estimated_days": 7,
      "steps": [
        {{
          "step_id": "step_2_1",
          "title": "Arrange Age Proof",
          "description": "Get a valid age proof document ready",
          "action": "Collect Birth Certificate or School Certificate or Passport",
          "is_completed": false,
          "is_required": true,
          "resources": []
        }},
        {{
          "step_id": "step_2_2",
          "title": "Arrange Address Proof",
          "description": "Get valid address proof for current location",
          "action": "For hostel residents get warden certificate on letterhead",
          "is_completed": false,
          "is_required": true,
          "resources": []
        }},
        {{
          "step_id": "step_2_3",
          "title": "Get Passport Size Photos",
          "description": "Get recent passport size photographs",
          "action": "Get 2 color passport size photos taken",
          "is_completed": false,
          "is_required": true,
          "resources": []
        }}
      ]
    }},
    {{
      "phase_id": "phase_3",
      "phase_number": 3,
      "title": "Voter Registration",
      "description": "Complete voter registration process",
      "status": "pending",
      "estimated_days": 3,
      "steps": [
        {{
          "step_id": "step_3_1",
          "title": "Fill Form 6 Online",
          "description": "Complete voter registration application",
          "action": "Visit voters.eci.gov.in and fill Form 6",
          "is_completed": false,
          "is_required": true,
          "resources": ["voters.eci.gov.in", "Voter Helpline App"]
        }},
        {{
          "step_id": "step_3_2",
          "title": "Upload Documents",
          "description": "Upload all required documents",
          "action": "Upload age proof, address proof and photo",
          "is_completed": false,
          "is_required": true,
          "resources": ["voters.eci.gov.in"]
        }},
        {{
          "step_id": "step_3_3",
          "title": "Note Application Number",
          "description": "Save your application reference number",
          "action": "Screenshot or note down the application number for tracking",
          "is_completed": false,
          "is_required": true,
          "resources": []
        }}
      ]
    }},
    {{
      "phase_id": "phase_4",
      "phase_number": 4,
      "title": "Registration Verification",
      "description": "Verify your registration was successful",
      "status": "pending",
      "estimated_days": 20,
      "steps": [
        {{
          "step_id": "step_4_1",
          "title": "Track Application Status",
          "description": "Monitor your registration application",
          "action": "Check status at voters.eci.gov.in using application number",
          "is_completed": false,
          "is_required": true,
          "resources": ["voters.eci.gov.in", "1950 helpline"]
        }},
        {{
          "step_id": "step_4_2",
          "title": "Verify Name on Electoral Roll",
          "description": "Confirm your name appears on voter list",
          "action": "Search your name on voters.eci.gov.in after approval",
          "is_completed": false,
          "is_required": true,
          "resources": ["voters.eci.gov.in"]
        }}
      ]
    }},
    {{
      "phase_id": "phase_5",
      "phase_number": 5,
      "title": "Poll Day Preparation",
      "description": "Get ready for voting day",
      "status": "pending",
      "estimated_days": 1,
      "steps": [
        {{
          "step_id": "step_5_1",
          "title": "Find Your Polling Booth",
          "description": "Know exactly where to go on poll day",
          "action": "Find your booth number and address on voters.eci.gov.in",
          "is_completed": false,
          "is_required": true,
          "resources": ["voters.eci.gov.in"]
        }},
        {{
          "step_id": "step_5_2",
          "title": "Prepare ID for Poll Day",
          "description": "Keep your voter ID or alternate ID ready",
          "action": "Keep Voter ID or Aadhar or any valid photo ID ready",
          "is_completed": false,
          "is_required": true,
          "resources": []
        }},
        {{
          "step_id": "step_5_3",
          "title": "Go Vote",
          "description": "Cast your vote at polling booth",
          "action": "Visit your polling booth between 7 AM to 6 PM on election day",
          "is_completed": false,
          "is_required": true,
          "resources": ["1950 helpline"]
        }}
      ]
    }}
  ],
  "personalization_notes": [
    "Journey customized for hostel resident",
    "Address proof step includes hostel certificate option"
  ],
  "important_reminders": [
    "Check registration deadline for your constituency",
    "Verify name on electoral roll before election day"
  ],
  "created_at": "{get_timestamp()}"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION
            )

            # Ensure session_id is set
            result["session_id"] = session_id

            # Save journey to Firebase
            firebase_service.save_journey(session_id, result)

            logger.info(f"Journey created for session: {session_id}")

            return {
                "success": True,
                "session_id": session_id,
                "data": result,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Create journey error: {e}")
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id
            }


    def update_step_status(
        self,
        session_id: str,
        phase_id: str,
        step_id: str,
        is_completed: bool
    ) -> Dict[str, Any]:
        """
        Update the completion status of a journey step.

        Args:
            session_id: User session ID
            phase_id: Phase identifier
            step_id: Step identifier
            is_completed: Whether step is completed

        Returns:
            Updated journey summary
        """
        try:
            # Get existing journey
            journey = firebase_service.get_journey(session_id)

            if not journey:
                return {
                    "success": False,
                    "error": "Journey not found"
                }

            # Update step status
            phases = journey.get("phases", [])
            updated = False

            for phase in phases:
                if phase.get("phase_id") == phase_id:
                    for step in phase.get("steps", []):
                        if step.get("step_id") == step_id:
                            step["is_completed"] = is_completed
                            step["completed_at"] = get_timestamp() if is_completed else None
                            updated = True
                            break

                    # Update phase status based on steps
                    all_steps = phase.get("steps", [])
                    completed_steps = [s for s in all_steps if s.get("is_completed")]

                    if len(completed_steps) == len(all_steps):
                        phase["status"] = "completed"
                    elif len(completed_steps) > 0:
                        phase["status"] = "in_progress"
                    else:
                        phase["status"] = "pending"

            if updated:
                journey["phases"] = phases
                journey["updated_at"] = get_timestamp()
                firebase_service.save_journey(session_id, journey)

            # Calculate overall progress
            progress = self._calculate_progress(phases)

            return {
                "success": True,
                "updated": updated,
                "progress": progress,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Update step status error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


    def get_next_steps(
        self,
        session_id: str
    ) -> Dict[str, Any]:
        """
        Get the next pending steps for a user.

        Args:
            session_id: User session ID

        Returns:
            Next steps to complete
        """
        try:
            journey = firebase_service.get_journey(session_id)

            if not journey:
                return {
                    "success": False,
                    "error": "Journey not found"
                }

            next_steps = []
            phases = journey.get("phases", [])

            for phase in phases:
                if phase.get("status") != "completed":
                    for step in phase.get("steps", []):
                        if not step.get("is_completed"):
                            next_steps.append({
                                "phase_id": phase.get("phase_id"),
                                "phase_title": phase.get("title"),
                                "step_id": step.get("step_id"),
                                "step_title": step.get("title"),
                                "action": step.get("action"),
                                "resources": step.get("resources", [])
                            })
                    # Only show next incomplete phase
                    if next_steps:
                        break

            progress = self._calculate_progress(phases)

            return {
                "success": True,
                "session_id": session_id,
                "next_steps": next_steps[:3],
                "progress": progress,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Get next steps error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


    def get_journey_summary(
        self,
        session_id: str
    ) -> Dict[str, Any]:
        """
        Get a summary of the user journey progress.

        Args:
            session_id: User session ID

        Returns:
            Journey summary with progress
        """
        try:
            journey = firebase_service.get_journey(session_id)

            if not journey:
                return {
                    "success": False,
                    "error": "Journey not found"
                }

            phases = journey.get("phases", [])
            progress = self._calculate_progress(phases)

            # Count steps
            total_steps = sum(
                len(p.get("steps", [])) for p in phases
            )
            completed_steps = sum(
                len([s for s in p.get("steps", []) if s.get("is_completed")])
                for p in phases
            )

            return {
                "success": True,
                "session_id": session_id,
                "journey_title": journey.get("journey_title"),
                "total_phases": len(phases),
                "completed_phases": len(
                    [p for p in phases if p.get("status") == "completed"]
                ),
                "total_steps": total_steps,
                "completed_steps": completed_steps,
                "progress_percentage": progress,
                "current_phase": self._get_current_phase(phases),
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Get journey summary error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


    def _calculate_progress(self, phases: List[Dict]) -> float:
        """Calculate overall journey progress percentage"""
        try:
            total_steps = sum(len(p.get("steps", [])) for p in phases)
            if total_steps == 0:
                return 0.0

            completed = sum(
                len([s for s in p.get("steps", []) if s.get("is_completed")])
                for p in phases
            )
            return round((completed / total_steps) * 100, 1)

        except Exception:
            return 0.0


    def _get_current_phase(self, phases: List[Dict]) -> Optional[Dict]:
        """Get the current active phase"""
        for phase in phases:
            if phase.get("status") in ["pending", "in_progress"]:
                return {
                    "phase_id": phase.get("phase_id"),
                    "title": phase.get("title"),
                    "status": phase.get("status")
                }
        return None


# Single instance
journey_planner_agent = JourneyPlannerAgent()