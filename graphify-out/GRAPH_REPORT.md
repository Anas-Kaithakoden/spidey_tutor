# Graph Report - spidey_tutor  (2026-09-19)

## Corpus Check
- 81 files · ~38,050 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .example 1, .ico 1)

## Summary
- 909 nodes · 2071 edges · 55 communities (37 shown, 18 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 144 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c00aa960`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- schemas.py
- progress/page.tsx
- README.md (Architecture & Runbook)
- api.ts
- quick.py
- components.json
- compilerOptions
- test_quick_generation.py
- package.json
- materials.py
- exam.py
- openai_compat.py
- test_youtube_ingestion.py
- select.tsx
- QuickChatReplyTests
- test_providers.py
- ai.py
- generate_chat_reply
- QuickQuizTests
- eslint.config.mjs
- flashcards/page.tsx
- exams.py
- notes/page.tsx
- exam/setup/page.tsx
- layout.tsx
- request
- Material
- quizzes.py
- postcss.config.mjs
- File SVG Icon
- Globe SVG Icon
- Next.js Logo
- Vercel Logo
- Window Icon (SVG)
- chat/page.tsx
- YoutubeMaterialEndpointTests
- useStudy
- test_exams.py
- exam/page.tsx
- AudioPlayer
- youtube.py
- dependencies
- flashcards.py
- devDependencies
- main.py
- scripts
- ExamApiTests
- generate_chat_reply
- GenerationTests
- radio-group.tsx
- next
- separator.tsx
- slider.tsx

## God Nodes (most connected - your core abstractions)
1. `Material` - 33 edges
2. `README.md (Architecture & Runbook)` - 30 edges
3. `request()` - 26 edges
4. `useStudy()` - 25 edges
5. `react` - 23 edges
6. `Base` - 20 edges
7. `AGENTS.md (Agent Gotchas & Rules)` - 20 edges
8. `lucide-react` - 19 edges
9. `Button()` - 18 edges
10. `compilerOptions` - 16 edges

## Surprising Connections (you probably didn't know these)
- `Typed API Helpers (src/lib/api.ts)` --semantically_similar_to--> `Typed API Client (src/lib/api.ts)`  [INFERRED] [semantically similar]
  AGENTS.md → README.md
- `Env Config Read-Once Gotcha (pydantic-settings)` --semantically_similar_to--> `Env Config (backend/.env, config.py)`  [INFERRED] [semantically similar]
  AGENTS.md → README.md
- `Hot-Spot Append-only Files` --semantically_similar_to--> `Collaboration & Merge-Conflict Rules`  [INFERRED] [semantically similar]
  AGENTS.md → README.md
- `useStudy() Global App Context` --semantically_similar_to--> `useStudy() Hook`  [INFERRED] [semantically similar]
  AGENTS.md → README.md
- `Verification Pipeline (lint, tsc, build, import)` --semantically_similar_to--> `Quality Checks (lint, tsc, build, import)`  [INFERRED] [semantically similar]
  AGENTS.md → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Frontend-Backend Request/Response Contract** — readme_fastapi_backend, readme_schemas_contract, readme_api_client, agents_api_proxy [INFERRED 0.85]
- **Pluggable AI Provider System** — readme_ai_dispatcher, readme_gemini_provider, readme_ollama_provider, readme_quick_mode, readme_seed_mock [INFERRED 0.85]
- **Spidey Tutor Study Features** — readme_quiz_flow, readme_flashcards, readme_study_notes, readme_grounded_chat, readme_analytics [INFERRED 0.85]

## Communities (55 total, 18 thin omitted)

### Community 0 - "schemas.py"
Cohesion: 0.17
Nodes (25): StudyNote, get_analytics(), get, Session, create_study_notes(), get_study_notes(), get, post (+17 more)

### Community 1 - "progress/page.tsx"
Cohesion: 0.14
Nodes (15): Preview(), ACTIVITY_ICONS, ActivityRow(), formatDate(), ProgressDashboard(), Props, Card(), CardContent() (+7 more)

### Community 2 - "README.md (Architecture & Runbook)"
Cohesion: 0.07
Nodes (58): AGENTS.md (Agent Gotchas & Rules), Typed API Helpers (src/lib/api.ts), Frontend API Proxy (next.config.ts rewrites), shadcn base-nova Style (Base UI, not Radix), Env Config Read-Once Gotcha (pydantic-settings), React set-state-in-effect eslint Rule, Gemini Client Singleton Reuse, Graphify Knowledge Graph (+50 more)

### Community 3 - "api.ts"
Cohesion: 0.08
Nodes (34): ModelSelect(), PROVIDER_BADGE, providerBadge(), ChatReply, CreateExamPayload, CreateQuizPayload, Exam, ExamAnswerIn (+26 more)

### Community 4 - "quick.py"
Cohesion: 0.15
Nodes (25): _band(), _cloze(), _default_exam_distribution(), _from_sentence(), generate_exam(), generate_flashcards(), generate_quiz(), generate_study_notes() (+17 more)

### Community 5 - "components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 6 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 7 - "test_quick_generation.py"
Cohesion: 0.24
Nodes (5): QuickFlashcardTests, QuickStudyNotesTests, pathlib, sys, unittest

### Community 8 - "package.json"
Cohesion: 0.12
Nodes (15): name, private, version, @base-ui/react, eslint, eslint-config-next, react-dom, shadcn (+7 more)

### Community 9 - "materials.py"
Cohesion: 0.05
Nodes (62): create_audio_summary(), post, Session, create_material(), get_material(), list_materials(), get, post (+54 more)

### Community 10 - "exam.py"
Cohesion: 0.06
Nodes (43): Any, _build_eval_prompt(), _build_generation_prompt(), _coerce_status(), _display_answer(), _error_detail(), evaluate_exam(), _expected_display() (+35 more)

### Community 11 - "openai_compat.py"
Cohesion: 0.09
Nodes (46): _cfg(), generate_chat_reply(), generate_flashcards(), generate_json(), generate_quiz(), generate_study_notes(), list_models(), _model() (+38 more)

### Community 12 - "test_youtube_ingestion.py"
Cohesion: 0.05
Nodes (21): fetch_transcript(), _flatten(), _pick_transcript(), Exception, Choose the best available transcript for a video. Raises the library's…, Join transcript snippet text into one readable block., User-facing error raised when a video's transcript cannot be retrieved., Return the plain-text transcript for a YouTube video. Prefers an English… (+13 more)

### Community 15 - "test_providers.py"
Cohesion: 0.10
Nodes (10): Settings, EnvConfigTests, FailureFallbackTests, FakeResponse, ModelRegistrationTests, ok_completion(), ProviderRoutingTests, object (+2 more)

### Community 16 - "ai.py"
Cohesion: 0.15
Nodes (13): _error_detail(), generate_flashcards(), generate_quiz(), generate_study_notes(), _normalize_flashcard(), _normalize_question(), _normalize_study_notes(), Exception (+5 more)

### Community 17 - "generate_chat_reply"
Cohesion: 0.43
Nodes (3): generate_chat_reply(), Generate a chat reply grounded in the material. Returns (generated_by,…, ChatDispatchTests

### Community 19 - "eslint.config.mjs"
Cohesion: 0.40
Nodes (4): eslintConfig, ref_eslint_config, ref_eslint_config_next_core_web_vitals, ref_eslint_config_next_typescript

### Community 20 - "flashcards/page.tsx"
Cohesion: 0.14
Nodes (16): ref_base_ui_react_button, lucide-react, ref_next_link, next-themes, sonner, Flashcards(), handleGenerate(), QuizResults() (+8 more)

### Community 21 - "exams.py"
Cohesion: 0.19
Nodes (25): Exam, ExamAttempt, ExamEvaluation, ExamQuestion, A generated exam: a configured set of mixed-type questions., create_exam(), _exam_out(), get_exam() (+17 more)

### Community 22 - "notes/page.tsx"
Cohesion: 0.16
Nodes (15): ref_base_ui_react_merge_props, ref_base_ui_react_use_render, class-variance-authority, ref_next_navigation, ExamResults(), STATUS_META, TYPE_LABELS, Notes() (+7 more)

### Community 23 - "exam/setup/page.tsx"
Cohesion: 0.13
Nodes (20): ref_base_ui_react_input, ref_base_ui_react_switch, cn, difficulties, durationOptions, ExamSetup(), handleStart(), questionCounts (+12 more)

### Community 24 - "layout.tsx"
Cohesion: 0.20
Nodes (8): ref_next_font_google, src_app_globals, geistMono, geistSans, metadata, Navbar(), ThemeProvider(), Toaster()

### Community 25 - "request"
Cohesion: 0.53
Nodes (9): AddMaterial(), handleContinue(), isYoutubeUrl(), createMaterial(), createYoutubeMaterial(), request(), uploadImage(), uploadOffice() (+1 more)

### Community 26 - "Material"
Cohesion: 0.22
Nodes (16): ChatMessage, Material, clear_chat(), create_chat_message(), get_chat_messages(), _history(), get, post (+8 more)

### Community 27 - "quizzes.py"
Cohesion: 0.28
Nodes (14): Quiz, create_quiz(), get_quiz(), get, post, Session, _quiz_out(), submit_quiz() (+6 more)

### Community 36 - "chat/page.tsx"
Cohesion: 0.23
Nodes (11): react, Chat(), handleClear(), handleKeyDown(), handleSend(), SUGGESTIONS, Textarea(), ChatMessage (+3 more)

### Community 38 - "useStudy"
Cohesion: 0.18
Nodes (5): ref_base_ui_react_progress, QuizScreen(), Progress(), submitQuiz(), useStudy()

### Community 39 - "test_exams.py"
Cohesion: 0.19
Nodes (12): Base, get_db(), Question, QuizResult, _to_out(), ExamResultOut, ExamOutSchemaTests, DeclarativeBase (+4 more)

### Community 40 - "exam/page.tsx"
Cohesion: 0.19
Nodes (10): AnswerState, ExamScreen(), mapAnswers(), readStored(), storageKey(), StoredAnswers, TYPE_LABELS, ExamQuestionType (+2 more)

### Community 41 - "AudioPlayer"
Cohesion: 0.83
Nodes (4): AudioPlayer(), toggle(), toggleBrowser(), toggleGemini()

### Community 42 - "youtube.py"
Cohesion: 0.19
Nodes (14): create_youtube_material(), post, Session, canonical_url(), _extract_video_id(), fetch_video_metadata(), _first_path_segment(), _is_valid_video_id() (+6 more)

### Community 43 - "dependencies"
Cohesion: 0.17
Nodes (12): dependencies, @base-ui/react, class-variance-authority, cn, lucide-react, next, next-themes, react (+4 more)

### Community 44 - "flashcards.py"
Cohesion: 0.35
Nodes (11): Flashcard, create_flashcards(), get_flashcards(), get, post, Session, review_flashcard(), _to_out() (+3 more)

### Community 45 - "devDependencies"
Cohesion: 0.22
Nodes (9): devDependencies, eslint, eslint-config-next, tailwindcss, @tailwindcss/postcss, @types/node, @types/react, @types/react-dom (+1 more)

### Community 46 - "main.py"
Cohesion: 0.27
Nodes (9): health(), lifespan(), list_models(), get, HealthOut, ModelInfo, ModelsOut, FastAPI (+1 more)

### Community 47 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, start

### Community 49 - "generate_chat_reply"
Cohesion: 0.33
Nodes (6): _contains_term(), generate_chat_reply(), _keywords(), Deterministically answer a question using only the material text. ``history``…, Match a term as a word, or a common inflection of it (e.g. add ~ adds). Used by…, _term_matches_sentence()

## Knowledge Gaps
- **120 isolated node(s):** `$schema`, `style`, `rsc`, `tsx`, `config` (+115 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 335 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Material` connect `Material` to `schemas.py`, `test_exams.py`, `materials.py`, `youtube.py`, `flashcards.py`, `main.py`, `ExamApiTests`, `exams.py`, `quizzes.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `Base` connect `test_exams.py` to `schemas.py`, `YoutubeMaterialEndpointTests`, `flashcards.py`, `test_youtube_ingestion.py`, `main.py`, `ExamApiTests`, `exams.py`, `Material`, `quizzes.py`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `Material` (e.g. with `get_analytics()` and `create_audio_summary()`) actually correct?**
  _`Material` has 19 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `style`, `rsc` to the rest of the system?**
  _120 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `progress/page.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.13768115942028986 - nodes in this community are weakly interconnected._
- **Should `README.md (Architecture & Runbook)` be split into smaller, more focused modules?**
  _Cohesion score 0.06957047791893527 - nodes in this community are weakly interconnected._
- **Should `api.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.08108108108108109 - nodes in this community are weakly interconnected._