"""Exam Mode: mixed-type exam generation and answer evaluation.

Design
------
- ``generate_exam`` is a dispatcher (like ``services/ai.py``) that routes to
  the selected provider. Prompts live here so the exam schema is defined once;
  providers only need a generic strict-JSON completion
  (``generate_json`` on each provider module).
- ``plan_exam_distribution`` guarantees a balanced, multi-type mix (never a
  single question type) for any requested count.
- ``evaluate_exam`` grades answers:
  * objective questions (MCQ, fill-in-the-blank) are scored deterministically,
  * subjective questions (short/paragraph/essay) are graded by an LLM using
    configurable criteria (strictness, partial credit, penalizing unsupported
    information) with a deterministic keyword-overlap fallback.
The evaluation criteria are backend-configurable (see ``app/config.py``) and
are surfaced on every ``ExamResultOut``.
"""

import logging
import re
from difflib import SequenceMatcher
from typing import Any

from pydantic import BaseModel, ValidationError

from app.config import settings
from app.seed import MOCK_EXAM_QUESTIONS
from app.services import gemini, groq, ollama, openrouter, quick
from app.services.openai_compat import ProviderError

logger = logging.getLogger(__name__)

QUESTION_TYPES = ["mcq", "short_answer", "fill_blank", "paragraph", "essay"]

MAX_SCORE = {
    "mcq": 1,
    "short_answer": 2,
    "fill_blank": 1,
    "paragraph": 4,
    "essay": 6,
}

TYPE_LABELS = {
    "mcq": "Multiple choice",
    "short_answer": "Short answer",
    "fill_blank": "Fill in the blank",
    "paragraph": "Paragraph",
    "essay": "Essay",
}

# Weights used to build a sensible default mix for any question count.
DISTRIBUTION_WEIGHTS = {
    "mcq": 0.40,
    "short_answer": 0.20,
    "fill_blank": 0.15,
    "paragraph": 0.15,
    "essay": 0.10,
}

MAX_MATERIAL_CHARS = 40000

_STATUS_CHOICES = {"correct", "partial", "incorrect", "unanswered"}


def _error_detail(provider: str, exc: Exception) -> str:
    """A safe, user-facing reason a provider/generation/evaluation failed."""
    if isinstance(exc, ProviderError) and exc.user_message:
        return exc.user_message
    return f"{provider} generation failed: {exc}"


def evaluation_criteria() -> dict:
    """Snapshot of the configurable backend evaluation criteria."""
    return {
        "ai_subjective": bool(settings.exam_eval_ai_subjective),
        "strictness": settings.exam_eval_strictness,
        "partial_credit": bool(settings.exam_eval_partial_credit),
        "penalize_unsupported": bool(settings.exam_eval_penalize_unsupported),
    }


def _min_variety(count: int) -> int:
    if count <= 1:
        return 1
    if count == 2:
        return 2
    if count < 5:
        return 3
    return 4


def plan_exam_distribution(question_count: int) -> list[str]:
    """Return an ordered list of question types summing to ``question_count``.

    Uses largest-remainder apportionment over a fixed weight table and then
    enforces a minimum variety so the exam never contains only one type.
    """
    if question_count < 1:
        return []

    counts: dict[str, int] = {}
    raw = {t: DISTRIBUTION_WEIGHTS[t] * question_count for t in QUESTION_TYPES}
    counts = {t: int(v) for t, v in raw.items()}
    remainder = question_count - sum(counts.values())
    # largest remainders get the leftover slots
    for t, v in sorted(
        raw.items(), key=lambda kv: kv[1] - int(kv[1]), reverse=True
    ):
        if remainder == 0:
            break
        counts[t] += 1
        remainder -= 1

    # Enforce minimum type variety by converting surplus MCQ slots.
    present = {t for t, c in counts.items() if c > 0}
    for t in QUESTION_TYPES:
        if len(present) >= _min_variety(question_count):
            break
        if t in present:
            continue
        donor = next((d for d in QUESTION_TYPES if counts[d] > 1), None)
        if donor is None:
            break
        counts[donor] -= 1
        counts[t] += 1
        present.add(t)

    # Interleave types for a balanced order (no large blocks of one type).
    remaining = dict(counts)
    result: list[str] = []
    while True:
        added = False
        for t in QUESTION_TYPES:
            if remaining[t] > 0:
                result.append(t)
                remaining[t] -= 1
                added = True
        if not added:
            break
    return result


def _norm(text: Any) -> str:
    return re.sub(r"[^a-z0-9 ]", "", str(text or "").lower()).strip()


def _similarity(a: Any, b: Any) -> float:
    na, nb = _norm(a), _norm(b)
    if not na or not nb:
        return 0.0
    return SequenceMatcher(None, na, nb).ratio()


def _round_half(value: float) -> float:
    return round(value * 2) / 2


def _safe_score(score: Any, max_score: int) -> float:
    try:
        val = min(float(score), float(max_score))
        return max(0.0, round(val, 2))
    except (TypeError, ValueError):
        return 0.0


def _coerce_status(status: Any, score: float, max_score: int) -> str:
    status = str(status or "").strip().lower()
    if status in _STATUS_CHOICES:
        return status
    if max_score and score >= max_score:
        return "correct"
    if score > 0:
        return "partial"
    return "incorrect"


def normalize_question(item: dict, idx: int = 0) -> dict:
    """Validate + normalize a raw provider question into a canonical dict.

    Raises ``ValueError`` for anything unusable so the caller can fall back.
    """
    qtype = str(item.get("question_type", "")).strip().lower().replace(" ", "_")
    aliases = {
        "multiple_choice": "mcq",
        "mc": "mcq",
        "short": "short_answer",
        "shortanswer": "short_answer",
        "fill": "fill_blank",
        "fillblank": "fill_blank",
        "fill_in_the_blank": "fill_blank",
        "para": "paragraph",
        "long_answer": "paragraph",
    }
    qtype = aliases.get(qtype, qtype)
    if qtype not in QUESTION_TYPES:
        raise ValueError(f"Unknown exam question type: {item.get('question_type')!r}")

    question = str(item.get("question", "")).strip()
    if not question:
        raise ValueError("Exam question text is empty")

    explanation = str(item.get("explanation", "")).strip()
    key_points = [
        str(kp).strip() for kp in item.get("key_points", []) if str(kp).strip()
    ][:8]

    out = {
        "question_type": qtype,
        "question": question,
        "options": None,
        "correct_answer": None,
        "accepted_answer": "",
        "key_points": key_points,
        "explanation": explanation,
        "max_score": MAX_SCORE.get(qtype, 1),
    }

    if qtype == "mcq":
        options = item.get("options", [])
        if not isinstance(options, list) or len(options) < 2:
            raise ValueError("MCQ must have at least 2 options")
        correct = item.get("correct_answer", item.get("correctAnswer", -1))
        if not isinstance(correct, int) or not (0 <= correct < len(options)):
            raise ValueError("Invalid MCG correct answer")
        clean_options = [str(o) for o in options]
        out["options"] = clean_options
        out["correct_answer"] = correct
        out["accepted_answer"] = clean_options[correct]
    else:
        accepted = str(item.get("accepted_answer", item.get("answer", ""))).strip()
        if not accepted:
            raise ValueError(f"{qtype} question is missing accepted_answer")
        out["accepted_answer"] = accepted
        if qtype in ("paragraph", "essay") and not key_points:
            # Fall back to the first ~50 chars of the answer as a key phrase.
            out["key_points"] = [accepted[:60]] if accepted else []

    return out


def _build_generation_prompt(
    material_text: str,
    difficulty: str,
    question_count: int,
    distribution: list[str],
) -> tuple[str, str]:
    counts: dict[str, int] = {}
    for t in distribution:
        counts[t] = counts.get(t, 0) + 1
    mix_lines = "\n".join(
        f"- {TYPE_LABELS[t]} ({t}): {counts[t]}"
        for t in QUESTION_TYPES
        if counts.get(t, 0) > 0
    )
    schema = (
        '{"questions": ['
        '{"question_type": "mcq|short_answer|fill_blank|paragraph|essay", '
        '"question": string, '
        '"options": [string x4] (mcq only), '
        '"correct_answer": int index (mcq only), '
        '"accepted_answer": string (reference answer, all types), '
        '"key_points": [string] (paragraph/essay: concepts to cover), '
        '"explanation": string}]}'
    )
    system = (
        "You are an exam generator for a study tool.\n"
        f"Create an exam of exactly {question_count} questions at "
        f"\"{difficulty}\" difficulty.\n"
        "Use ONLY the provided study material: every question and reference "
        "answer must be strictly grounded in the text.\n"
        "Use a balanced mix of question types with exactly these counts:\n"
        f"{mix_lines}\n"
        "Rules:\n"
        "- mcq: exactly 4 options with exactly one correct_answer index.\n"
        "- fill_blank: include the blank marker \"______\" inside the question.\n"
        "- short_answer: accepted_answer is a concise 1-2 sentence answer.\n"
        "- paragraph: accepted_answer is a short paragraph; give 2-4 key_points\n"
        "  the answer should cover.\n"
        "- essay: accepted_answer is a short structured essay; give 3-6 key_points.\n"
        "- accepted_answer is required for every question.\n"
        "- Do not ask questions the material cannot answer.\n"
        'Respond with STRICT JSON only matching: ' + schema
    )
    return system, f"Study material:\n{material_text[:MAX_MATERIAL_CHARS]}"


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


def generate_exam(
    material_text: str,
    difficulty: str,
    question_count: int,
    provider: str = "gemini",
    model_name: str = "",
) -> tuple[str, list[dict], str]:
    """Generate a mixed-type exam. Returns (generated_by, questions, error).

    ``error`` is a user-safe reason string, non-empty only when the generation
    fell back to mock data.
    """
    error_detail = ""
    try:
        distribution = plan_exam_distribution(question_count)
        success_tag = "ai"
        if provider == "quick":
            raw = quick.generate_exam(
                material_text, difficulty, question_count, distribution
            )
            success_tag = "quick"
        else:
            system, user = _build_generation_prompt(
                material_text, difficulty, question_count, distribution
            )
            data = _provider_generate_json(provider, system, user, model_name)
            raw = data.get("questions", [])

        questions = [
            normalize_question(q, idx)
            for idx, q in enumerate(raw[:question_count])
        ]
        if not questions:
            raise ValueError("No exam questions generated")
        if provider != "quick" and len(questions) != question_count:
            raise ValueError(
                f"Expected {question_count} questions, got {len(questions)}"
            )
        actual = len(questions)
        if actual > 1 and len({q["question_type"] for q in questions}) < 2:
            raise ValueError("Exam must include more than one question type")
        return success_tag, questions, error_detail

    except Exception as exc:
        error_detail = _error_detail(provider, exc)
        logger.exception(
            "Exam generation failed (provider=%s, model=%s): %s",
            provider, model_name, exc,
        )
        questions = [
            normalize_question(dict(q), idx)
            for idx, q in enumerate(MOCK_EXAM_QUESTIONS[:question_count])
        ]
        return "mock", questions, error_detail


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------


class _LLMReview(BaseModel):
    question_id: int
    score: float = 0.0
    status: str = "incorrect"
    feedback: str = ""
    improved_answer: str | None = None


class _LLMExamEvaluation(BaseModel):
    summary: str = ""
    strengths: list[str] = []
    weak_areas: list[str] = []
    topics_to_improve: list[str] = []
    recommendations: list[str] = []
    reviews: list[_LLMReview] = []


def _validate_eval(raw: Any, expected_ids: set[int]) -> _LLMExamEvaluation:
    if not isinstance(raw, dict):
        raise ValueError("Evaluation response was not an object")
    ev = _LLMExamEvaluation.model_validate(raw)
    present = {r.question_id for r in ev.reviews}
    missing = expected_ids - present
    if missing:
        raise ValueError(
            f"Evaluation is missing reviews for {len(missing)} question(s)"
        )
    return ev


def _build_eval_prompt(
    material_text: str,
    questions: list[dict],
    answers_by_id: dict[int, dict],
    criteria: dict,
) -> tuple[str, str]:
    strictness = criteria.get("strictness", "balanced")
    if strictness == "lenient":
        strictness_line = (
            "When a partially-correct idea is expressed, give the student the "
            "benefit of the doubt."
        )
    elif strictness == "strict":
        strictness_line = (
            "Demand clear, explicit support from the answer for each claim; "
            "be conservative when awarding partial credit."
        )
    else:
        strictness_line = (
            "Award credit only for what the answer actually supports."
        )

    rules = [
        "Grade each answer against the reference answer AND the study material.",
        strictness_line,
    ]
    if criteria.get("partial_credit"):
        rules.append(
            "Distinguish well-supported answers from partially correct ones: "
            "award partial credit for answers that contain some correct ideas "
            "from the material."
        )
    if criteria.get("penalize_unsupported"):
        rules.append(
            "Do NOT reward statements that are not supported by the study "
            "material; unsupported claims earn no credit and can lower the "
            "score for the unsupported part."
        )
    rules.append(
        "Allow reasonable variation in wording for equivalent answers."
    )
    rules.append(
        "For paragraph and essay answers evaluate factual accuracy, relevance "
        "to the question, coverage of the important concepts (key_points) from "
        "the source material, and clarity. Do not judge purely on writing "
        "style unless the question explicitly requires it."
    )
    rules.append("status must be one of: correct, partial, incorrect, unanswered.")
    rules.append("score must be a number between 0 and the question's max_score.")
    rules.append(
        "feedback: 1-3 sentences explaining what was done well and what was "
        "missing. improved_answer: a concise model answer (or null)."
    )

    schema = (
        '{"summary": string, '
        '"strengths": [string], "weak_areas": [string], '
        '"topics_to_improve": [string], "recommendations": [string], '
        '"reviews": [{"question_id": int, "score": number, '
        '"status": string, "feedback": string, '
        '"improved_answer": string|null}]}'
    )
    system = (
        "You are a rigorous but fair exam grader for a study tool.\n"
        "Rules:\n" + "\n".join(f"- {r}" for r in rules) +
        '\n\nRespond with STRICT JSON only matching: ' + schema
    )

    lines = ["Questions and student answers:"]
    for q in questions:
        ans = answers_by_id.get(q["id"], {})
        student = (ans.get("text") or "").strip() or "(No answer)"
        lines.append(
            f"Q{q['id']} [{q['question_type']}, max {q['max_score']}]: "
            f"{q['question']}"
        )
        lines.append(f"  Reference answer: {q['accepted_answer']}")
        if q.get("key_points"):
            lines.append(f"  Key points to cover: {'; '.join(q['key_points'])}")
        lines.append(f"  Student answer: {student}")

    user = (
        f"Study material:\n{material_text[:MAX_MATERIAL_CHARS]}\n\n"
        + "\n".join(lines)
    )
    return system, user


def _display_answer(question: dict, ans: dict | None = None) -> str | None:
    ans = ans or {}
    if question["question_type"] == "mcq":
        option = ans.get("option")
        if isinstance(option, int):
            options = question.get("options") or []
            if 0 <= option < len(options):
                return f"{chr(65 + option)}. {options[option]}"
            return "(Invalid selection)"
        return None
    text = ans.get("text")
    text = str(text).strip() if text else ""
    return text or None


def _expected_display(question: dict) -> str:
    if question["question_type"] == "mcq":
        options = question.get("options") or []
        idx = question.get("correct_answer")
        if options and isinstance(idx, int) and 0 <= idx < len(options):
            return f"{chr(65 + idx)}. {options[idx]}"
        return question.get("accepted_answer", "")
    return question.get("accepted_answer", "")


def _make_review(
    question: dict,
    ans: dict | None,
    *,
    status: str,
    score: float,
    feedback: str,
    improved_answer: str | None = None,
) -> dict:
    return {
        "question_id": question.get("id", 0),
        "question": question["question"],
        "question_type": question["question_type"],
        "user_answer": _display_answer(question, ans),
        "expected_answer": _expected_display(question),
        "status": status,
        "score": score,
        "max_score": question["max_score"],
        "feedback": feedback,
        "improved_answer": improved_answer,
    }


def grade_deterministic(question: dict, ans: dict | None = None) -> dict:
    """Objective scoring used for MCQ/fill-blank and for the fallback path."""
    max_score = question["max_score"]
    qtype = question["question_type"]
    ans = ans or {}

    if qtype == "mcq":
        expected_text = _expected_display(question)
        option = ans.get("option")
        if not isinstance(option, int):
            return _make_review(
                question, ans, status="unanswered", score=0.0,
                feedback="No answer provided.",
            )
        if option == question["correct_answer"]:
            return _make_review(
                question, ans, status="correct", score=float(max_score),
                feedback="Correct.",
            )
        return _make_review(
            question, ans, status="incorrect", score=0.0,
            feedback="Incorrect. Compare your selection with the expected answer.",
            improved_answer=expected_text,
        )

    text = str(ans.get("text") or "").strip()
    if not text:
        return _make_review(
            question, ans, status="unanswered", score=0.0,
            feedback="No answer provided.",
        )

    norm_text = _norm(text)
    norm_accepted = _norm(question["accepted_answer"])
    sim = (
        1.0
        if norm_accepted and norm_accepted in norm_text
        else _similarity(text, question["accepted_answer"])
    )
    key_points = question.get("key_points") or []
    coverage = 0.0
    if key_points:
        covered = [
            1.0 for kp in key_points if kp.lower().strip() in norm_text
        ]
        coverage = (len(covered) / len(key_points)) if key_points else 0.0
    else:
        coverage = sim
    combined = 0.7 * sim + 0.3 * coverage

    if combined >= 0.8:
        return _make_review(
            question, ans, status="correct", score=float(max_score),
            feedback="Good — the answer is well supported by the material.",
        )
    if combined >= 0.4:
        return _make_review(
            question, ans, status="partial", score=float(_round_half(max_score * 0.5)),
            feedback=(
                "Partially correct — some key ideas are present but the answer "
                "is incomplete or imprecise. See the reference answer."
            ),
            improved_answer=question["accepted_answer"],
        )
    return _make_review(
        question, ans, status="incorrect", score=0.0,
        feedback=(
            "This answer does not match the reference answer closely enough. "
            "See the reference answer."
        ),
        improved_answer=question["accepted_answer"],
    )


def _llm_score_review(question: dict, ans: dict | None, llm: _LLMReview) -> dict:
    max_score = question["max_score"]
    score = _safe_score(llm.score, max_score)
    status = _coerce_status(llm.status, score, max_score)
    return _make_review(
        question,
        ans,
        status=status,
        score=score,
        feedback=str(llm.feedback or "").strip(),
        improved_answer=(
            str(llm.improved_answer).strip() if llm.improved_answer else None
        ),
    )


def evaluate_exam(
    questions: list[dict],
    answers_by_id: dict[int, dict],
    material_text: str,
    provider: str = "gemini",
    model_name: str = "",
    criteria: dict | None = None,
) -> tuple[str, dict, str]:
    """Grade an exam attempt.

    Returns ``(grading_method, result_dict, error_detail)`` where
    ``grading_method`` is one of ``deterministic``, ``hybrid`` or ``fallback``.
    The result dict is validated into ``ExamResultOut`` by the router.
    """
    criteria = criteria or evaluation_criteria()
    ai_subjective = bool(criteria.get("ai_subjective", True))
    if ai_subjective:
        subjective_types = {"paragraph", "essay", "short_answer"}
    else:
        subjective_types = set()

    subjective = [
        q for q in questions if q["question_type"] in subjective_types
    ]

    result: dict[str, Any] = {
        "summary": "",
        "strengths": [],
        "weak_areas": [],
        "topics_to_improve": [],
        "recommendations": [],
        "reviews": [],
    }
    grading_method = "deterministic"
    error_detail = ""
    llm_reviews: dict[int, _LLMReview] = {}

    if subjective:
        grading_method = "hybrid"
        try:
            system, user = _build_eval_prompt(
                material_text, subjective, answers_by_id, criteria
            )
            raw = _provider_generate_json(provider, system, user, model_name)
            ev = _validate_eval(raw, {q["id"] for q in subjective})
            llm_reviews = {r.question_id: r for r in ev.reviews}
            result["summary"] = str(ev.summary or "").strip()
            result["strengths"] = [s for s in ev.strengths if str(s).strip()]
            result["weak_areas"] = [s for s in ev.weak_areas if str(s).strip()]
            result["topics_to_improve"] = [
                s for s in ev.topics_to_improve if str(s).strip()
            ]
            result["recommendations"] = [
                s for s in ev.recommendations if str(s).strip()
            ]
        except Exception as exc:
            error_detail = _error_detail(provider, exc)
            logger.exception(
                "Exam evaluation failed (provider=%s, model=%s): %s",
                provider, model_name, exc,
            )
            grading_method = "fallback"

    reviews: list[dict] = []
    for q in questions:
        ans = answers_by_id.get(q["id"]) or {}
        if q["id"] in llm_reviews and q["question_type"] in subjective_types:
            reviews.append(_llm_score_review(q, ans, llm_reviews[q["id"]]))
        else:
            reviews.append(grade_deterministic(q, ans))

    total_score = sum(float(r["score"]) for r in reviews)
    max_score = sum(int(q["max_score"]) for q in questions)
    percentage = round((total_score / max_score) * 100, 1) if max_score else 0.0

    result["reviews"] = reviews
    result["total_score"] = round(total_score, 2)
    result["max_score"] = max_score
    result["percentage"] = percentage
    result["grading_method"] = grading_method

    if not result["summary"]:
        result["summary"] = (
            f"You scored {round(total_score, 1)} out of {max_score} "
            f"({percentage}%)."
        )
    if grading_method in ("deterministic", "fallback") and not result["recommendations"]:
        result["strengths"] = result["strengths"] or [
            "The answers you gave followed the study material closely "
            "where they were scored."
        ]
        weak = [
            r["question_type"] for r in reviews
            if r["status"] in ("incorrect", "partial")
        ]
        if weak:
            result["weak_areas"] = result["weak_areas"] or [
                f"Review the material around: {', '.join(sorted(set(weak)))} questions."
            ]
        result["topics_to_improve"] = result["topics_to_improve"] or [
            "Re-read the study material sections related to the questions you "
            "missed or answered partially."
        ]
        result["recommendations"] = result["recommendations"] or [
            "Re-take this exam after reviewing the marked questions, or ask "
            "the AI Chat to explain any concept you found difficult."
        ]

    return grading_method, result, error_detail