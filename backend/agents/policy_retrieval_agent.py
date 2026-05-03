from typing import Dict, Any, List, Optional
import logging

from services.vertex_ai_service import vertex_ai_service
from utils.helpers import get_timestamp

# Setup logging
logger = logging.getLogger(__name__)


class PolicyRetrievalAgent:
    """
    Agent 2 - Policy Retrieval Agent

    Responsibilities:
    - Fetch and explain election rules and policies
    - Provide accurate voting procedures
    - Retrieve document requirements
    - Get registration timelines and deadlines
    - Explain legal voter eligibility criteria
    """

    SYSTEM_INSTRUCTION = """
    You are the Policy Retrieval Agent for Civic Twin Navigator.
    You provide accurate, unbiased information about Indian election procedures.

    Rules:
    - Only provide factual, verified election information
    - Reference Election Commission of India guidelines
    - Never promote any political party or candidate
    - Be precise about legal requirements
    - Clearly state when information may vary by state
    - Always mention source as Election Commission of India
    - If unsure, say so and recommend official ECI website
    - Always return valid JSON with no trailing commas
    - Use double quotes for all strings in JSON
    """


    def get_eligibility_rules(
        self,
        user_profile: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Get voter eligibility rules personalized if profile provided.

        Args:
            user_profile: Optional user profile for personalization

        Returns:
            Eligibility rules and assessment
        """
        try:
            profile_context = ""
            if user_profile:
                age = user_profile.get("personal_info", {}).get("age")
                location = user_profile.get("personal_info", {}).get("location")
                profile_context = f"User age: {age}, Location: {location}"

            prompt = f"""
Provide voter eligibility rules for India.
{profile_context}

Return this exact JSON structure:
{{
  "eligibility_criteria": {{
    "minimum_age": 18,
    "citizenship_required": true,
    "residence_requirement": "Must be ordinarily resident in the constituency",
    "disqualifications": ["Declared of unsound mind", "Corrupt practices conviction", "Criminal sentence over 2 years"]
  }},
  "user_eligibility": {{
    "is_eligible": true,
    "eligibility_reason": "User meets basic eligibility criteria",
    "age_check": "passed",
    "concerns": []
  }},
  "next_steps": ["Check your name on electoral roll at voters.eci.gov.in", "Register if not already registered using Form 6"],
  "official_source": "Election Commission of India - eci.gov.in",
  "important_notes": ["Eligibility is checked at constituency level", "Registration deadline varies by election"]
}}

IMPORTANT: Return only valid JSON. No markdown. No extra text. No trailing commas.
"""
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION
            )

            return {
                "success": True,
                "data": result,
                "source": "Election Commission of India",
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Get eligibility rules error: {e}")
            return {
                "success": True,
                "data": {
                    "eligibility_criteria": {
                        "minimum_age": 18,
                        "citizenship_required": True,
                        "residence_requirement": "Must be ordinarily resident in constituency",
                        "disqualifications": [
                            "Declared of unsound mind",
                            "Criminal conviction"
                        ]
                    },
                    "next_steps": [
                        "Check voters.eci.gov.in",
                        "Register using Form 6"
                    ],
                    "official_source": "eci.gov.in"
                },
                "source": "Election Commission of India (Fallback)",
                "timestamp": get_timestamp()
            }


    def get_registration_process(
        self,
        user_profile: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Get voter registration process steps.

        Args:
            user_profile: Optional user profile for personalization

        Returns:
            Step by step registration process
        """
        try:
            voter_status = "new voter"
            location = "India"

            if user_profile:
                voter_status = user_profile.get(
                    "voter_profile", {}
                ).get("voter_status", "new voter")
                location = user_profile.get(
                    "personal_info", {}
                ).get("location", "India")

            prompt = f"""
Provide voter registration process for India.
User type: {voter_status}
Location: {location}

Return this exact JSON:
{{
  "registration_method": {{
    "online": {{
      "platform": "voters.eci.gov.in or Voter Helpline App",
      "form": "Form 6 for new voters",
      "steps": [
        "Visit voters.eci.gov.in",
        "Click on Register as New Voter",
        "Fill Form 6 with personal details",
        "Upload required documents",
        "Submit and note application number"
      ]
    }},
    "offline": {{
      "location": "Booth Level Officer or Electoral Registration Office",
      "form": "Form 6",
      "steps": [
        "Visit nearest Electoral Registration Office",
        "Collect and fill Form 6",
        "Attach required documents",
        "Submit to Booth Level Officer"
      ]
    }}
  }},
  "required_documents": {{
    "mandatory": ["Age Proof", "Address Proof", "Photograph"],
    "age_proof_options": ["Birth Certificate", "School Certificate", "Passport", "PAN Card"],
    "address_proof_options": ["Aadhar Card", "Passport", "Bank Passbook", "Utility Bill"],
    "photo_requirement": "Recent passport size photograph"
  }},
  "timeline": {{
    "processing_time": "15 to 30 days",
    "verification_process": "Field verification by Booth Level Officer",
    "confirmation_method": "SMS and email notification"
  }},
  "special_cases": {{
    "hostel_students": "Use hostel certificate from warden as address proof",
    "migrants": "Can register at current place of residence",
    "no_fixed_address": "Contact Electoral Registration Officer for assistance"
  }},
  "important_deadlines": ["Check ECI website for current deadlines"],
  "helpline": "1950",
  "official_website": "voters.eci.gov.in"
}}

IMPORTANT: Return only valid JSON. No markdown. No extra text. No trailing commas.
"""
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION
            )

            return {
                "success": True,
                "data": result,
                "source": "Election Commission of India",
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Get registration process error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


    def get_document_requirements(
        self,
        user_profile: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Get personalized document requirements.

        Args:
            user_profile: User profile to personalize requirements

        Returns:
            Document requirements with alternatives
        """
        try:
            profile_context = ""
            if user_profile:
                doc_status = user_profile.get("document_status", {})
                personal = user_profile.get("personal_info", {})
                profile_context = f"""
User residence: {personal.get('residence_type', 'unknown')}
Has Aadhar: {doc_status.get('has_aadhar', 'unknown')}
Occupation: {personal.get('occupation', 'unknown')}
"""

            prompt = f"""
Provide voter registration document requirements for India.
{profile_context}

Return this exact JSON structure with no trailing commas:
{{
  "mandatory_documents": [
    {{
      "type": "Age Proof",
      "options": ["Birth Certificate", "School Leaving Certificate", "Passport", "PAN Card", "Driving License"],
      "notes": "Any one document showing date of birth"
    }},
    {{
      "type": "Address Proof",
      "options": ["Aadhar Card", "Passport", "Driving License", "Bank Passbook", "Utility Bill", "Rent Agreement"],
      "notes": "Any one document showing current address"
    }},
    {{
      "type": "Photograph",
      "options": ["Recent Passport Size Photo"],
      "notes": "Color photo with white background preferred"
    }}
  ],
  "special_situations": {{
    "hostel_students": "Hostel Certificate from Warden on institute letterhead",
    "no_aadhar": "Use Passport, Driving License or Bank Passbook instead",
    "no_fixed_address": "Contact local Electoral Registration Officer",
    "parents_home": "Use parent address proof with relationship proof"
  }},
  "document_tips": [
    "Keep original documents for verification",
    "Ensure documents are valid and not expired",
    "Use clear scanned copies for online application"
  ],
  "common_mistakes": [
    "Using expired documents",
    "Address mismatch between documents",
    "Submitting unclear photocopies"
  ],
  "where_to_get_docs": {{
    "aadhar": "Visit uidai.gov.in or nearest Aadhar enrollment center",
    "birth_certificate": "Municipal Corporation of your birth place",
    "other": "Contact Electoral Registration Office for guidance"
  }}
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
                "source": "Election Commission of India",
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Get document requirements error: {e}")
            return {
                "success": True,
                "data": {
                    "mandatory_documents": [
                        {
                            "type": "Age Proof",
                            "options": [
                                "Birth Certificate",
                                "School Leaving Certificate",
                                "Passport",
                                "PAN Card"
                            ],
                            "notes": "Any one document"
                        },
                        {
                            "type": "Address Proof",
                            "options": [
                                "Aadhar Card",
                                "Passport",
                                "Bank Passbook",
                                "Utility Bill"
                            ],
                            "notes": "Any one document"
                        },
                        {
                            "type": "Photograph",
                            "options": ["Passport Size Photo"],
                            "notes": "Recent color photo"
                        }
                    ],
                    "special_situations": {
                        "hostel_students": "Hostel Certificate from Warden",
                        "no_aadhar": "Use alternative address proof"
                    },
                    "document_tips": [
                        "Keep originals ready",
                        "Use clear copies"
                    ],
                    "common_mistakes": [
                        "Expired documents",
                        "Unclear copies"
                    ]
                },
                "source": "Election Commission of India (Fallback)",
                "timestamp": get_timestamp(),
                "warning": "Using fallback data"
            }


    def get_poll_day_guide(
        self,
        user_profile: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Get complete poll day guidance.

        Args:
            user_profile: User profile for personalization

        Returns:
            Poll day guide
        """
        try:
            prompt = f"""
Provide complete poll day guidance for Indian voters.

Return this exact JSON:
{{
  "before_poll_day": {{
    "check_name_on_list": "Visit voters.eci.gov.in or call 1950 to verify your name",
    "find_polling_station": "Check your Voter ID card or voters.eci.gov.in for booth details",
    "what_to_prepare": ["Carry any one valid photo ID", "Note your booth number and address", "Check polling hours"]
  }},
  "valid_id_proofs": [
    "Voter ID Card (EPIC)",
    "Aadhar Card",
    "Passport",
    "Driving License",
    "PAN Card",
    "MNREGA Job Card",
    "Bank or Post Office Passbook with photo",
    "Pension document with photo",
    "Service Identity Card with photo"
  ],
  "at_polling_station": {{
    "process_steps": [
      "Join the queue at your designated polling booth",
      "Show your photo ID to polling officer",
      "Get your finger marked with indelible ink",
      "Press the button on EVM for your choice",
      "Verify on VVPAT slip"
    ],
    "voting_machine": "Electronic Voting Machine press button next to candidate name",
    "vvpat": "Voter Verified Paper Audit Trail shows slip for 7 seconds to verify",
    "time_required": "Approximately 5 to 10 minutes"
  }},
  "polling_hours": "7:00 AM to 6:00 PM general timing may vary by constituency",
  "rights_at_booth": [
    "Right to vote without being pressured",
    "Right to cast NOTA vote",
    "Right to complain if facing issues"
  ],
  "what_not_to_do": [
    "Do not carry mobile phones inside voting compartment",
    "Do not take photos of your vote",
    "Do not campaign within 100 meters of booth"
  ],
  "if_name_missing": "Contact Presiding Officer or call 1950 helpline immediately",
  "helpline": "1950"
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
                "source": "Election Commission of India",
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Get poll day guide error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


    def answer_specific_query(
        self,
        query: str,
        user_profile: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Answer a specific election policy question.

        Args:
            query: User specific question
            user_profile: Optional user profile for context

        Returns:
            Answer with source and confidence
        """
        try:
            profile_context = ""
            if user_profile:
                location = user_profile.get(
                    "personal_info", {}
                ).get("location", "India")
                profile_context = f"User location: {location}"

            prompt = f"""
Answer this election question accurately and completely.

Question: "{query}"
{profile_context}

Provide a thorough and complete answer covering all aspects of the question.

Return this exact JSON:
{{
  "question": "{query}",
  "answer": "Write a complete and detailed answer here. Cover all aspects. Do not cut short. Minimum 3 to 4 sentences.",
  "key_points": [
    "Complete key point 1 with full detail",
    "Complete key point 2 with full detail",
    "Complete key point 3 with full detail"
  ],
  "action_required": true,
  "action_steps": [
    "Step 1 with full instruction",
    "Step 2 with full instruction",
    "Step 3 with full instruction"
  ],
  "confidence_level": "high",
  "official_source": "Election Commission of India - eci.gov.in",
  "disclaimer": "Information based on ECI guidelines. Always verify at eci.gov.in for latest updates."
}}

IMPORTANT:
- Return only valid JSON
- No markdown
- No trailing commas
- Answer field must be complete and not cut short
- All fields must have complete values
"""
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION,
                temperature=0.2
            )

            return {
                "success": True,
                "data": result,
                "source": "Election Commission of India",
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Answer specific query error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


    def get_state_specific_info(
        self,
        state: str
    ) -> Dict[str, Any]:
        """
        Get state specific election information.

        Args:
            state: Indian state name

        Returns:
            State specific election details
        """
        try:
            prompt = f"""
Provide state specific election information for {state}, India.

Return this exact JSON:
{{
  "state": "{state}",
  "election_body": "State Election Commission details",
  "current_assembly_seats": "number or unknown",
  "last_election_year": "year or unknown",
  "voter_helpline": "state specific number or 1950",
  "special_provisions": ["any state specific rules"],
  "official_website": "state election commission website",
  "notes": "any important state specific notes"
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
                "source": "State Election Commission",
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Get state info error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Single instance
policy_retrieval_agent = PolicyRetrievalAgent()