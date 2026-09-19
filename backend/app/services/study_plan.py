import json
import logging
import re
from datetime import date, timedelta

from app.config import settings
from app.services import gemini, ollama

logger = logging.getLogger(__name__)


def _robust_json_loads(text: str) -> dict:
    t = text.strip()
    if t.startswith("```"):
        t = "\n".join([l for l in t.split("\n") if not l.strip().startswith("```")]).strip()
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        pass
    t2 = re.sub(r",\s*}", "}", t)
    t2 = re.sub(r",\s*]", "]", t2)
    try:
        return json.loads(t2)
    except json.JSONDecodeError:
        pass
    s = t.find("{")
    e = t.rfind("}")
    if s != -1 and e > s:
        snippet = t[s:e+1]
        snippet = re.sub(r",\s*}", "}", snippet)
        snippet = re.sub(r",\s*]", "]", snippet)
        try:
            return json.loads(snippet)
        except json.JSONDecodeError:
            pass
    raise ValueError(f"Could not parse JSON: {text[:500]}")


MOCK_PLAN = {
    "plan": [
        {"day": 1, "topic": "Overview & Foundations", "tasks": ["Read syllabus overview", "List all topics", "Prioritize weak areas"], "focus": "Planning", "duration_hours": 3, "revision": False},
        {"day": 2, "topic": "Core Concepts - Part 1", "tasks": ["Study core definitions", "Make flashcards", "Do 5 practice Qs"], "focus": "Understanding", "duration_hours": 3, "revision": False},
    ],
    "tips": ["Study 25 min, break 5 min (Pomodoro)", "Revise previous day for 15 min", "Sleep 7+ hours before exam"]
}


def generate_study_plan(
    syllabus: str,
    exam_date: str,
    daily_hours: int = 3,
    provider: str = "gemini",
    model_name: str = "",
    language: str = "en",
) -> tuple[str, dict]:
    """Generate detailed day-by-day plan. Returns (generated_by, plan_dict)."""
    if not syllabus or not syllabus.strip():
        raise ValueError("Syllabus cannot be empty")
    try:
        exam_d = date.fromisoformat(exam_date)
    except Exception:
        raise ValueError("Invalid exam_date")
    days_left = (exam_d - date.today()).days
    if days_left <= 0:
        raise ValueError("exam_date must be in future")
    if days_left > 60:
        days_left = 60  # cap for prompt

    truncated = syllabus[:35000]
    is_ml = language.lower().startswith("ml")

    # Build language-specific prompt
    if is_ml:
        prompt = (
            "You are a study planner. Given syllabus and exam date, create a detailed day-by-day study plan in Malayalam (മലയാളം).\n"
            f"Exam in {days_left} days ({exam_date}), {daily_hours} hours/day. Syllabus:\n{truncated}\n\n"
            "Rules: 130-150 words total for tips, but plan days must cover all topics. "
            "Respond STRICT JSON only:\n"
            '{"plan": [{"day": int, "topic": string, "tasks": [string], "focus": string, "duration_hours": float, "revision": bool}], "tips": [string]}\n'
            f"Create exactly {min(days_left, 14)} days if many topics, else {days_left} days. Each day 2-4 tasks. In Malayalam."
        )
    else:
        prompt = (
            "You are an expert study planner. Given syllabus and exam date, create a detailed, realistic day-by-day study plan.\n"
            f"Exam in {days_left} days on {exam_date}, {daily_hours} hours/day. Syllabus:\n{truncated}\n\n"
            "Rules:\n"
            "- Cover all syllabus topics, split large topics across days\n"
            "- Allocate 2-4 concrete tasks per day (e.g., read, flashcards, practice Qs, mock test)\n"
            "- Alternate focus: Understanding / Practice / Revision / Mock\n"
            "- Mark revision days where you revise previous topics\n"
            "- Keep tone warm, encouraging, student-friendly\n"
            "Respond with STRICT JSON only, no markdown:\n"
            '{"plan": [{"day": int, "topic": string, "tasks": [string], "focus": string, "duration_hours": float, "revision": bool}], "tips": [string]}\n'
            f"Create {min(days_left, 20)} days max (if more days left, compress). Each day duration ~{daily_hours}h. In English."
        )

    try:
        if provider == "ollama":
            name = model_name or "qwen3:8b"
            from app.services.ollama import _chat_json

            system = "You are a study planner. Respond STRICT JSON only."
            raw = _chat_json(name, system, prompt, temperature=0.6)
            data = _robust_json_loads(raw) if isinstance(raw, str) else raw
        elif provider == "gemini":
            from google.genai import types

            name = model_name or settings.gemini_model
            # handle deprecated
            if name in ("gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-flash-lite", ""):
                name = settings.gemini_model
            client = gemini._client()
            resp = client.models.generate_content(
                model=name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.6,
                ),
            )
            data = _robust_json_loads(resp.text)
        elif provider == "quick":
            # deterministic quick: split syllabus lines into topics
            topics = [t.strip() for t in truncated.split("\n") if t.strip()][:20]
            if not topics:
                topics = truncated.split(".")[:10]
            plan = []
            start = date.today() + timedelta(days=1)
            for i, topic in enumerate(topics[:min(days_left, 10)]):
                d = start + timedelta(days=i)
                plan.append({
                    "day": i+1,
                    "topic": topic[:80],
                    "tasks": [f"Study {topic[:40]}", "Make flashcards", "Practice 5 Qs"],
                    "focus": "Understanding" if i % 3 == 0 else "Practice",
                    "duration_hours": float(daily_hours),
                    "revision": i % 4 == 3,
                    "date": d.isoformat(),
                })
            return "quick", {
                "plan": plan,
                "tips": ["Revise daily 15 min", "Pomodoro 25/5", "Sleep well"],
            }
        else:
            raise ValueError(f"Unknown provider {provider}")

        # Normalize plan: add date field if missing
        raw_plan = data.get("plan", [])
        tips = data.get("tips", [])[:5]
        plan = []
        start = date.today() + timedelta(days=1)
        for idx, p in enumerate(raw_plan):
            d = start + timedelta(days=idx)
            plan.append({
                "day": p.get("day", idx+1),
                "date": p.get("date", d.isoformat()),
                "topic": str(p.get("topic", f"Topic {idx+1}")).strip()[:120],
                "tasks": [str(t).strip() for t in p.get("tasks", []) if str(t).strip()][:4],
                "focus": str(p.get("focus", "Study")).strip(),
                "duration_hours": float(p.get("duration_hours", daily_hours)),
                "revision": bool(p.get("revision", False)),
            })
        if not plan:
            raise ValueError("Empty plan")

        return "ai", {"plan": plan, "tips": tips}

    except Exception as exc:
        logger.exception("Study plan generation failed (provider=%s): %s", provider, exc)
        # mock fallback: generate simple split
        start = date.today() + timedelta(days=1)
        topics = [t.strip() for t in truncated.split("\n") if t.strip()][:10]
        if not topics:
            topics = ["General Review"]
        plan = []
        for i, topic in enumerate(topics[: min(days_left, 7)]):
            d = start + timedelta(days=i)
            plan.append({
                "day": i+1,
                "date": d.isoformat(),
                "topic": topic[:80],
                "tasks": [f"Review {topic[:30]}", "Practice Qs"],
                "focus": "Revision" if i == len(topics)-1 else "Understanding",
                "duration_hours": float(daily_hours),
                "revision": i > 0 and i % 3 == 0,
            })
        return "mock", {"plan": plan, "tips": MOCK_PLAN["tips"]}
