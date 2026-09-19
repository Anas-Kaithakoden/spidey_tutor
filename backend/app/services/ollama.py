import json
import logging

import httpx

logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = "http://localhost:11434"
REQUEST_TIMEOUT = 600


def _chat_json(
    model_name: str,
    system: str,
    user: str,
    temperature: float = 0.7,
) -> dict:
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "format": "json",
        "options": {"temperature": temperature},
    }
    resp = httpx.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json=payload,
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def _robust_parse(raw: str) -> dict:
    """Try to extract JSON from text that may contain markdown fences etc."""
    text = raw.strip()
    # strip ```json fences
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # find first { to last }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            pass
    raise ValueError(f"Could not parse JSON from LLM response: {text[:200]}")


def generate_quiz(
    material_text: str,
    difficulty: str,
    question_count: int,
    model_name: str,
    max_material_chars: int = 40000,
) -> list[dict]:
    truncated = material_text[:max_material_chars]

    system = (
        "You are a quiz generator for a study tool.\n"
        f"Create exactly {question_count} multiple-choice questions.\n"
        f"Difficulty: {difficulty}\n"
        "Rules:\n"
        "- Each question must have exactly 4 options, with exactly one correct answer.\n"
        "- Keep language clear, simple, and accurate to the material.\n"
        "- For \"easy\", test basic recall. For \"medium\", test understanding. For \"hard\", test analysis and application.\n"
        "- Provide a short 1-2 sentence explanation for each answer.\n"
        'Respond with STRICT JSON only matching: '
        '{"questions": [{"question": string, "options": [string x4], '
        '"correct_answer": int (index of the correct option), "explanation": string}]}'
    )
    raw = _chat_json(model_name, system, f"Study material:\n{truncated}")
    data = _robust_parse(raw)
    return data.get("questions", [])[:question_count]


def generate_flashcards(
    material_text: str,
    count: int,
    model_name: str,
    max_material_chars: int = 40000,
) -> list[dict]:
    truncated = material_text[:max_material_chars]

    system = (
        "You are a study assistant.\n"
        f"Create {count} flashcards covering the most important concepts, definitions, and facts.\n"
        "Rules:\n"
        "- Front: a concise question or prompt.\n"
        "- Back: a clear answer or definition (1-3 sentences).\n"
        'Respond with STRICT JSON only matching: '
        '{"flashcards": [{"front": string, "back": string}]}'
    )
    raw = _chat_json(model_name, system, f"Study material:\n{truncated}")
    data = _robust_parse(raw)
    return data.get("flashcards", [])[:count]


def generate_study_notes(
    material_text: str,
    model_name: str,
    max_material_chars: int = 40000,
) -> dict:
    truncated = material_text[:max_material_chars]

    system = (
        "You are a study notes generator for a study tool.\n"
        "Create structured, student-friendly study notes from the material.\n"
        "Rules:\n"
        "- Base the notes ONLY on the provided material; do not invent unrelated information.\n"
        "- Organize the content into logical topics/sections with clear headings.\n"
        "- Keep explanations concise and clear.\n"
        "- Use bullet points where listing facts, steps, or examples helps.\n"
        "- Highlight the most important concepts and definitions in key_concepts.\n"
        'Respond with STRICT JSON only matching: '
        '{"title": string, "summary": string, '
        '"sections": [{"heading": string, "content": string, "bullet_points": [string]}], '
        '"key_concepts": [{"term": string, "definition": string}]}'
    )
    raw = _chat_json(model_name, system, f"Study material:\n{truncated}")
    return _robust_parse(raw)


def _chat_text(
    model_name: str,
    system: str,
    user: str,
    temperature: float = 0.3,
) -> str:
    """Free-form chat completion (no forced JSON format)."""
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "options": {"temperature": temperature},
    }
    resp = httpx.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json=payload,
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    return str(resp.json()["message"]["content"]).strip()


def generate_chat_reply(
    material_text: str,
    history: list[dict],
    model_name: str,
    max_material_chars: int = 40000,
) -> str:
    """Answer the last user message, grounded in the study material."""

    truncated = material_text[:max_material_chars]

    system = (
        "You are a study assistant that answers questions strictly based "
        "ONLY on the uploaded study material provided to you.\n"
        "Rules:\n"
        "- Answer ONLY from the study material. Do not use outside or "
        "general knowledge as if it came from the material.\n"
        "- If the material does not contain enough information to answer, "
        "say clearly that the answer is not available in the uploaded "
        "material — never invent an answer.\n"
        "- Follow-up questions may refer back to earlier messages or to the "
        "material.\n"
        "- Keep answers concise and clear.\n"
    )
    conversation = "\n".join(
        f"{m['role']}: {m['content']}" for m in history
    )
    return _chat_text(
        model_name,
        system,
        f"Conversation so far (newest last):\n{conversation}\n\n"
        f"Study material:\n{truncated}",
    )


def available_models() -> list[dict]:
    """Query Ollama for available models."""
    try:
        resp = httpx.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        resp.raise_for_status()
        models = resp.json().get("models", [])
        return [
            {"provider": "ollama", "name": m["name"], "label": m["name"]}
            for m in models
        ]
    except Exception:
        logger.debug("Ollama unreachable")
        return []


def generate_json(
    system: str, user: str, model_name: str, temperature: float = 0.3
) -> dict:
    """Generic strict-JSON completion (used by Exam Mode prompts)."""
    raw = _chat_json(model_name, system, user, temperature=temperature)
    return _robust_parse(raw)