# 🕷️ Spidey Tutor

**Hackathon project — a study buddy that turns lecture material into quizzes and flashcards.**

Upload a PDF or paste text → pick a quiz difficulty, question count, timer, and **AI model** → take the quiz → review your answers → create flashcards to study the key concepts.

Built with **Next.js (TypeScript + Tailwind + shadcn/ui)** on the frontend and **FastAPI (Python)** on the backend, with pluggable AI providers (**Gemini API** or **local Ollama**).

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [How It Works](#how-it-works)
3. [Project Structure](#project-structure)
4. [API Reference](#api-reference)
5. [Database](#database)
6. [AI Providers](#ai-providers)
7. [Frontend Conventions](#frontend-conventions)
8. [Backend Conventions](#backend-conventions)
9. [🤝 Collaboration & Avoiding Merge Conflicts](#-collaboration--avoiding-merge-conflicts)
10. [Quality Checks](#quality-checks)

---

## Quick Start

### 1. Frontend (Next.js on `http://localhost:3000`)

```bash
npm install
npm run dev
```

The frontend proxies all `/api/*` calls to the backend automatically. If your backend runs on a different URL, set `BACKEND_URL` in your shell before starting, e.g. `BACKEND_URL=http://localhost:8000 npm run dev`.

### 2. Backend (FastAPI on `http://localhost:8000`)

```bash
cd backend

# Create & activate a virtual environment (Windows / macOS-Linux)
py -m venv .venv                      # Windows
.\.venv\Scripts\activate              # Windows
# python3 -m venv .venv               # macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt

# Config — copy the example and add your key(s)
cp .env.example .env                  # Window: Copy-Item .env.example .env
# edit .env → set GEMINI_API_KEY=...

# Run with auto-reload for development
..\.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
# (from inside backend/, or just: uvicorn app.main:app --reload)
```

### 3. (Optional) Local AI via Ollama

For local, offline generation, install [Ollama](https://ollama.com) and pull a model:

```bash
ollama pull qwen3:8b
```

Ollama runs on `http://localhost:11434` by default — the backend discovers installed models automatically. You'll see them in the **AI Model** dropdown in the UI.

---

## How It Works

### User Flow

```
Home → Add Material (PDF/text) → Material Preview → Quiz Setup (difficulty, count, timer, model)
    → Quiz (timer + progress) → Results (score + review) → Flashcards
```

### Architecture

```text
Browser (Next.js on :3000)
   │  /api/*  (proxied by next.config.ts rewrites)
   ▼
FastAPI (on :8000)
   │
   ├─ POST /api/materials     → PyMuPDF extracts text from PDFs
   ├─ POST /api/quizzes       → AI generates questions (provider selected in UI)
   ├─ POST /api/flashcards    → AI generates flashcards (provider selected in UI)
   │
   ▼
SQLAlchemy ──► SQLite (dev, default) / PostgreSQL (via DATABASE_URL)

AI routing:
   services/ai.py  (dispatcher, decides provider)
      ├── services/gemini.py  (Google Gemini API — requires GEMINI_API_KEY)
      ├── services/ollama.py  (local Ollama — no key needed)
      └── seed.py ──────────── (mock fallback if generation fails)
```

**Model selection is global**: the dropdown (`components/model-select.tsx`) stores the chosen provider/model in the shared context + `localStorage`, and it is sent with every quiz/flashcard generation request. Adding a new provider means editing **one** dispatcher, not multiple endpoints.

---

## Project Structure

```text
├── src/                        # Next.js frontend
│   ├── app/                    #   routes (each folder = a page)
│   │   ├── page.tsx            #     Home
│   │   ├── add/                #     Add study material
│   │   ├── preview/            #     Material preview
│   │   ├── quiz/setup/         #     Quiz configuration
│   │   ├── quiz/page.tsx       #     Quiz screen
│   │   ├── quiz/results/       #     Quiz results + review
│   │   └── flashcards/         #     Flashcard deck
│   ├── components/
│   │   ├── ui/                 #     shadcn/ui components (managed by CLI)
│   │   ├── navbar.tsx
│   │   ├── theme-toggle.tsx
│   │   └── model-select.tsx    #     shared AI model dropdown
│   └── lib/
│       ├── api.ts              #     typed API client (one function per endpoint)
│       ├── context.tsx         #     global UI state (material, quiz, model)
│       └── utils.ts
├── backend/
│   ├── app/
│   │   ├── main.py             #   FastAPI app + route registration
│   │   ├── config.py           #   env-based settings (pydantic-settings)
│   │   ├── database.py         #   SQLAlchemy engine/session
│   │   ├── models.py           #   SQLAlchemy ORM models (tables)
│   │   ├── schemas.py          #   Pydantic request/response models
│   │   ├── seed.py             #   mock quiz/flashcard fallback data
│   │   ├── routers/            #   API endpoints (materials, quizzes, flashcards)
│   │   └── services/           #   PDF extraction, Gemini, Ollama, AI dispatcher
│   ├── requirements.txt
│   ├── .env.example
│   └── .env                    #   <- your secrets (DO NOT COMMIT)
├── next.config.ts              # proxying /api → backend
├── package.json
└── README.md
```

---

## API Reference

All endpoints live under `/api`. From the frontend they are proxied automatically; from a browser or tool they can be hit at `http://localhost:8000` directly.

| Method | Endpoint | Body | Description |
|---|---|---|---|
| `GET` | `/api/health` | — | `{ status, gemini_configured, database }` |
| `GET` | `/api/models` | — | Available models `{ providers: [{ provider, name, label }] }` (Gemini + Ollama) |
| `POST` | `/api/materials` | `{ title?, text }` | Save pasted study material |
| `POST` | `/api/materials/pdf` | `multipart` file | Save PDF, text extracted via PyMuPDF |
| `GET` | `/api/materials/{id}` | — | Fetch material + word/char counts |
| `POST` | `/api/quizzes` | `{ material_id, difficulty, question_count, timer_enabled, timer_minutes, provider, model_name }` | Generate + save a quiz |
| `GET` | `/api/quizzes/{id}` | — | Quiz questions (correct answers hidden) |
| `POST` | `/api/quizzes/{id}/submit` | `{ answers: (int\|null)[], time_taken_seconds }` | Score + full review |
| `GET` | `/api/flashcards?material_id={id}` | — | Saved flashcards for a material |
| `POST` | `/api/flashcards` | `{ material_id, provider, model_name }` | Generate (and replace) flashcards |
| `GET` | `/api/study-notes?material_id={id}` | — | Saved study notes for a material (`null` if none) |
| `POST` | `/api/study-notes` | `{ material_id, provider, model_name }` | Generate (and replace) structured study notes |

**Convention: request/response payloads are defined once in `backend/app/schemas.py` and typed once in `src/lib/api.ts`. When you add an endpoint, update both.**

---

## Database

- **Default (dev):** SQLite at `backend/spidey.db` — zero setup.
- **Production / Postgres:** set `DATABASE_URL` in `backend/.env`, e.g.

  ```env
  DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/spidey
  ```

- Tables are created automatically on startup from `backend/app/models.py` (no migration tool yet).
- ⚠️ **Schema change?** The dev SQLite file is **not** auto-migrated. If you add/rename columns, delete `backend/spidey.db` and let it recreate. Never commit `*.db` files.

---

## AI Providers

Models come from two sources and are chosen **per session in the UI** (persisted in `localStorage`):

| Provider | Requires | Model(s) | Notes |
|---|---|---|---|
| `gemini` | `GEMINI_API_KEY` in `backend/.env` | `gemini-2.5-flash` (set `GEMINI_MODEL`) | Cloud |
| `ollama` | Ollama running on `:11434` | anything pulled, e.g. `qwen3:8b` | Local, free, offline |
| `quick` | nothing | `quick` | **Quick Mode** — deterministic local generation (no API call) |

**Quick Mode:** pick "Quick (deterministic, no AI)" in the AI Model dropdown. Generation runs server-side with pure Python (term frequency + sentence analysis) — cloze quizzes, term-definition flashcards, and sectioned study notes — always drawn from the uploaded material. The same input + configuration always produces the same output, never hits an external API, and responses are stamped `generated_by: "quick"` so the UI can badge them separately from LLM (`"ai"`) and mock-fallback (`"mock"`) content.

Generation flow:

1. The UI sends `{ provider, model_name }` with the request.
2. `services/ai.py` routes to the right provider.
3. If the provider isn't configured, the request fails, or the model returns invalid JSON → **falls back to `seed.py` mock data** and marks the response `generated_by: "mock"` (shown as a toast in the UI).

> 🐛 Gotcha: do **not** create a new `google-genai` `Client` per request — its HTTP transport closes mid-call. Reuse the process-wide client in `services/gemini.py`.

---

## Frontend Conventions

- **Routing:** App Router. Each folder under `src/app/` is a page. Client components that use state/hooks must start with `"use client"`.
- **UI components:** use shadcn/ui primitives from `src/components/ui/`. Add new ones with the CLI (`npx shadcn add <component>`), **don't hand-edit** them.
- **Icons:** `lucide-react` only.
- **API calls:** always go through a typed function in `src/lib/api.ts` — no raw `fetch` in pages.
- **Shared state:** everything flows through `src/lib/context.tsx` (the `useStudy()` hook). Keep it small; prefer passing props for page-local state.
- **Styling:** Tailwind, mostly black/white/gray with a small accent. Respect the existing design tokens in `src/app/globals.css`; it's also where dark mode lives.
- **New page in a folder with multiple files** (e.g. quiz → setup/ and results/)? Keep the layout/loading components in that subfolder so other routes are untouched.

---

## Backend Conventions

- **Endpoints** live in `backend/app/routers/*.py`; register new routers in `backend/app/main.py` via `app.include_router(...)`.
- **Payloads** are Pydantic models in `backend/app/schemas.py`. Return `response_model=...` on every route.
- **Tables** are SQLAlchemy models in `backend/app/models.py`.
- **AI logic** belongs in `backend/app/services/`. A new provider = one new module + one branch in `services/ai.py`. The API layer never talks to a provider directly.
- **Text limits:** large material is truncated client-side-free (providers cap at ~40k chars).
- Environment config lives only in `backend/app/config.py` and is overridden via `backend/.env`.

---

## 🤝 Collaboration & Avoiding Merge Conflicts

This repo is split so people can work in **parallel with minimal collisions**. Follow these rules and you'll rarely (if ever) get a conflict.

### 1. Never edit these files without telling the team

These are the "hot spots" — everyone touches them, so treat them as shared:

| File | Why it conflicts | Rule |
|---|---|---|
| `src/lib/context.tsx` | global state | Only **add** new fields; don't reformat or reorder |
| `src/lib/api.ts` | API types/functions | Only **append** new functions |
| `backend/app/main.py` | router registration | Only **add** `include_router` lines |
| `backend/app/schemas.py` | request models | Only **append** new model classes |
| `backend/app/models.py` | DB tables | Only **add** new model classes (see DB note) |
| `backend/app/services/ai.py` | dispatcher | Only **add** new `provider` branches |
| `package.json` / `package-lock.json` | npm deps | Tell the team before installing; reinstall intentionally |

### 2. Default to **additive** changes

- Prefer **new files** over editing existing ones: a new page = new folder under `src/app/`, a new endpoint = new router file, a new component = new file in `src/components/`.
- Adding one `createRouter` import/line at the **end** of `main.py` is much safer than editing an existing function.
- Don't reformat, rename, or "clean up" code someone else wrote. A production-readability refactor is **not** worth a hackathon conflict.
- Never run a global formatter or `find-and-replace` across files not related to your feature.

### 3. Git workflow

- One person owns the **frontend**, one owns the **backend** → you can literally commit on the same branch with almost no overlap.
- If you must touch shared hotspots, use a **feature branch** and keep it short-lived:
  ```bash
  git checkout -b feat/<your-feature>
  # ...commit small, focused changes...
  git pull --rebase origin main   # before you push
  git push -u origin feat/<your-feature>
  ```
- Pull with `--rebase` to replay your commits cleanly on top of teammate changes.
- Resolve conflicts if any: only the lines you **intentionally changed** should differ — revert anything you didn't mean to touch.
- Commit early and often in small, reviewable chunks.

### 4. Don't break each other's local setup

- **Never commit** these (already in `.gitignore`): `backend/.env`, `backend/spidey.db`, `.venv/`, `node_modules/`, `.next/`.
- When you add a dependency, run the install command yourself and commit `package-lock.json`/`requirements.txt` so teammates get the same versions via `npm install` / `pip install -r`.
- If you change the DB schema, tell the team to delete `backend/spidey.db` (it regenerates).
- If you add an AI provider, don't remove `seed.py` mock data — the fallback keeps the demo runnable without keys.

### 5. Before you push

Run the checks (see below) and make sure you can still run the app. A green build is everyone's baseline.

---

## Quality Checks

Before pushing, from the repo root:

```bash
npm run lint          # frontend lint (eslint)
npx tsc --noEmit      # frontend typecheck
npm run build         # full production build (catches prerender issues)
```

Backend (from `backend/`):

```bash
..\.venv\Scripts\python -c "from app.main import app; print('ok')"   # imports + routes load
```

**Everything must pass** — broken lint/build blocks collaboration and is the fastest way to slow a hackathon down.

---

## Optional: Docker

The stack is Docker-friendly if you need it (backend image = `python:3.12-slim` + `requirements.txt`, database = Postgres container). Full compose setup is a nice stretch goal — keep `DATABASE_URL` env-driven so it swaps cleanly.