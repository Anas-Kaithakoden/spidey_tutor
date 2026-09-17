import logging

from app.config import settings
from app.seed import MOCK_FLASHCARDS, MOCK_QUESTIONS, MOCK_STUDY_NOTES
from app.services import gemini, ollama

logger = logging.getLogger(__name__)


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
        if provider == "ollama":
            name = model_name or "qwen3:8b"
            raw = ollama.generate_quiz(material_text, difficulty, question_count, name)
        elif provider == "gemini":
            name = model_name or settings.gemini_model
            raw = gemini.generate_quiz_raw(material_text, difficulty, question_count, name)
        else:
            raise ValueError(f"Unknown provider: {provider}")

        questions = [_normalize_question(q) for q in raw]
        if not questions:
            raise ValueError("No questions generated")
        return "ai", questions

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
        if provider == "ollama":
            name = model_name or "qwen3:8b"
            raw = ollama.generate_flashcards(material_text, count, name)
        elif provider == "gemini":
            name = model_name or settings.gemini_model
            raw = gemini.generate_flashcards_raw(material_text, count, name)
        else:
            raise ValueError(f"Unknown provider: {provider}")

        cards = [_normalize_flashcard(c) for c in raw]
        if not cards:
            raise ValueError("No flashcards generated")
        return "ai", cards

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
        if provider == "ollama":
            name = model_name or "qwen3:8b"
            raw = ollama.generate_study_notes(material_text, name)
        elif provider == "gemini":
            name = model_name or settings.gemini_model
            raw = gemini.generate_study_notes_raw(material_text, name)
        else:
            raise ValueError(f"Unknown provider: {provider}")

        notes = _normalize_study_notes(raw)
        return "ai", notes

    except Exception as exc:
        logger.exception(
            "Study notes generation failed (provider=%s, model=%s): %s",
            provider, model_name, exc,
        )
        return "mock", dict(MOCK_STUDY_NOTES)