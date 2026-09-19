import json
import logging
from dataclasses import dataclass

import httpx

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 600


class ProviderError(RuntimeError):
    """A provider request failed.

    ``user_message`` is a safe, end-user-friendly reason (no keys/URLs) that
    the dispatcher can surface in the UI alongside the mock-data fallback.
    """

    def __init__(self, message: str, *, user_message: str | None = None):
        super().__init__(message)
        self.user_message = user_message or message


@dataclass
class CompatConfig:
    """Everything an OpenAI-compatible provider needs, bundled in one place.

    A new OpenAI-compatible provider is just a new module that builds one of
    these (base URL + key + default model) and reuses the functions below.
    """

    provider: str
    base_url: str
    api_key: str
    default_model: str


def _error_message(status_code: int, body: str) -> str:
    """Best-effort human-readable message from an API error body."""
    try:
        data = json.loads(body)
        err = data.get("error", data)
        if isinstance(err, dict):
            msg = err.get("message") or err.get("detail") or ""
            code = err.get("code") or err.get("type") or ""
            return f"{code}: {msg}".strip(": ") or f"HTTP {status_code}"
    except (json.JSONDecodeError, AttributeError, TypeError):
        pass
    return f"HTTP {status_code}"


def _badge_error(
    status_code: int, body: str, *, provider: str, model: str
) -> ProviderError:
    """Map an HTTP status to a useful, user-facing ProviderError."""
    detail = _error_message(status_code, body)
    if status_code == 401:
        return ProviderError(
            f"{provider} rejected the API key (HTTP 401): {detail}",
            user_message=f"{provider} rejected your API key — check {provider.upper()}_API_KEY in backend/.env.",
        )
    if status_code == 429:
        return ProviderError(
            f"{provider} rate limited the request (HTTP 429): {detail}",
            user_message=f"{provider} is rate-limiting requests right now — wait a moment and retry.",
        )
    if status_code in (400, 404):
        # 400 often means the model doesn't support JSON mode; 404 = unknown model
        return ProviderError(
            f"{provider} rejected request for model '{model}' (HTTP {status_code}): {detail}",
            user_message=f"Model '{model}' is unavailable on {provider} or the request was rejected — pick another model.",
        )
    return ProviderError(
        f"{provider} returned an error (HTTP {status_code}): {detail}",
        user_message=f"{provider} failed to generate (HTTP {status_code}) — try again shortly.",
    )


def chat_completion(
    cfg: CompatConfig,
    model: str,
    system: str,
    user: str,
    *,
    temperature: float = 0.7,
    json_object: bool = False,
    timeout: float = DEFAULT_TIMEOUT,
) -> str:
    """Call an OpenAI-compatible ``/chat/completions`` endpoint.

    Returns the raw text content of the first completion, or raises
    ``ProviderError`` with a user-safe message.
    """
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "temperature": temperature,
    }
    if json_object:
        payload["response_format"] = {"type": "json_object"}

    headers = {
        "Authorization": f"Bearer {cfg.api_key}",
        "Content-Type": "application/json",
    }

    try:
        resp = httpx.post(
            f"{cfg.base_url}/chat/completions",
            json=payload,
            headers=headers,
            timeout=timeout,
        )
    except httpx.TimeoutException as exc:
        raise ProviderError(
            f"{cfg.provider} timed out after {int(timeout)}s",
            user_message=f"{cfg.provider} took too long to respond — try a faster model.",
        ) from exc
    except httpx.HTTPError as exc:
        raise ProviderError(
            f"{cfg.provider} is unreachable: {exc}",
            user_message=f"Could not reach {cfg.provider} — check your network and try again.",
        ) from exc

    if resp.status_code >= 400:
        raise _badge_error(
            resp.status_code,
            resp.text,
            provider=cfg.provider,
            model=model,
        )

    try:
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        raise ProviderError(
            f"{cfg.provider} returned a malformed completion response: {exc}",
            user_message=f"{cfg.provider} returned an unreadable response — try again.",
        ) from exc

    if not str(content).strip():
        raise ProviderError(
            f"{cfg.provider} returned an empty completion for model '{model}'.",
            user_message=f"{cfg.provider} returned an empty answer for model '{model}' — pick another model.",
        )
    return str(content)


def _unsupported_json_mode(exc: ProviderError) -> bool:
    """True when the provider/model told us it can't do json_object mode."""
    haystack = (f"{exc} {exc.user_message}").lower()
    return any(
        token in haystack
        for token in ("response_format", "json_object", "json mode", "structured outputs")
    )


def _extract_json(raw: str) -> dict:
    """Robustly parse JSON out of a completion that may add prose/fences."""
    text = raw.strip()
    if text.startswith("```"):
        lines = [l for l in text.split("\n") if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            pass
    raise ProviderError(
        f"Could not parse JSON from completion: {raw[:200]}",
        user_message="The model's response was not valid JSON — try again or pick another model.",
    )


def chat_json(
    cfg: CompatConfig,
    model: str,
    system: str,
    user: str,
    *,
    temperature: float = 0.7,
) -> dict:
    """JSON completion with graceful fallback when the model lacks JSON mode."""
    try:
        raw = chat_completion(
            cfg,
            model,
            system,
            user,
            temperature=temperature,
            json_object=True,
        )
    except ProviderError as exc:
        if _unsupported_json_mode(exc):
            # model genuinely can't do json_object mode (e.g. some free models)
            raw = chat_completion(
                cfg,
                model,
                system,
                user,
                temperature=temperature,
                json_object=False,
            )
        else:
            raise
    return _extract_json(raw)


def chat_text(
    cfg: CompatConfig,
    model: str,
    system: str,
    user: str,
    *,
    temperature: float = 0.3,
) -> str:
    """Free-form completion (no JSON format)."""
    return chat_completion(
        cfg, model, system, user, temperature=temperature, json_object=False
    )


def generate_quiz(
    cfg: CompatConfig,
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
    data = chat_json(cfg, model_name, system, f"Study material:\n{truncated}")
    return data.get("questions", [])[:question_count]


def generate_flashcards(
    cfg: CompatConfig,
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
    data = chat_json(cfg, model_name, system, f"Study material:\n{truncated}")
    return data.get("flashcards", [])[:count]


def generate_study_notes(
    cfg: CompatConfig,
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
    return chat_json(cfg, model_name, system, f"Study material:\n{truncated}")


def generate_chat_reply(
    cfg: CompatConfig,
    material_text: str,
    history: list[dict],
    model_name: str,
    max_material_chars: int = 40000,
) -> str:
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
    conversation = "\n".join(f"{m['role']}: {m['content']}" for m in history)
    return chat_text(
        cfg,
        model_name,
        system,
        f"Conversation so far (newest last):\n{conversation}\n\n"
        f"Study material:\n{truncated}",
    )