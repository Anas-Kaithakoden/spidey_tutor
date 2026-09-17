import json
import logging

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

_client_instance: genai.Client | None = None


def _client() -> genai.Client:
    from app.config import settings

    global _client_instance
    if _client_instance is None:
        _client_instance = genai.Client(api_key=settings.gemini_api_key)
    return _client_instance


def generate_quiz_raw(
    material_text: str,
    difficulty: str,
    question_count: int,
    model_name: str,
) -> list[dict]:
    """Call Gemini and return raw quiz dicts (no normalization)."""
    prompt = (
        f"You are a quiz generator for a study tool.\n"
        f"Create exactly {question_count} multiple-choice questions.\n\n"
        f"Difficulty: {difficulty}\n"
        "Rules:\n"
        "- Each question must have exactly 4 options, with exactly one correct answer.\n"
        "- Keep language clear, simple, and accurate to the material.\n"
        "- For \"easy\", test basic recall. For \"medium\", test understanding. For \"hard\", test analysis and application.\n"
        "- Provide a short 1-2 sentence explanation for each answer.\n\n"
        "Respond with STRICT JSON only, matching this schema:\n"
        '{"questions": [{"question": string, "options": [string × 4], '
        '"correct_answer": int, "explanation": string}]}\n\n'
        f"Study material:\n{material_text[:40000]}"
    )
    response = _client().models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.7,
        ),
    )
    data = json.loads(response.text)
    return data.get("questions", [])[:question_count]


def generate_flashcards_raw(
    material_text: str,
    count: int,
    model_name: str,
) -> list[dict]:
    """Call Gemini and return raw flashcard dicts (no normalization)."""
    prompt = (
        f"You are a study assistant.\n"
        f"Create {count} flashcards covering the most important concepts, definitions, and facts.\n\n"
        "Rules:\n"
        "- Front: a concise question or prompt.\n"
        "- Back: a clear answer or definition (1-3 sentences).\n\n"
        "Respond with STRICT JSON only, matching this schema:\n"
        '{"flashcards": [{"front": string, "back": string}]}\n\n'
        f"Study material:\n{material_text[:40000]}"
    )
    response = _client().models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.7,
        ),
    )
    data = json.loads(response.text)
    return data.get("flashcards", [])[:count]