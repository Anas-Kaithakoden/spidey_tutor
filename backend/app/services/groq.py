import logging

from app.config import settings
from app.services import openai_compat

logger = logging.getLogger(__name__)

BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "openai/gpt-oss-20b"
STRONG_MODEL = "openai/gpt-oss-120b"


def _cfg() -> openai_compat.CompatConfig:
    return openai_compat.CompatConfig(
        provider="groq",
        base_url=BASE_URL,
        api_key=settings.groq_api_key,
        default_model=settings.groq_model or DEFAULT_MODEL,
    )


def _ready_cfg() -> openai_compat.CompatConfig:
    cfg = _cfg()
    if not cfg.api_key:
        raise openai_compat.ProviderError(
            "GROQ_API_KEY is not set",
            user_message=(
                "Groq is not configured — add GROQ_API_KEY to backend/.env and "
                "restart the backend."
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
) -> dict:
    return openai_compat.generate_study_notes(
        _ready_cfg(), material_text, _model(model_name)
    )


def generate_chat_reply(
    material_text: str,
    history: list[dict],
    model_name: str = "",
) -> str:
    return openai_compat.generate_chat_reply(
        _ready_cfg(), material_text, history, _model(model_name)
    )


def list_models() -> list[dict]:
    """Provider/models advertised to the UI (must have a matching provider key)."""
    return [
        {
            "provider": "groq",
            "name": settings.groq_model or DEFAULT_MODEL,
            "label": "GPT-OSS 20B (fast)",
        },
        {
            "provider": "groq",
            "name": settings.groq_model_strong or STRONG_MODEL,
            "label": "GPT-OSS 120B (quality)",
        },
    ]