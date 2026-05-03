from google.cloud import texttospeech
from google.cloud import speech
from typing import Dict, Any, Optional
import logging
import base64

from config.settings import settings

# Setup logging
logger = logging.getLogger(__name__)


class SpeechService:
    """
    Google Cloud Speech service for Civic Twin Navigator.
    Handles Text-to-Speech and Speech-to-Text for voice interaction.
    """

    # Voice configs per language
    VOICE_CONFIGS = {
        "en": {"language_code": "en-IN", "name": "en-IN-Standard-A"},
        "hi": {"language_code": "hi-IN", "name": "hi-IN-Standard-A"},
        "mr": {"language_code": "mr-IN", "name": "mr-IN-Standard-A"},
        "ta": {"language_code": "ta-IN", "name": "ta-IN-Standard-A"},
        "te": {"language_code": "te-IN", "name": "te-IN-Standard-A"},
        "kn": {"language_code": "kn-IN", "name": "kn-IN-Standard-A"},
        "ml": {"language_code": "ml-IN", "name": "ml-IN-Standard-A"},
        "gu": {"language_code": "gu-IN", "name": "gu-IN-Standard-A"},
        "bn": {"language_code": "bn-IN", "name": "bn-IN-Standard-A"},
    }

    def __init__(self):
        try:
            # Initialize TTS client with ADC
            self.tts_client = texttospeech.TextToSpeechClient()

            # Initialize STT client with ADC
            self.stt_client = speech.SpeechClient()

            logger.info("Speech Service initialized successfully")

        except Exception as e:
            logger.error(f"Speech initialization error: {e}")
            raise Exception(f"Speech setup failed: {str(e)}")


    def text_to_speech(
        self,
        text: str,
        language: str = "en",
        speaking_rate: float = 0.9,
        pitch: float = 0.0
    ) -> Dict[str, Any]:
        """
        Convert text to speech audio.

        Args:
            text: Text to convert to speech
            language: Language code
            speaking_rate: Speed of speech (0.25 to 4.0)
            pitch: Voice pitch (-20.0 to 20.0)

        Returns:
            Audio content as base64 encoded string
        """
        try:
            # Get voice config for language
            voice_config = self.VOICE_CONFIGS.get(
                language,
                self.VOICE_CONFIGS["en"]
            )

            # Set input text
            synthesis_input = texttospeech.SynthesisInput(text=text)

            # Set voice parameters
            voice = texttospeech.VoiceSelectionParams(
                language_code=voice_config["language_code"],
                name=voice_config["name"],
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )

            # Set audio config
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=speaking_rate,
                pitch=pitch
            )

            # Generate speech
            response = self.tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            # Encode to base64
            audio_base64 = base64.b64encode(
                response.audio_content
            ).decode("utf-8")

            return {
                "success": True,
                "audio_base64": audio_base64,
                "language": language,
                "format": "mp3",
                "text_length": len(text)
            }

        except Exception as e:
            logger.error(f"Text to speech error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


    def speech_to_text(
        self,
        audio_base64: str,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Convert speech audio to text.

        Args:
            audio_base64: Base64 encoded audio content
            language: Expected language code

        Returns:
            Transcribed text
        """
        try:
            # Decode base64 audio
            audio_bytes = base64.b64decode(audio_base64)

            # Get language code
            voice_config = self.VOICE_CONFIGS.get(
                language,
                self.VOICE_CONFIGS["en"]
            )
            language_code = voice_config["language_code"]

            # Create audio object
            audio = speech.RecognitionAudio(content=audio_bytes)

            # Configure recognition
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.MP3,
                sample_rate_hertz=16000,
                language_code=language_code,
                enable_automatic_punctuation=True,
                model="latest_long"
            )

            # Recognize speech
            response = self.stt_client.recognize(
                config=config,
                audio=audio
            )

            # Extract transcript
            transcript = ""
            confidence = 0.0

            for result in response.results:
                transcript += result.alternatives[0].transcript
                confidence = result.alternatives[0].confidence

            return {
                "success": True,
                "transcript": transcript,
                "confidence": confidence,
                "language": language
            }

        except Exception as e:
            logger.error(f"Speech to text error: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcript": ""
            }


    def test_connection(self) -> Dict[str, Any]:
        """Test Speech service TTS connection"""
        try:
            result = self.text_to_speech(
                text="Civic Twin Navigator voice service connected.",
                language="en"
            )
            if result["success"]:
                return {
                    "connected": True,
                    "message": "TTS working successfully",
                    "audio_size": len(result["audio_base64"])
                }
            return {
                "connected": False,
                "error": result.get("error")
            }
        except Exception as e:
            return {
                "connected": False,
                "error": str(e)
            }


# Single instance
speech_service = SpeechService()