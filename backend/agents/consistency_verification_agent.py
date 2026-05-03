from typing import Dict, Any, List, Optional
import logging

from services.vertex_ai_service import vertex_ai_service
from utils.helpers import get_timestamp

# Setup logging
logger = logging.getLogger(__name__)


class ConsistencyVerificationAgent:
    """
    Agent 3 - Consistency & Verification Agent

    Responsibilities:
    - Validate information provided by other agents
    - Cross check user profile data for consistency
    - Verify document combinations are valid
    - Detect contradictions in user inputs
    - Flag potential issues before they cause problems
    - Ensure data quality across the journey
    """

    SYSTEM_INSTRUCTION = """
    You are the Consistency & Verification Agent for Civic Twin Navigator.
    Your job is to validate and verify election related information.

    Rules:
    - Be thorough and precise in verification
    - Flag any inconsistencies clearly
    - Suggest corrections when issues are found
    - Never approve invalid or contradictory information
    - Always return valid JSON with no trailing commas
    - Use double quotes for all strings in JSON
    - Be helpful not alarming when flagging issues
    """


    def verify_civic_twin_profile(
        self,
        profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Verify a Civic Twin profile for consistency and completeness.

        Args:
            profile: Civic Twin profile to verify

        Returns:
            Verification result with issues and suggestions
        """
        try:
            prompt = f"""
Verify this Civic Twin voter profile for consistency and completeness.

Profile to verify:
{profile}

Check for:
1. Age eligibility (must be 18 or older to vote)
2. Required fields are present
3. Location information is valid Indian location
4. Document status consistency
5. Any contradictory information
6. Missing critical information

Return this exact JSON:
{{
  "is_valid": true,
  "verification_status": "verified",
  "overall_score": 85,
  "checks": {{
    "age_check": {{
      "passed": true,
      "message": "Age verification result"
    }},
    "location_check": {{
      "passed": true,
      "message": "Location verification result"
    }},
    "document_check": {{
      "passed": true,
      "message": "Document verification result"
    }},
    "completeness_check": {{
      "passed": true,
      "message": "Profile completeness result"
    }}
  }},
  "issues_found": [],
  "warnings": [],
  "suggestions": [],
  "missing_critical_fields": [],
  "verified_at": "{get_timestamp()}"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION
            )

            return {
                "success": True,
                "data": result,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Verify civic twin profile error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


    def verify_document_combination(
        self,
        documents: List[str],
        purpose: str = "voter_registration"
    ) -> Dict[str, Any]:
        """
        Verify if the provided document combination is valid.

        Args:
            documents: List of documents user has
            purpose: Purpose of verification

        Returns:
            Verification result
        """
        try:
            prompt = f"""
Verify if this document combination is valid for {purpose} in India.

Documents provided by user: {documents}

Check against Election Commission of India requirements:
1. Is age proof present and valid
2. Is address proof present and valid
3. Is photograph available
4. Are there any document conflicts
5. What is missing if anything

Return this exact JSON:
{{
  "is_valid_combination": true,
  "purpose": "{purpose}",
  "documents_provided": {documents},
  "verification_results": {{
    "age_proof": {{
      "satisfied": true,
      "document_used": "document name or none",
      "message": "result message"
    }},
    "address_proof": {{
      "satisfied": true,
      "document_used": "document name or none",
      "message": "result message"
    }},
    "photo": {{
      "satisfied": false,
      "message": "Passport size photo needs to be arranged"
    }}
  }},
  "missing_documents": [],
  "alternative_suggestions": [],
  "can_proceed": true,
  "blocking_issues": [],
  "recommendation": "overall recommendation"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION
            )

            return {
                "success": True,
                "data": result,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Verify document combination error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


    def detect_contradictions(
        self,
        user_inputs: List[str]
    ) -> Dict[str, Any]:
        """
        Detect contradictions in multiple user inputs.

        Args:
            user_inputs: List of user statements to cross check

        Returns:
            Contradiction detection result
        """
        try:
            inputs_text = "\n".join(
                [f"{i+1}. {inp}" for i, inp in enumerate(user_inputs)]
            )

            prompt = f"""
Analyze these user statements for contradictions or inconsistencies.

User statements:
{inputs_text}

Check for:
1. Age contradictions
2. Location contradictions
3. Document status contradictions
4. Voter status contradictions
5. Timeline contradictions

Return this exact JSON:
{{
  "has_contradictions": false,
  "contradiction_count": 0,
  "contradictions": [],
  "consistent_facts": ["fact 1", "fact 2"],
  "needs_clarification": [],
  "recommendation": "all statements are consistent"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION
            )

            return {
                "success": True,
                "data": result,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Detect contradictions error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


    def verify_agent_response(
        self,
        agent_name: str,
        response_data: Dict[str, Any],
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Verify response from another agent for accuracy.

        Args:
            agent_name: Name of the agent whose response is being verified
            response_data: The response data to verify
            context: Optional context for verification

        Returns:
            Verification result
        """
        try:
            context_text = ""
            if context:
                context_text = f"Context: {context}"

            prompt = f"""
Verify this response from {agent_name} for accuracy and consistency.

Response to verify:
{response_data}

{context_text}

Check:
1. Is the information factually accurate for Indian elections
2. Is it consistent with Election Commission of India guidelines
3. Are there any misleading statements
4. Is it complete and not missing critical information
5. Is it politically neutral

Return this exact JSON:
{{
  "agent_name": "{agent_name}",
  "is_accurate": true,
  "is_complete": true,
  "is_neutral": true,
  "accuracy_score": 90,
  "issues": [],
  "corrections_needed": [],
  "approved": true,
  "verification_notes": "response is accurate and complete"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION
            )

            return {
                "success": True,
                "data": result,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Verify agent response error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


    def cross_check_eligibility(
        self,
        profile: Dict[str, Any],
        eligibility_rules: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Cross check user profile against eligibility rules.

        Args:
            profile: User civic twin profile
            eligibility_rules: Rules from policy agent

        Returns:
            Cross check result
        """
        try:
            prompt = f"""
Cross check this user profile against Indian voter eligibility rules.

User Profile:
{profile}

Eligibility Rules:
{eligibility_rules}

Perform detailed cross check and return this exact JSON:
{{
  "is_eligible": true,
  "eligibility_score": 90,
  "criteria_checks": [
    {{
      "criteria": "Age requirement",
      "status": "passed",
      "detail": "User is 20 years old, meets 18 year minimum"
    }},
    {{
      "criteria": "Citizenship",
      "status": "assumed_passed",
      "detail": "Citizenship not explicitly stated but assumed Indian"
    }},
    {{
      "criteria": "Residence",
      "status": "needs_verification",
      "detail": "Hostel address needs proper documentation"
    }}
  ],
  "blocking_issues": [],
  "non_blocking_issues": [],
  "final_recommendation": "User appears eligible to vote",
  "confidence_level": "high"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION
            )

            return {
                "success": True,
                "data": result,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Cross check eligibility error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Single instance
consistency_verification_agent = ConsistencyVerificationAgent()