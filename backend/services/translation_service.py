from google.cloud import translate_v2 as translate
from typing import Dict, Any, List, Optional
import logging

from config.settings import settings

# Setup logging
logger = logging.getLogger(__name__)


class TranslationService:
    """
    Google Cloud Translation service for Civic Twin Navigator.
    Handles multilingual support for all Indian languages.
    """

    # Supported Indian languages
    SUPPORTED_LANGUAGES = {
        "en": "English",
        "hi": "Hindi",
        "mr": "Marathi",
        "ta": "Tamil",
        "te": "Telugu",
        "kn": "Kannada",
        "ml": "Malayalam",
        "gu": "Gujarati",
        "bn": "Bengali",
        "pa": "Punjabi",
        "or": "Odia",
        "as": "Assamese"
    }

    def __init__(self):
        try:
            # Initialize with ADC
            self.client = translate.Client()
            logger.info("Translation Service initialized successfully")
        except Exception as e:
            logger.error(f"Translation initialization error: {e}")
            raise Exception(f"Translation setup failed: {str(e)}")


    def translate_text(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Translate text to target language.

        Args:
            text: Text to translate
            target_language: Target language code (hi, mr, ta etc)
            source_language: Source language code (auto-detect if None)

        Returns:
            Translation result dictionary
        """
        try:
            if not text or not text.strip():
                return {
                    "success": False,
                    "error": "Empty text provided"
                }

            # Skip translation if already in target language
            if source_language == target_language:
                return {
                    "success": True,
                    "original_text": text,
                    "translated_text": text,
                    "source_language": source_language,
                    "target_language": target_language
                }

            # Translate
            result = self.client.translate(
                text,
                target_language=target_language,
                source_language=source_language
            )

            return {
                "success": True,
                "original_text": text,
                "translated_text": result["translatedText"],
                "source_language": result.get("detectedSourceLanguage",
                                               source_language or "en"),
                "target_language": target_language,
                "language_name": self.SUPPORTED_LANGUAGES.get(
                    target_language, target_language
                )
            }

        except Exception as e:
            logger.error(f"Translation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "original_text": text,
                "translated_text": text  # Return original on failure
            }


    def translate_batch(
        self,
        texts: List[str],
        target_language: str,
        source_language: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Translate multiple texts at once.

        Args:
            texts: List of texts to translate
            target_language: Target language code
            source_language: Source language code

        Returns:
            List of translation results
        """
        try:
            if not texts:
                return []

            results = self.client.translate(
                texts,
                target_language=target_language,
                source_language=source_language
            )

            return [
                {
                    "success": True,
                    "original_text": texts[i],
                    "translated_text": result["translatedText"],
                    "target_language": target_language
                }
                for i, result in enumerate(results)
            ]

        except Exception as e:
            logger.error(f"Batch translation error: {e}")
            return [
                {
                    "success": False,
                    "original_text": text,
                    "translated_text": text,
                    "error": str(e)
                }
                for text in texts
            ]


    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of input text.

        Args:
            text: Text to detect language of

        Returns:
            Detection result with language code and confidence
        """
        try:
            result = self.client.detect_language(text)

            return {
                "success": True,
                "language_code": result["language"],
                "language_name": self.SUPPORTED_LANGUAGES.get(
                    result["language"], result["language"]
                ),
                "confidence": result.get("confidence", 0)
            }

        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return {
                "success": False,
                "language_code": "en",
                "language_name": "English",
                "error": str(e)
            }


    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get all supported languages.

        Returns:
            Dictionary of language codes and names
        """
        return self.SUPPORTED_LANGUAGES


    def test_connection(self) -> Dict[str, Any]:
        """Test Translation service connection"""
        try:
            result = self.translate_text(
                text="Hello, I want to vote.",
                target_language="hi"
            )
            if result["success"]:
                return {
                    "connected": True,
                    "test_translation": result["translated_text"],
                    "target_language": "Hindi"
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
translation_service = TranslationService()