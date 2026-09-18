import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Material
from app.schemas import AudioSummaryOut, CreateAudioSummary
from app.services.audio import generate_summary_text, generate_tts_audio

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/audio", tags=["audio"])


@router.post("/summary", response_model=AudioSummaryOut)
def create_audio_summary(payload: CreateAudioSummary, db: Session = Depends(get_db)):
    material = db.get(Material, payload.material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found.")
    if not material.content or not material.content.strip():
        raise HTTPException(status_code=422, detail="Material has no content.")

    # 1) Generate 1-min summary text (uses gemini or ollama, falls back to mock)
    generated_by, summary_text = generate_summary_text(
        material.content,
        provider=payload.provider,
        model_name=payload.model_name,
        language=payload.language,
    )

    # 2) Generate audio via Gemini TTS — simple, no DB, no file storage
    # If no API key or TTS fails, we still return text so frontend can use browser TTS
    mime_type = "audio/wav"
    audio_b64 = ""
    tts_provider = payload.provider
    tts_model = payload.model_name or settings.gemini_model

    try:
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not set — TTS unavailable")

        mime_type, audio_b64, tts_generated = generate_tts_audio(
            summary_text, voice_name=payload.voice_name, language=payload.language
        )
        # if TTS succeeded, mark as ai even if summary was mock
        if tts_generated == "ai":
            generated_by = "ai"
    except Exception as exc:
        logger.warning("TTS fallback to text-only: %s", exc)
        # keep summary_text, return empty audio so frontend uses browser speech
        # don't fail the whole request — user still gets 1-min summary
        audio_b64 = ""
        mime_type = "audio/wav"
        # generated_by stays as from summary step (ai or mock)

    return AudioSummaryOut(
        material_id=material.id,
        summary_text=summary_text,
        audio_base64=audio_b64,
        mime_type=mime_type,
        generated_by=generated_by,
        provider=tts_provider,
        model_name=tts_model,
    )
