from typing import Dict, Any, Optional
import logging

from services.vertex_ai_service import vertex_ai_service
from services.translation_service import translation_service
from services.speech_service import speech_service
from utils.helpers import get_timestamp

logger = logging.getLogger(__name__)


class AccessibilityAgent:
    """
    Agent 8 – Accessibility Agent

    Responsibilities:
    - Simplify language based on literacy level
    - Support multilingual interaction
    - Enable voice-based interaction (TTS/STT)
    - Adapt content for users with special needs
    - Provide step-by-step micro-guidance
    """

    SYSTEM_INSTRUCTION = """
    You are the Accessibility Agent for Civic Twin Navigator.
    You make election information accessible to all Indian voters.

    Rules:
    - Use simple words and short sentences
    - Translate to user's preferred language
    - Adapt for different literacy levels
    - Be patient and encouraging
    - Respect all users regardless of background
    """

    def simplify_content(
        self,
        text: str,
        user_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Simplify content based on user literacy level.

        Args:
            text: Original text to simplify
            user_profile: User profile with literacy level

        Returns:
            Simplified content
        """
        try:
            literacy = user_profile.get(
                "accessibility_profile", {}
            ).get("literacy_level", "basic")

            simplified = vertex_ai_service.simplify_text(
                text=text,
                language="en",
                literacy_level=literacy
            )

            return {
                "success": True,
                "original": text,
                "simplified": simplified,
                "literacy_level": literacy,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Simplify content error: {e}")
            return {"success": False, "error": str(e), "simplified": text}

    def translate_content(
        self,
        text: str,
        target_language: str
    ) -> Dict[str, Any]:
        """
        Translate content to user's language.

        Args:
            text: Text to translate
            target_language: Language code (hi, mr, ta, te, etc.)

        Returns:
            Translated content
        """
        try:
            result = translation_service.translate_text(
                text=text,
                target_language=target_language
            )

            return {
                "success": result.get("success", False),
                "original": text,
                "translated": result.get("translated_text", text),
                "language": target_language,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Translate content error: {e}")
            return {"success": False, "error": str(e), "translated": text}

    def text_to_speech(
        self,
        text: str,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Convert text to speech for voice interaction.

        Args:
            text: Text to speak
            language: Language code

        Returns:
            Audio data as base64
        """
        try:
            result = speech_service.text_to_speech(
                text=text,
                language=language,
                speaking_rate=0.9
            )

            return {
                "success": result.get("success", False),
                "audio_base64": result.get("audio_base64", ""),
                "format": "mp3",
                "language": language,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Text to speech error: {e}")
            return {"success": False, "error": str(e)}

    def speech_to_text(
        self,
        audio_base64: str,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Convert speech to text.

        Args:
            audio_base64: Base64 encoded audio
            language: Expected language

        Returns:
            Transcribed text
        """
        try:
            result = speech_service.speech_to_text(
                audio_base64=audio_base64,
                language=language
            )

            return {
                "success": result.get("success", False),
                "transcript": result.get("transcript", ""),
                "confidence": result.get("confidence", 0),
                "language": language,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Speech to text error: {e}")
            return {"success": False, "error": str(e)}

    def create_micro_guidance(
        self,
        step_title: str,
        step_description: str
    ) -> Dict[str, Any]:
        """
        Create a small, easy-to-follow guidance for one step.

        Args:
            step_title: Title of the step
            step_description: Description

        Returns:
            Micro-guidance with simple instructions
        """
        try:
            prompt = f"""
Create simple step-by-step guidance for this election step.

Step Title: {step_title}
Step Description: {step_description}

Return this exact JSON:
{{
  "step_title": "{step_title}",
  "simple_instructions": [
    "Instruction 1 – one simple sentence with action",
    "Instruction 2 – one simple sentence with action",
    "Instruction 3 – one simple sentence with action"
  ],
  "what_you_need": ["item 1", "item 2"],
  "time_needed": "X minutes",
  "common_mistake": "one common mistake to avoid",
  "encouragement": "one motivational line"
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
            logger.error(f"Create micro guidance error: {e}")
            return {"success": False, "error": str(e)}


accessibility_agent = AccessibilityAgent()