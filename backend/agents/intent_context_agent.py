from typing import Dict, Any, Optional
import logging

from services.vertex_ai_service import vertex_ai_service
from services.firebase_service import firebase_service
from utils.helpers import generate_id, get_timestamp, sanitize_input
from utils.validators import validate_location, validate_age, validate_language

# Setup logging
logger = logging.getLogger(__name__)


class IntentContextAgent:
    """
    Agent 1 - Intent & Context Agent
    
    Responsibilities:
    - Understand what the user is asking
    - Extract user profile information
    - Identify knowledge gaps and concerns
    - Build initial Civic Twin profile
    - Determine language and literacy level
    """

    SYSTEM_INSTRUCTION = """
    You are the Intent & Context Agent for Civic Twin Navigator.
    Your job is to understand user inputs about elections and voting.
    
    Rules:
    - Be neutral, never promote any political party or candidate
    - Be helpful and empathetic especially to first-time voters
    - Extract only factual information from user input
    - Always respond in valid JSON format when asked
    - Identify user concerns and knowledge gaps
    - Respect all languages and literacy levels
    """

    def analyze_user_input(
        self,
        user_input: str,
        session_id: Optional[str] = None,
        existing_profile: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Analyze user input to extract intent and context.

        Args:
            user_input: Raw user text input
            session_id: Optional existing session ID
            existing_profile: Optional existing civic twin profile

        Returns:
            Analyzed intent and extracted context
        """
        try:
            # Sanitize input
            clean_input = sanitize_input(user_input)

            # Build context from existing profile
            profile_context = ""
            if existing_profile:
                profile_context = f"""
Existing user profile:
- Location: {existing_profile.get('location', 'unknown')}
- Age: {existing_profile.get('age', 'unknown')}
- Voter Status: {existing_profile.get('voter_status', 'unknown')}
- Language: {existing_profile.get('language', 'en')}
"""

            prompt = f"""
Analyze this user input about elections/voting and extract information.

User Input: "{clean_input}"

{profile_context}

Extract and return JSON with this exact structure:
{{
    "intent": "one of: registration_query, eligibility_query, document_query, timeline_query, polling_query, general_query, scenario_query, help_request",
    "extracted_info": {{
        "location": "city or area mentioned or null",
        "age": "age if mentioned or null",
        "voter_status": "one of: first_time, registered, unsure or null",
        "occupation": "student/worker/etc or null",
        "residence_type": "hostel/rented/owned/etc or null",
        "language_preference": "detected language code like en/hi/mr or en",
        "literacy_level": "one of: basic/intermediate/advanced based on writing style",
        "special_needs": "any accessibility needs mentioned or null"
    }},
    "concerns": ["list", "of", "specific", "concerns", "mentioned"],
    "knowledge_gaps": ["things", "user", "seems", "unsure", "about"],
    "confidence_level": "one of: low/medium/high - how confident user seems",
    "requires_clarification": true or false,
    "clarification_questions": ["question if clarification needed or empty list"],
    "summary": "one sentence summary of what user needs"
}}
"""
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION
            )

            logger.info(f"Intent analyzed: {result.get('intent')} for session: {session_id}")
            return {
                "success": True,
                "session_id": session_id,
                "analysis": result,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Intent analysis error: {e}")
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id
            }


    def build_civic_twin_profile(
        self,
        user_input: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Build a complete Civic Twin profile from user input.

        Args:
            user_input: Raw user text describing their situation
            session_id: Optional session ID (generates new if not provided)

        Returns:
            Complete Civic Twin profile
        """
        try:
            # Generate session ID if not provided
            if not session_id:
                session_id = generate_id()

            # Clean input
            clean_input = sanitize_input(user_input)

            prompt = f"""
Based on this user input, create a complete Civic Twin profile for an
Indian election assistance system.

User Input: "{clean_input}"

Create a detailed profile with this exact JSON structure:
{{
    "session_id": "{session_id}",
    "personal_info": {{
        "location": "extracted city/area or 'Not specified'",
        "state": "extracted Indian state or 'Not specified'",
        "age": null or number,
        "occupation": "extracted or 'Not specified'",
        "residence_type": "hostel/rented/owned/parents_home or 'Not specified'"
    }},
    "voter_profile": {{
        "voter_status": "first_time/registered/unsure",
        "is_eligible": true or false or null,
        "registration_status": "registered/not_registered/unknown",
        "has_voter_id": true or false or null,
        "constituency": "if mentioned or null"
    }},
    "document_status": {{
        "has_aadhar": null,
        "has_address_proof": null,
        "has_age_proof": null,
        "document_concerns": ["list of document concerns mentioned"]
    }},
    "accessibility_profile": {{
        "language_preference": "language code like en/hi/mr",
        "literacy_level": "basic/intermediate/advanced",
        "needs_voice_support": false,
        "needs_simple_language": false,
        "special_needs": null
    }},
    "risk_factors": ["list", "of", "identified", "risk", "factors"],
    "priority_concerns": ["most", "urgent", "concerns", "to", "address"],
    "created_at": "{get_timestamp()}",
    "profile_completeness": 0 to 100
}}
"""
            profile = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION
            )

            # Ensure session_id is set
            profile["session_id"] = session_id

            # Save to Firebase
            firebase_service.save_civic_twin(session_id, profile)

            # Save initial message
            firebase_service.save_message(session_id, "user", user_input)

            logger.info(f"Civic Twin profile built: {session_id}")

            return {
                "success": True,
                "session_id": session_id,
                "profile": profile,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Build civic twin error: {e}")
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id
            }


    def update_civic_twin_profile(
        self,
        session_id: str,
        new_input: str
    ) -> Dict[str, Any]:
        """
        Update existing Civic Twin profile with new information.

        Args:
            session_id: Existing session ID
            new_input: New user input with additional information

        Returns:
            Updated profile
        """
        try:
            # Get existing profile
            existing_profile = firebase_service.get_civic_twin(session_id)

            if not existing_profile:
                # Build new profile if not found
                return self.build_civic_twin_profile(new_input, session_id)

            # Clean input
            clean_input = sanitize_input(new_input)

            prompt = f"""
Update this existing Civic Twin profile with new information from user.

Existing Profile:
{existing_profile}

New User Input: "{clean_input}"

Return updated JSON profile with same structure but incorporating new info.
Only update fields where new information is provided.
Keep existing values for fields not mentioned in new input.
Update profile_completeness score based on how complete the profile is now.
"""
            updated_profile = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION
            )

            # Ensure session_id preserved
            updated_profile["session_id"] = session_id

            # Save updated profile
            firebase_service.save_civic_twin(session_id, updated_profile)

            # Save new message
            firebase_service.save_message(session_id, "user", new_input)

            logger.info(f"Civic Twin profile updated: {session_id}")

            return {
                "success": True,
                "session_id": session_id,
                "profile": updated_profile,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Update civic twin error: {e}")
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id
            }


    def get_clarification_response(
        self,
        session_id: str,
        missing_info: list
    ) -> Dict[str, Any]:
        """
        Generate friendly questions to get missing information.

        Args:
            session_id: Session ID
            missing_info: List of missing information fields

        Returns:
            Friendly questions for the user
        """
        try:
            prompt = f"""
Generate friendly, simple questions to collect missing voter information.

Missing information needed: {missing_info}

Rules:
- Ask maximum 2 questions at a time
- Use simple conversational language
- Be encouraging and friendly
- Frame questions in context of helping them vote

Return JSON:
{{
    "questions": ["question 1", "question 2"],
    "friendly_message": "encouraging message to motivate user",
    "why_needed": "brief explanation of why this info helps"
}}
"""
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION
            )

            return {
                "success": True,
                "session_id": session_id,
                "clarification": result,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Clarification error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Single instance
intent_context_agent = IntentContextAgent()