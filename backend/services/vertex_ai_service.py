from google import genai
from google.genai import types
from typing import Optional, List, Dict, Any
import logging
import json
import re
import time

from config.settings import settings

# Setup logging
logger = logging.getLogger(__name__)


class VertexAIService:
    """
    Core Vertex AI service for Civic Twin Navigator.
    Uses new Google Gen AI SDK with Gemini 2.5 Flash on Vertex AI.
    Extended thinking is DISABLED via thinking_budget=0 for speed.
    """

    def __init__(self):
        # Initialize using new Gen AI SDK with Vertex AI backend
        self.client = genai.Client(
            vertexai=True,
            project=settings.google_cloud_project_id,
            location=settings.google_cloud_location
        )

        self.model = settings.vertex_ai_model

        logger.info(f"Vertex AI Service initialized with model: {self.model}")


    def _build_config(
        self,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_instruction: Optional[str] = None
    ) -> types.GenerateContentConfig:
        """
        Build generation config with extended thinking DISABLED.
        This prevents the model from entering long reasoning loops
        which caused the Safety Agent and other agents to hang.

        Args:
            temperature: Generation temperature
            max_tokens: Max output tokens
            system_instruction: Optional system instruction

        Returns:
            GenerateContentConfig with thinking disabled
        """
        config = types.GenerateContentConfig(
            max_output_tokens=max_tokens or settings.vertex_ai_max_tokens,
            temperature=temperature or settings.vertex_ai_temperature,
            top_p=0.95,
            thinking_config=types.ThinkingConfig(
                thinking_budget=0  # Disable extended thinking for speed
            )
        )

        if system_instruction:
            config.system_instruction = system_instruction

        return config


    def _call_with_retry(
        self,
        contents: list,
        config: types.GenerateContentConfig,
        max_retries: int = 3,
        base_delay: float = 5.0
    ) -> str:
        """
        Call Vertex AI with exponential backoff retry on 429 errors.

        Args:
            contents: Message contents list
            config: Generation config
            max_retries: Maximum retry attempts
            base_delay: Base delay in seconds for backoff

        Returns:
            Generated text string
        """
        last_error = None

        for attempt in range(max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=config
                )
                if response and response.text:
                    return response.text.strip()
                return ""

            except Exception as e:
                last_error = e
                error_str = str(e)

                # Check if 429 rate limit error
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    if attempt < max_retries:
                        # Exponential backoff: 5s, 10s, 20s
                        delay = base_delay * (2 ** attempt)
                        logger.warning(
                            f"Rate limit hit (attempt {attempt + 1}/{max_retries + 1}). "
                            f"Retrying in {delay}s..."
                        )
                        time.sleep(delay)
                        continue
                    else:
                        logger.error(
                            f"Rate limit exceeded after {max_retries} retries"
                        )
                        raise Exception(
                            f"Rate limit exceeded: {error_str}"
                        )
                else:
                    # Non-rate-limit error, raise immediately
                    raise Exception(f"AI generation failed: {error_str}")

        raise Exception(f"AI generation failed after retries: {last_error}")


    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_instruction: Optional[str] = None
    ) -> str:
        """
        Generate a response from Vertex AI Gemini model.

        Args:
            prompt: User prompt text
            temperature: Override default temperature
            max_tokens: Override default max tokens
            system_instruction: Optional system instruction

        Returns:
            Generated text response as string
        """
        try:
            # Build generation config with thinking disabled
            config = self._build_config(
                temperature=temperature,
                max_tokens=max_tokens,
                system_instruction=system_instruction
            )

            # Build contents
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part(text=prompt)]
                )
            ]

            # Generate response with retry
            return self._call_with_retry(contents, config)

        except Exception as e:
            logger.error(f"Vertex AI generation error: {e}")
            raise Exception(f"AI generation failed: {str(e)}")


    def generate_structured(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Generate a structured JSON response from Vertex AI.

        Args:
            prompt: User prompt text
            system_instruction: System instruction for the model
            temperature: Override default temperature

        Returns:
            Parsed JSON as dictionary
        """
        try:
            # Add strict JSON instruction to prompt
            json_prompt = f"""
{prompt}

STRICT RULES FOR RESPONSE:
1. Return ONLY valid JSON
2. No text before or after JSON
3. No markdown code blocks like ```json
4. No trailing commas
5. All strings must use double quotes
6. Boolean values must be true or false (lowercase)
7. Null values must be null (lowercase)
"""
            # Use _build_config to ensure thinking is disabled
            config = self._build_config(
                temperature=temperature or 0.2,
                system_instruction=system_instruction
            )

            # Build contents
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part(text=json_prompt)]
                )
            ]

            # Generate response with retry
            response_text = self._call_with_retry(contents, config)

            if not response_text:
                raise Exception("Empty response from Vertex AI")

            # Clean response
            cleaned = self._clean_json_response(response_text)

            # Try to parse JSON
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                # Try to fix common issues and parse again
                fixed = self._fix_json(cleaned)
                return json.loads(fixed)

        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            raise Exception(f"Failed to parse AI response as JSON: {str(e)}")
        except Exception as e:
            logger.error(f"Structured generation error: {e}")
            raise Exception(f"Structured AI generation failed: {str(e)}")


    def generate_with_history(
        self,
        messages: List[Dict[str, str]],
        system_instruction: Optional[str] = None
    ) -> str:
        """
        Generate response with conversation history (multi-turn).

        Args:
            messages: List of {"role": "user/model", "content": "text"}
            system_instruction: System instruction for the model

        Returns:
            Generated text response
        """
        try:
            # Build config with thinking disabled
            config = self._build_config(
                system_instruction=system_instruction
            )

            # Build contents from history
            contents = []
            for msg in messages:
                role = msg["role"]
                # Vertex AI uses "model" not "assistant"
                if role == "assistant":
                    role = "model"
                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part(text=msg["content"])]
                    )
                )

            # Generate response with retry
            return self._call_with_retry(contents, config)

        except Exception as e:
            logger.error(f"Multi-turn generation error: {e}")
            raise Exception(f"Multi-turn AI generation failed: {str(e)}")


    def check_safety(self, text: str) -> Dict[str, Any]:
        """
        Check if text contains unsafe or politically biased content.

        Args:
            text: Text to check

        Returns:
            Safety assessment dictionary
        """
        try:
            safety_prompt = f"""
Analyze this text for safety issues in election information context.

Text: "{text}"

Return JSON:
{{
  "is_safe": true,
  "has_political_bias": false,
  "has_misinformation": false,
  "has_harmful_content": false,
  "risk_level": "low",
  "reason": "explanation here"
}}

IMPORTANT: Return only valid JSON. No markdown. No extra text.
"""
            result = self.generate_structured(
                prompt=safety_prompt,
                temperature=0.1
            )
            return result

        except Exception as e:
            logger.error(f"Safety check error: {e}")
            return {
                "is_safe": True,
                "has_political_bias": False,
                "has_misinformation": False,
                "has_harmful_content": False,
                "risk_level": "low",
                "reason": "Safety check unavailable"
            }


    def simplify_text(
        self,
        text: str,
        language: str = "en",
        literacy_level: str = "basic"
    ) -> str:
        """
        Simplify complex text for accessibility.

        Args:
            text: Complex text to simplify
            language: Target language code
            literacy_level: basic, intermediate, advanced

        Returns:
            Simplified text
        """
        try:
            simplify_prompt = f"""
Simplify the following text for someone with {literacy_level} literacy level.
Target language: {language}

Original text:
{text}

Rules:
- Use simple everyday words
- Keep sentences short
- Avoid jargon
- Be clear and direct
- Respond in target language if not English

Return only the simplified text, no JSON needed.
"""
            return self.generate(
                prompt=simplify_prompt,
                temperature=0.3
            )

        except Exception as e:
            logger.error(f"Text simplification error: {e}")
            return text


    def _clean_json_response(self, text: str) -> str:
        """
        Clean AI response to extract valid JSON.

        Args:
            text: Raw AI response text

        Returns:
            Cleaned JSON string
        """
        # Remove markdown code blocks
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)

        # Strip whitespace
        text = text.strip()

        # Find JSON object
        obj_match = re.search(r'\{.*\}', text, re.DOTALL)
        if obj_match:
            return obj_match.group(0).strip()

        # Find JSON array
        arr_match = re.search(r'\[.*\]', text, re.DOTALL)
        if arr_match:
            return arr_match.group(0).strip()

        return text


    def _fix_json(self, text: str) -> str:
        """
        Try to fix common JSON formatting issues.

        Args:
            text: Potentially broken JSON string

        Returns:
            Fixed JSON string
        """
        # Remove trailing commas before closing braces/brackets
        text = re.sub(r',\s*}', '}', text)
        text = re.sub(r',\s*]', ']', text)

        # Fix single quotes to double quotes
        text = re.sub(r"(?<![\\])'", '"', text)

        # Remove any control characters
        text = re.sub(r'[\x00-\x1f\x7f]', ' ', text)

        # Fix True/False/None to JSON compatible
        text = text.replace('True', 'true')
        text = text.replace('False', 'false')
        text = text.replace('None', 'null')

        return text


    def test_connection(self) -> Dict[str, Any]:
        """
        Test Vertex AI connection with a simple prompt.

        Returns:
            Connection test result
        """
        try:
            response = self.generate(
                prompt="Say exactly this: Civic Twin Navigator connected successfully!",
                temperature=0.1,
                max_tokens=50
            )
            return {
                "connected": True,
                "model": self.model,
                "project": settings.google_cloud_project_id,
                "response": response
            }
        except Exception as e:
            return {
                "connected": False,
                "model": self.model,
                "project": settings.google_cloud_project_id,
                "error": str(e)
            }


# Single instance to use across all agents
vertex_ai_service = VertexAIService()