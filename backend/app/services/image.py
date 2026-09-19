import logging

from app.config import settings
from app.services import gemini

logger = logging.getLogger(__name__)

# Supported image mimes for Gemini vision
IMAGE_MIMES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
}


def extract_image_text(data: bytes, filename: str = "image") -> str:
    """Extract text from image bytes using Gemini vision (no local OCR deps)."""
    if not settings.gemini_api_key:
        raise ValueError("Image OCR needs GEMINI_API_KEY. Add it to backend/.env.")

    # detect mime from extension
    lower = filename.lower()
    mime = "image/png"
    for ext, m in IMAGE_MIMES.items():
        if lower.endswith(ext):
            mime = m
            break

    # Gemini vision: send image + prompt to extract verbatim text
    try:
        from google.genai import types

        client = gemini._client()
        # Use flash-latest which supports vision (per list we saw gemini-flash-latest works)
        model = settings.gemini_model  # now gemini-3-flash-preview which supports vision
        prompt = (
            "Extract all readable text from this image verbatim. "
            "Return plain text only, preserve paragraphs and line breaks. "
            "If no text is found, describe the image content briefly in 2-3 sentences."
        )
        # content can be list of parts
        image_part = types.Part.from_bytes(data=data, mime_type=mime)
        resp = client.models.generate_content(
            model=model,
            contents=[image_part, prompt],
            config=types.GenerateContentConfig(temperature=0.2),
        )
        text = (resp.text or "").strip()
        if not text:
            raise ValueError("No text could be extracted from this image.")
        return text
    except Exception as exc:
        logger.exception("Image OCR failed (%s): %s", filename, exc)
        raise ValueError(f"Could not extract text from image: {exc}") from exc
