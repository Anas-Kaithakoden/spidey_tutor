import logging

from app.config import settings
from app.seed import MOCK_FLASHCARDS, MOCK_QUESTIONS, MOCK_STUDY_NOTES
from app.services import gemini, ollama, quick

logger = logging.getLogger(__name__)

# deprecated models that now 404 - auto-fix to current
DEPRECATED_MODELS = {
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.5-flash-lite",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-2.0-flash-lite",
    "gemini-pro-latest",
    "",
}


def _fix_model(name: str) -> str:
    if not name or name in DEPRECATED_MODELS:
        return settings.gemini_model
    return name


def _normalize_question(item: dict) -> dict:
    question = str(item.get("question", "")).strip()
    options = item.get("options", [])
    if not isinstance(options, list) or len(options) < 2:
        raise ValueError("Invalid options")
    correct = item.get("correct_answer", item.get("correctAnswer", -1))
    if not isinstance(correct, int) or not (0 <= correct < len(options)):
        raise ValueError("Invalid correct answer")
    explanation = str(item.get("explanation", "")).strip()
    return {
        "question": question,
        "options": [str(o) for o in options],
        "correct_answer": correct,
        "explanation": explanation,
    }


def _normalize_flashcard(item: dict) -> dict:
    front = str(item.get("front", item.get("question", ""))).strip()
    back = str(item.get("back", item.get("answer", ""))).strip()
    if not front or not back:
        raise ValueError("Invalid flashcard")
    return {"front": front, "back": back}


def generate_quiz(
    material_text: str,
    difficulty: str,
    question_count: int,
    provider: str = "gemini",
    model_name: str = "",
) -> tuple[str, list[dict]]:
    """Generate quiz questions. Returns (generated_by, questions)."""
    try:
        success_tag = "ai"
        if provider == "quick":
            raw = quick.generate_quiz(
                material_text, difficulty, question_count
            )
            success_tag = "quick"
        elif provider == "ollama":
            name = model_name or "qwen3:8b"
            raw = ollama.generate_quiz(material_text, difficulty, question_count, name)
        elif provider == "gemini":
            name = _fix_model(model_name) if model_name else settings.gemini_model
            raw = gemini.generate_quiz_raw(material_text, difficulty, question_count, name)
        else:
            raise ValueError(f"Unknown provider: {provider}")

        questions = [_normalize_question(q) for q in raw]
        if not questions:
            raise ValueError("No questions generated")
        return success_tag, questions

    except Exception as exc:
        logger.exception(
            "Quiz generation failed (provider=%s, model=%s): %s",
            provider, model_name, exc,
        )
        return "mock", [dict(q) for q in MOCK_QUESTIONS[:question_count]]


def generate_flashcards(
    material_text: str,
    count: int = 8,
    provider: str = "gemini",
    model_name: str = "",
) -> tuple[str, list[dict]]:
    """Generate flashcards. Returns (generated_by, flashcards)."""
    try:
        success_tag = "ai"
        if provider == "quick":
            raw = quick.generate_flashcards(material_text, count)
            success_tag = "quick"
        elif provider == "ollama":
            name = model_name or "qwen3:8b"
            raw = ollama.generate_flashcards(material_text, count, name)
        elif provider == "gemini":
            name = _fix_model(model_name) if model_name else settings.gemini_model
            raw = gemini.generate_flashcards_raw(material_text, count, name)
        else:
            raise ValueError(f"Unknown provider: {provider}")

        cards = [_normalize_flashcard(c) for c in raw]
        if not cards:
            raise ValueError("No flashcards generated")
        return success_tag, cards

    except Exception as exc:
        logger.exception(
            "Flashcard generation failed (provider=%s, model=%s): %s",
            provider, model_name, exc,
        )
        return "mock", [dict(c) for c in MOCK_FLASHCARDS[:count]]


def _normalize_study_notes(item: dict) -> dict:
    title = str(item.get("title", "Study Notes")).strip() or "Study Notes"
    summary = str(item.get("summary", "")).strip()

    sections = []
    for s in item.get("sections", []):
        if not isinstance(s, dict):
            continue
        heading = str(s.get("heading", "")).strip()
        content = str(s.get("content", "")).strip()
        bullet_points = [
            str(b).strip()
            for b in s.get("bullet_points", [])
            if str(b).strip()
        ]
        if not heading and not content and not bullet_points:
            continue
        sections.append(
            {
                "heading": heading,
                "content": content,
                "bullet_points": bullet_points,
            }
        )

    key_concepts = []
    for kc in item.get("key_concepts", []):
        if not isinstance(kc, dict):
            continue
        term = str(kc.get("term", "")).strip()
        definition = str(kc.get("definition", "")).strip()
        if term and definition:
            key_concepts.append({"term": term, "definition": definition})

    if not sections and not key_concepts:
        raise ValueError("Invalid study notes")

    return {
        "title": title,
        "summary": summary,
        "sections": sections,
        "key_concepts": key_concepts,
    }


def generate_study_notes(
    material_text: str,
    provider: str = "gemini",
    model_name: str = "",
) -> tuple[str, dict]:
    """Generate study notes. Returns (generated_by, notes dict)."""
    try:
        success_tag = "ai"
        if provider == "quick":
            raw = quick.generate_study_notes(material_text)
            success_tag = "quick"
        elif provider == "ollama":
            name = model_name or "qwen3:8b"
            raw = ollama.generate_study_notes(material_text, name)
        elif provider == "gemini":
            name = _fix_model(model_name) if model_name else settings.gemini_model
            raw = gemini.generate_study_notes_raw(material_text, name)
        else:
            raise ValueError(f"Unknown provider: {provider}")

        notes = _normalize_study_notes(raw)
        return success_tag, notes

    except Exception as exc:
        logger.exception(
            "Study notes generation failed (provider=%s, model=%s): %s",
            provider, model_name, exc,
        )
        return "mock", dict(MOCK_STUDY_NOTES)


def generate_chat_reply(
    material_text: str,
    history: list[dict],
    provider: str = "gemini",
    model_name: str = "",
) -> tuple[str, str]:
    """Generate a chat reply grounded in the material.

    ``history`` is the conversation so far (oldest first, ending with the
    current user question) as ``{"role": ..., "content": ...}`` dicts.
    Returns (generated_by, reply_text).

    The fallback deliberately reuses ``quick.generate_chat_reply`` (rather
    than generic ``seed.py`` content): a chat answer about a specific upload
    must never surface unrelated general knowledge as if it came from the
    material, so even mock replies stay grounded in the text.
    """
    try:
        success_tag = "ai"
        if provider == "quick":
            raw = quick.generate_chat_reply(material_text, history)
            success_tag = "quick"
        elif provider == "ollama":
            name = model_name or "qwen3:8b"
            raw = ollama.generate_chat_reply(material_text, history, name)
        elif provider == "gemini":
            name = _fix_model(model_name) if model_name else settings.gemini_model
            raw = gemini.generate_chat_reply_raw(material_text, history, name)
        else:
            raise ValueError(f"Unknown provider: {provider}")

        reply = str(raw).strip()
        if not reply:
            raise ValueError("Empty chat reply")
        return success_tag, reply

    except Exception as exc:
        logger.exception(
            "Chat reply generation failed (provider=%s, model=%s): %s",
            provider, model_name, exc,
        )
        return "mock", quick.generate_chat_reply(material_text, history)