# AGENTS.md

Hackathon study app: upload material (PDF/text) → AI generates quizzes & flashcards. Root = Next.js frontend (`:3000`), `backend/` = FastAPI API (`:8000`). README.md holds the full architecture + collaboration rules; this file lists gotchas an agent would otherwise get wrong.

## Running it
- Frontend (repo root): `npm run dev`
- Backend — must run **from inside `backend/`** so the `app` package and `.env` resolve:
  `..\.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000`
- Frontend proxies `/api/*` → `http://127.0.0.1:8000` via `next.config.ts` rewrites (`BACKEND_URL` overrides the target).

## Verification (no test suite exists)
- `npm run lint` → `npx tsc --noEmit` → `npm run build` (all must pass)
- Backend: from `backend/`, `..\.venv\Scripts\python -c "from app.main import app"`
- Live check: `GET /api/models`, then one quiz + flashcard generation through the UI.

## Backend gotchas
- `backend/.env` is read **once at process start** (pydantic-settings); restart uvicorn after edits. Copy `.env.example`; never commit `.env`.
- No migration tool; tables auto-create on startup. **Schema change → delete `backend/spidey.db`** to regenerate.
- Request/response shapes defined once in `app/schemas.py`; every route returns `response_model=...`.
- PyMuPDF is imported as `import pymupdf` (NOT `fitz`).
- New AI provider = new module in `app/services/` + one `provider` branch in `app/services/ai.py` + a row in `/api/models` (`app/main.py`).

## AI gotchas
- Any provider failure silently returns `seed.py` mock data (`generated_by: "mock"`, toast in UI) — a "working" endpoint may be serving mocks. Check backend logs for exceptions.
- `google-genai`: never create a `genai.Client` per request (transport dies → "client has been closed"). Reuse the module singleton `_client()` in `services/gemini.py`.
- Local Ollama is slow (e.g. `qwen3:8b`); request timeout is 600s in `ollama.py`. Keep `experimental.proxyTimeout` (≥600s) in `next.config.ts` — Next's rewrite proxy otherwise kills slow generations at ~30s (`socket hang up`, ECONNRESET).

## Frontend gotchas
- shadcn uses the **"base-nova"** style backed by `@base-ui/react` (NOT Radix) — e.g. `Button`/`FieldControl` take a `render` prop, not `asChild`. Add components via `npx shadcn add <name>`; don't hand-edit `src/components/ui/*`.
- eslint enforces `react-hooks/set-state-in-effect` — no synchronous setState in effects (defer with `setTimeout(0)`).
- All fetch logic lives in typed helpers in `src/lib/api.ts`; raw `fetch` is not used in pages. Keep types in sync with `app/schemas.py`.
- Global app state + chosen AI model flow through `useStudy()` in `src/lib/context.tsx`; model persisted under `localStorage["spidey-model"]` and sent as `provider`/`model_name`.
- `lucide-react` has no `Spider` icon (`Bug` is used as the logo).

## Collaboration
Follow README "Collaboration & Avoiding Merge Conflicts": the shared "hot spot" files (`context.tsx`, `api.ts`, `main.py`, `schemas.py`, `models.py`, `ai.py`, package files) are append-only; prefer additive changes and new files over edits.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
