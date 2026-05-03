from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import logging

from services.translation_service import translation_service
from utils.helpers import build_response
from utils.validators import validate_translation_text, validate_translation_batch

logger = logging.getLogger(__name__)

router = APIRouter()


class TranslateRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = "en"


class TranslateBatchRequest(BaseModel):
    texts: List[str]
    target_language: str
    source_language: Optional[str] = "en"


@router.post("")
async def translate_text(request: TranslateRequest):
    """Translate text to target language."""
    try:
        # Validate input length
        is_valid, error_msg = validate_translation_text(request.text)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        if request.target_language == request.source_language:
            return build_response(
                success=True,
                data={
                    "original_text": request.text,
                    "translated_text": request.text,
                    "target_language": request.target_language,
                },
                message="Same language, no translation needed"
            )

        result = translation_service.translate_text(
            text=request.text,
            target_language=request.target_language,
            source_language=request.source_language
        )

        if result.get("success"):
            return build_response(
                success=True,
                data={
                    "original_text": request.text,
                    "translated_text": result.get("translated_text", request.text),
                    "target_language": request.target_language,
                    "language_name": result.get("language_name", ""),
                },
                message="Translation successful"
            )
        else:
            return build_response(
                success=True,
                data={
                    "original_text": request.text,
                    "translated_text": request.text,
                    "target_language": request.target_language,
                },
                message="Translation failed, returning original"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return build_response(
            success=True,
            data={
                "original_text": request.text,
                "translated_text": request.text,
                "target_language": request.target_language,
            },
            message="Translation unavailable"
        )


@router.post("/batch")
async def translate_batch(request: TranslateBatchRequest):
    """Translate multiple texts at once."""
    try:
        # Validate batch input
        is_valid, error_msg = validate_translation_batch(request.texts)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        if request.target_language == request.source_language:
            return build_response(
                success=True,
                data={
                    "translations": [
                        {"original": t, "translated": t}
                        for t in request.texts
                    ],
                    "target_language": request.target_language,
                },
                message="Same language, no translation needed"
            )

        results = translation_service.translate_batch(
            texts=request.texts,
            target_language=request.target_language,
            source_language=request.source_language
        )

        translations = []
        for r in results:
            translations.append({
                "original": r.get("original_text", ""),
                "translated": r.get("translated_text", r.get("original_text", "")),
            })

        return build_response(
            success=True,
            data={
                "translations": translations,
                "target_language": request.target_language,
            },
            message="Batch translation complete"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch translation error: {e}")
        return build_response(
            success=True,
            data={
                "translations": [
                    {"original": t, "translated": t}
                    for t in request.texts
                ],
                "target_language": request.target_language,
            },
            message="Translation unavailable"
        )