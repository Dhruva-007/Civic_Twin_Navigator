from typing import Dict, Any, List, Optional
import logging

from services.vertex_ai_service import vertex_ai_service
from utils.helpers import get_timestamp

logger = logging.getLogger(__name__)


class PredictionAgent:
    """
    Agent 7 – Prediction Agent

    Responsibilities:
    - Predict failure risks based on similar user profiles
    - Proactively create corrective missions
    - Identify common pitfalls for specific user types
    - Recommend preventive actions
    """

    SYSTEM_INSTRUCTION = """
    You are the Prediction Agent for Civic Twin Navigator.
    You analyze user profiles to predict potential election participation failures.

    Rules:
    - Base predictions on common patterns for Indian voters
    - Never assume based on demographics
    - Be helpful, not alarming
    - Focus on actionable prevention
    - Always return valid JSON with no trailing commas
    """

    def predict_failure_risks(
        self,
        profile: Dict[str, Any],
        journey: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Predict failure risks for the user.

        Args:
            profile: Civic Twin profile
            journey: Optional journey data

        Returns:
            Risk predictions with corrective missions
        """
        try:
            prompt = f"""
Analyze this voter profile for potential failure risks during the Indian election process.

Profile:
- Location: {profile.get('personal_info', {}).get('location')}
- Age: {profile.get('personal_info', {}).get('age')}
- Residence: {profile.get('personal_info', {}).get('residence_type')}
- Voter Status: {profile.get('voter_profile', {}).get('voter_status')}
- Document Concerns: {profile.get('document_status', {}).get('document_concerns')}
- Risk Factors: {profile.get('risk_factors')}

Return this exact JSON:
{{
  "profile_type": "first_time_student_hostel",
  "risk_assessment": {{
    "overall_risk_level": "medium",
    "risk_factors": [
      {{
        "factor": "Address proof for hostel residents",
        "risk_level": "high",
        "probability": 0.8,
        "impact": "Registration rejection or delay",
        "explanation": "Hostel residents often submit incorrect address proof, causing application to be returned",
        "similar_users_affected": true,
        "preventive_action": "Obtain official hostel certificate from warden on institution letterhead"
      }},
      {{
        "factor": "First-time voter unaware of deadlines",
        "risk_level": "medium",
        "probability": 0.6,
        "impact": "Missing registration deadline",
        "explanation": "Many first-time voters underestimate processing time and miss cutoff",
        "similar_users_affected": true,
        "preventive_action": "Set calendar reminders 30 days before election announcement"
      }},
      {{
        "factor": "Missing photo ID on poll day",
        "risk_level": "low",
        "probability": 0.3,
        "impact": "Unable to vote",
        "explanation": "User has Aadhar which is accepted alternative ID",
        "similar_users_affected": false,
        "preventive_action": "Keep Aadhar card ready"
      }}
    ]
  }},
  "corrective_mission": {{
    "mission_title": "Fix Your Address Proof",
    "description": "Complete this mission to get your hostel address proof ready",
    "steps": [
      "Meet hostel warden with request letter",
      "Get certificate on official letterhead with stamp and signature",
      "Scan or photograph the certificate clearly"
    ],
    "estimated_time": "1 day"
  }},
  "recommendations": [
    "Start registration process immediately to allow buffer time",
    "Keep multiple copies of hostel certificate"
  ],
  "prediction_confidence": "high"
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
            logger.error(f"Predict failure risks error: {e}")
            return {"success": False, "error": str(e)}

    def suggest_preventive_missions(
        self,
        risk_factors: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate preventive missions based on risk factors.

        Args:
            risk_factors: List of identified risks

        Returns:
            Preventive missions
        """
        try:
            prompt = f"""
Create preventive missions for these voter risk factors.

Risk Factors: {risk_factors}

Return this exact JSON:
{{
  "missions": [
    {{
      "title": "Fix Address Proof",
      "reason": "Hostel residents at risk of registration delay",
      "priority": "high",
      "steps": ["Get warden certificate", "Verify address", "Upload to form"]
    }},
    {{
      "title": "Deadline Reminder Setup",
      "reason": "First-time voters often miss deadlines",
      "priority": "medium",
      "steps": ["Check election schedule", "Set phone reminders", "Mark calendar"]
    }}
  ]
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
            logger.error(f"Suggest preventive missions error: {e}")
            return {"success": False, "error": str(e)}


prediction_agent = PredictionAgent()