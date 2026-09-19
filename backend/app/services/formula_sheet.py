import json
import logging
import re

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


MOCK_FORMULAS = [
    {"title": "Pythagorean Theorem", "formula": "a² + b² = c²", "description": "Relates sides of a right triangle", "category": "Geometry"},
    {"title": "Quadratic Formula", "formula": "x = (-b ± √(b²-4ac)) / 2a", "description": "Solves ax²+bx+c=0", "category": "Algebra"},
    {"title": "Ohm's Law", "formula": "V = I × R", "description": "Voltage equals current times resistance", "category": "Physics"},
]


def generate_formula_sheet(
    material_text: str,
    provider: str = "gemini",
    model_name: str = "",
    language: str = "en",
) -> tuple[str, list[dict]]:
    """Extract formulas and key equations. Returns (generated_by, formulas)."""
    if not material_text or not material_text.strip():
        raise ValueError("Material is empty")
    truncated = material_text[:35000]
    is_ml = language.lower().startswith("ml")

    if is_ml:
        prompt = (
            "You are a formula sheet generator. Extract all important formulas, equations, and key definitions from the material and present them in Malayalam where possible.\n"
            f"Material:\n{truncated}\n\n"
            "Rules:\n"
            "- Extract 8-15 most important formulas/equations/definitions\n"
            "- For each: title (short), formula (LaTeX or plain), description (1 sentence in Malayalam), category\n"
            "- If no explicit formulas, create key concept definitions as formula-like entries\n"
            "Respond STRICT JSON only:\n"
            '{"formulas": [{"title": string, "formula": string, "description": string, "category": string}]}\n'
        )
    else:
        prompt = (
            "You are a formula sheet generator for students. Extract all important formulas, equations, laws, and key definitions.\n"
            f"Material:\n{truncated}\n\n"
            "Rules:\n"
            "- Find 8-15 most important formulas/equations\n"
            "- For each: title, formula (use plain text or LaTeX-like, e.g., E=mc^2, F=ma), description (1 sentence), category (e.g., Algebra, Physics, OS)\n"
            "- If material has no explicit formulas, extract key definitions/theorems as formula-like entries\n"
            "- Keep formula concise, description clear\n"
            "Respond STRICT JSON only:\n"
            '{"formulas": [{"title": string, "formula": string, "description": string, "category": string}]}\n'
        )

    try:
        if provider == "ollama":
            name = model_name or "qwen3:8b"
            from app.services.ollama import _chat_json

            system = "You are a formula extractor. Respond STRICT JSON only."
            raw = _chat_json(name, system, prompt, temperature=0.5)
            data = _robust_json_loads(raw) if isinstance(raw, str) else raw
        elif provider == "gemini":
            from google.genai import types

            name = model_name or settings.gemini_model
            if name in ("gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-flash-lite", ""):
                name = settings.gemini_model
            client = gemini._client()
            resp = client.models.generate_content(
                model=name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.5,
                ),
            )
            data = _robust_json_loads(resp.text)
        elif provider == "quick":
            # quick: split material into sentences and fake formulas
            sentences = [s.strip() for s in truncated.split(".") if len(s.strip()) > 20][:10]
            formulas = []
            for i, s in enumerate(sentences):
                formulas.append({
                    "title": f"Concept {i+1}",
                    "formula": s[:40],
                    "description": s[:80],
                    "category": "General",
                })
            return "quick", formulas
        else:
            raise ValueError(f"Unknown provider {provider}")

        formulas = []
        for f in data.get("formulas", []):
            title = str(f.get("title", "")).strip()
            formula = str(f.get("formula", "")).strip()
            desc = str(f.get("description", "")).strip()
            cat = str(f.get("category", "General")).strip() or "General"
            if not title or not formula:
                continue
            formulas.append({"title": title, "formula": formula, "description": desc, "category": cat})
        if not formulas:
            raise ValueError("No formulas extracted")
        return "ai", formulas[:15]

    except Exception as exc:
        logger.exception("Formula sheet generation failed (provider=%s): %s", provider, exc)
        return "mock", [dict(f) for f in MOCK_FORMULAS]
