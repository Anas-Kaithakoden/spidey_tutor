"""Study Podcast: two-host conversational episodes generated from study material.

Design
------
- ``generate_podcast_script`` is a provider-agnostic dispatcher (same pattern as
  ``services/ai.py`` / ``services/exam.py``). Prompts live here; providers only
  need their generic strict-JSON ``generate_json`` helper.
- The script is validated against a strict Pydantic schema (``Script``/``Line``)
  BEFORE it is handed to TTS, and the word budget is enforced per duration so
  an episode can never balloon past its target length.
- ``weak_topics`` mode receives the student's real performance data (queried by
  the router from the same tables the analytics dashboard uses) and must only
  prioritise those topics when the material actually covers them.
- On any failure the dispatcher falls back to a deterministic, material-grounded
  script (``services/quick.py``) so the request never dies — mirroring the seed
  fallback used by quizzes/flashcards/notes.
"""

import logging
from typing import Any, Literal

from pydantic import BaseModel, Field, ValidationError, field_validator

from app.config import settings
from app.schemas import PODCAST_MODES
from app.services import gemini, groq, ollama, openrouter, quick
from app.services.openai_compat import ProviderError

logger = logging.getLogger(__name__)

MAX_DURATION_MINUTES = settings.podcast_max_duration_minutes
HOST_VOICE_ONE = settings.podcast_voice_host_one
HOST_VOICE_TWO = settings.podcast_voice_host_two

MAX_MATERIAL_CHARS = 40000

# Natural speech is roughly 130-165 words per minute. We ask the model for
# ~130 wpm and hard-cap the script at ~165 wpm so a requested episode length
# never runs away.
WPM = 150
MAX_WPB = 165  # words per minute hard ceiling for script validation

MODE_LABELS = {
    "learn": "Learn",
    "revise": "Revise",
    "exam_prep": "Exam Prep",
    "weak_topics": "Weak Topics",
}

MAX_WORDS_PER_LINE = 140


def supported_modes() -> list[str]:
    return list(PODCAST_MODES)


def max_words_for(duration_minutes: int) -> int:
    """Hard word budget for a requested duration (validates script length)."""
    duration_minutes = max(1, int(duration_minutes))
    return duration_minutes * MAX_WPB


def target_word_count(duration_minutes: int) -> int:
    """Word target the prompt asks the model to aim for."""
    duration_minutes = max(1, int(duration_minutes))
    return duration_minutes * 130


def min_words_for(duration_minutes: int) -> int:
    """Lower bound: a valid script must be long enough to justify the length."""
    return max(1, int(duration_minutes) * 60)


def min_lines_for(duration_minutes: int) -> int:
    """Minimum number of dialogue turns for a natural conversation."""
    return max(6, int(duration_minutes) * 3)


def _error_detail(provider: str, exc: Exception) -> str:
    """A safe, user-facing reason a provider/generation failed."""
    if isinstance(exc, ProviderError) and exc.user_message:
        return exc.user_message
    return f"{provider} podcast generation failed: {exc}"


class Line(BaseModel):
    speaker: Literal["host_one", "host_two"]
    text: str = Field(min_length=1)

    @field_validator("text")
    @classmethod
    def text_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Dialogue line cannot be blank.")
        return v


class Script(BaseModel):
    title: str = ""
    lines: list[Line]


def _word_count(lines: list[dict] | list[Line]) -> int:
    return sum(len(str(line.text).split()) for line in lines)


def _validate_script(
    raw: Any,
    duration_minutes: int,
    fallback_title: str = "",
) -> Script:
    """Strictly validate + normalize a raw provider script.

    Raises ``ValueError`` (callers fall back to the deterministic script) for
    anything unusable: wrong shape, blank lines, missing a host, runaway
    monologues, or an estimated length outside the request's word budget.
    """
    if not isinstance(raw, dict):
        raise ValueError("Podcast script response was not an object")

    try:
        script = Script.model_validate(raw)
    except ValidationError as exc:
        raise ValueError(f"Invalid podcast script: {exc.errors()[0]['msg']}") from exc

    lines = script.lines
    if not lines:
        raise ValueError("Podcast script has no dialogue lines")

    if not script.title.strip():
        if not fallback_title.strip():
            raise ValueError("Podcast script is missing a title")
        script.title = fallback_title.strip()

    speakers = {line.speaker for line in lines}
    if speakers != {"host_one", "host_two"}:
        raise ValueError("Podcast script must include both hosts")

    # Natural alternation: no more than two consecutive turns from one host.
    run = 1
    for prev, curr in zip(lines, lines[1:]):
        run = run + 1 if prev.speaker == curr.speaker else 1
        if run > 2:
            raise ValueError("Hosts must alternate — a single speaker held 3+ turns")

    if len(lines) < min_lines_for(duration_minutes):
        raise ValueError("Podcast script is too short for the requested duration")

    total_words = _word_count(lines)
    if total_words < min_words_for(duration_minutes):
        raise ValueError("Podcast script is too short for the requested duration")
    if total_words > max_words_for(duration_minutes):
        raise ValueError(
            f"Podcast script is too long for {duration_minutes} minutes "
            f"(~{total_words} words, budget {max_words_for(duration_minutes)})"
        )

    for line in lines:
        if len(str(line.text).split()) > MAX_WORDS_PER_LINE:
            raise ValueError("A single host held a turn longer than the per-line cap")

    return script


def _build_script_prompt(
    material_text: str,
    mode: str,
    duration_minutes: int,
    focus_topic: str,
    weak_topics: list[dict] | None,
) -> tuple[str, str]:
    mode_rules = {
        "learn": (
            "- Learn mode: give DEEPER conversational explanations. Build the "
            "episode around understanding: intuitive examples, analogies, and "
            "explicit connections BETWEEN concepts in the material.\n"
        ),
        "revise": (
            "- Revise mode: a FAST review. Prioritise concise summaries, key "
            "definitions, relationships between ideas, and the most important "
            "facts. Little fluff, high density.\n"
        ),
        "exam_prep": (
            "- Exam Prep mode: prioritise the highest-value concepts and points "
            "most likely to appear on an exam. Include 1-3 short self-check "
            "moments (a question one host asks, the other answers) — do NOT turn "
            "the whole episode into a quiz.\n"
        ),
        "weak_topics": (
            "- Weak Topics mode: focus the episode on the topics where the "
            "student performed poorly (performance snapshot below). Explain "
            "those concepts clearly and patiently. Only cover a weak topic if "
            "it is actually present in the study material.\n"
        ),
    }.get(mode, "")

    spoken_prompt = (
        "You are writing a conversation between TWO distinct podcast hosts:\n"
        "- host_one: the lead host — warm, curious, explains clearly.\n"
        "- host_two: the co-host — asks questions, asks for clarifications, "
        "adds examples, and summarises out loud.\n"
        "Make it feel like a REAL learning session, NOT two people reading "
        "notes aloud. Naturally alternate between explanations, questions, "
        "examples, clarifications, and short recaps. Both hosts must speak, "
        "no host should hold the floor for more than about a sentence or two "
        "at a time.\n"
        "\n"
        "STRICT RULES:\n"
        "- Only refer to facts and terms that appear in the study material. "
        "NEVER invent source-specific facts, statistics, definitions, or "
        "examples that are not in the text. If the material lacks detail, "
        "have the hosts say so and move on.\n"
        "- Speak naturally: contractions, short spoken sentences, no markdown, "
        "no bullet points, no stage directions, no 'Episode: ...' labels. "
        "Each line is pure spoken dialogue.\n"
        f"- Keep the script about {duration_minutes} minute(s) of audio: "
        f"roughly {target_word_count(duration_minutes)} words in total, and "
        f"NEVER more than {max_words_for(duration_minutes)} words. Each line "
        f"below {MAX_WORDS_PER_LINE} words.\n"
        "- Alternate speakers live: never more than two consecutive lines by "
        "the same host.\n"
    )

    if mode_rules:
        spoken_prompt += mode_rules

    if focus_topic:
        spoken_prompt += (
            f"- The student asked to focus on this topic/unit (cover it when "
            f"the material supports it): \"{focus_topic}\".\n"
        )

    _weak = weak_topics or []
    if mode == "weak_topics" and _weak:
        lines = "\n".join(
            f"  - {t.get('title', 'Unknown')} (average score {t.get('average_score', 0)}%, "
            f"{t.get('questions_answered', 0)} question(s) answered)"
            for t in _weak
        )
        spoken_prompt += (
            f"Student performance snapshot (weak topics, weakest first):\n"
            f"{lines}\n"
            "Use ONLY these topics where the material covers them. Do NOT "
            "fabricate details about the student's performance.\n"
        )

    schema = (
        '{"title": string, "lines": ['
        '{"speaker": "host_one" | "host_two", "text": string}'
        "]}"
    )
    system = (
        "You are a podcast scriptwriter for a study app.\n"
        + spoken_prompt
        + "\nRespond with STRICT JSON only, matching exactly: " + schema
    )

    user = (
        f"MODE: {MODE_LABELS.get(mode, mode)}\n"
        f"DURATION: about {duration_minutes} minute(s)\n\n"
        f"Study material:\n{material_text[:MAX_MATERIAL_CHARS]}"
    )
    return system, user


def _provider_generate_json(
    provider: str, system: str, user: str, model_name: str
) -> dict:
    """Pipe a strict-JSON prompt through the selected provider."""
    if provider == "gemini":
        name = model_name or settings.gemini_model
        return gemini.generate_json(system, user, name)
    if provider == "groq":
        return groq.generate_json(system, user, model_name)
    if provider == "openrouter":
        return openrouter.generate_json(system, user, model_name)
    if provider == "ollama":
        name = model_name or "qwen3:8b"
        return ollama.generate_json(system, user, name)
    raise ValueError(f"Unknown provider: {provider}")


def generate_podcast_script(
    material_text: str,
    mode: str = "learn",
    duration_minutes: int = 5,
    provider: str = "gemini",
    model_name: str = "",
    focus_topic: str = "",
    weak_topics: list[dict] | None = None,
) -> tuple[str, dict, str]:
    """Generate a validated two-host podcast script.

    Returns ``(generated_by, script_dict, error_detail)`` where ``script_dict``
    is a strict ``{"title": str, "lines": [{"speaker", "text"}]}`` structure
    ready for TTS. ``error_detail`` is non-empty only on the mock fallback.
    """
    error_detail = ""
    try:
        success_tag = "ai"
        if provider == "quick":
            raw = quick.generate_podcast_script(
                material_text,
                mode=mode,
                duration_minutes=duration_minutes,
                focus_topic=focus_topic,
                weak_topics=weak_topics,
            )
            success_tag = "quick"
        else:
            system, user = _build_script_prompt(
                material_text, mode, duration_minutes, focus_topic, weak_topics
            )
            raw = _provider_generate_json(provider, system, user, model_name)

        script = _validate_script(raw, duration_minutes)
        return success_tag, script.model_dump(), error_detail

    except Exception as exc:
        error_detail = _error_detail(provider, exc)
        logger.exception(
            "Podcast script generation failed (provider=%s, mode=%s): %s",
            provider, mode, exc,
        )
        return "mock", _mock_script(
            material_text, mode, duration_minutes, focus_topic, weak_topics
        ), error_detail


def _mock_script(
    material_text: str,
    mode: str,
    duration_minutes: int,
    focus_topic: str,
    weak_topics: list[dict] | None,
) -> dict:
    """Deterministic, material-grounded fallback script."""
    raw = quick.generate_podcast_script(
        material_text,
        mode=mode,
        duration_minutes=duration_minutes,
        focus_topic=focus_topic,
        weak_topics=weak_topics,
    )
    script = Script.model_validate(raw)
    title = script.title.strip() or f"{MODE_LABELS.get(mode, mode)} Episode"
    script.title = title
    return script.model_dump()