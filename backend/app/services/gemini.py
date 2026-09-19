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


def generate_study_notes_raw(
    material_text: str,
    model_name: str,
) -> dict:
    """Call Gemini and return raw study-notes dict (no normalization)."""
    prompt = (
        "You are a study notes generator for a study tool.\n"
        "Create structured, student-friendly study notes from the material.\n\n"
        "Rules:\n"
        "- Base the notes ONLY on the provided material; do not invent unrelated information.\n"
        "- Organize the content into logical topics/sections with clear headings.\n"
        "- Keep explanations concise and clear.\n"
        "- Use bullet points where listing facts, steps, or examples helps.\n"
        "- Highlight the most important concepts and definitions in key_concepts.\n\n"
        "Respond with STRICT JSON only, matching this schema:\n"
        '{"title": string, "summary": string, '
        '"sections": [{"heading": string, "content": string, "bullet_points": [string]}], '
        '"key_concepts": [{"term": string, "definition": string}]}\n\n'
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
    return json.loads(response.text)


def generate_chat_reply_raw(
    material_text: str,
    history: list[dict],
    model_name: str,
) -> str:
    """Call Gemini and return a grounded answer to the last user message.

    ``history`` is the conversation so far (oldest first, ending with the
    current user question) as ``{"role": ..., "content": ...}`` dicts.
    """
    prompt = (
        "You are a study assistant that answers questions strictly based "
        "ONLY on the uploaded study material provided below.\n\n"
        "Rules:\n"
        "- Answer ONLY from the study material. Do not use outside or "
        "general knowledge as if it came from the material.\n"
        "- If the material does not contain enough information to answer, "
        "say clearly that the answer is not available in the uploaded "
        "material — never invent an answer.\n"
        "- Follow-up questions may refer back to earlier messages or to the "
        "material.\n"
        "- Keep answers concise, clear, and in the same language as the "
        "question.\n\n"
        "Conversation so far (newest last):\n"
    )
    for m in history:
        prompt += f"{m['role']}: {m['content']}\n"
    prompt += f"\nStudy material:\n{material_text[:40000]}"

    response = _client().models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.3),
    )
    return response.text.strip()