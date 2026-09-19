import logging

from app.config import settings
from app.services import openai_compat

logger = logging.getLogger(__name__)

BASE_URL = "https://openrouter.ai/api/v1"
FREE_MODEL = "openrouter/free"


def _cfg() -> openai_compat.CompatConfig:
    return openai_compat.CompatConfig(
        provider="openrouter",
        base_url=BASE_URL,
        api_key=settings.openrouter_api_key,
        default_model=settings.openrouter_model or FREE_MODEL,
    )


def _ready_cfg() -> openai_compat.CompatConfig:
    cfg = _cfg()
    if not cfg.api_key:
        raise openai_compat.ProviderError(
            "OPENROUTER_API_KEY is not set",
            user_message=(
                "OpenRouter is not configured — add OPENROUTER_API_KEY to "
                "backend/.env and restart the backend."
            ),
        )
    return cfg


def _model(model_name: str) -> str:
    return model_name or _cfg().default_model


def generate_quiz(
    material_text: str,
    difficulty: str,
    question_count: int,
    model_name: str = "",
) -> list[dict]:
    return openai_compat.generate_quiz(
        _ready_cfg(), material_text, difficulty, question_count, _model(model_name)
    )


def generate_flashcards(
    material_text: str,
    count: int,
    model_name: str = "",
) -> list[dict]:
    return openai_compat.generate_flashcards(
        _ready_cfg(), material_text, count, _model(model_name)
    )


def generate_study_notes(
    material_text: str,
    model_name: str = "",
    language: str = "en",
) -> dict:
    return openai_compat.generate_study_notes(
        _ready_cfg(), material_text, _model(model_name), language=language
    )


def generate_chat_reply(
    material_text: str,
    history: list[dict],
    model_name: str = "",
    language: str = "en",
) -> str:
    return openai_compat.generate_chat_reply(
        _ready_cfg(), material_text, history, _model(model_name), language=language
    )


def generate_json(
    system: str, user: str, model_name: str = "", temperature: float = 0.3
) -> dict:
    """Generic strict-JSON completion (used by Exam Mode prompts)."""
    return openai_compat.chat_json(
        _ready_cfg(), _model(model_name), system, user, temperature=temperature
    )


def list_models() -> list[dict]:
    """Provider/models advertised to the UI (must have a matching provider key).

    ``openrouter/free`` lets OpenRouter route to whatever free model is
    available; extra free model IDs are configurable via OPENROUTER_FREE_MODELS
    (comma-separated) since specific free models come and go.
    """
    default_model = settings.openrouter_model or FREE_MODEL
    entries = [
        {
            "provider": "openrouter",
            "name": default_model,
            "label": "Free (auto)",
        }
    ]
    seen = {default_model}
    for raw in settings.openrouter_free_models.split(","):
        model_id = raw.strip()
        if model_id and model_id not in seen:
            seen.add(model_id)
            entries.append(
                {
                    "provider": "openrouter",
                    "name": model_id,
                    "label": f"{model_id} (free)",
                }
            )
    return entries