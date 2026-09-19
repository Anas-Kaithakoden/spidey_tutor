# Graph Report - spidey_tutor  (2026-09-19)

## Corpus Check
- 95 files · ~51,424 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .example 1, .ico 1)

## Summary
- 1141 nodes · 2750 edges · 74 communities (49 shown, 25 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 182 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b118d41b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- transcript.py
- study-plan/page.tsx
- README.md (Architecture & Runbook)
- api.ts
- quick.py
- components.json
- compilerOptions
- youtube.py
- package.json
- materials.py
- exam.py
- openai_compat.py
- test_youtube_ingestion.py
- select.tsx
- QuickChatReplyTests
- object
- ai.py
- generate_chat_reply
- QuickQuizTests
- eslint.config.mjs
- flashcards/page.tsx
- exams.py
- podcast.py
- request
- layout.tsx
- UrlValidationTests
- chat.py
- ollama.py
- postcss.config.mjs
- File SVG Icon
- Globe SVG Icon
- Next.js Logo
- Vercel Logo
- Window Icon (SVG)
- routers/formula_sheet.py
- YoutubeMaterialEndpointTests
- chat/page.tsx
- QuizScreen
- exam/page.tsx
- AudioPlayer
- Material
- dependencies
- flashcards.py
- devDependencies
- StudyPlanApiTests
- scripts
- ExamApiTests
- groq.py
- main.py
- radio-group.tsx
- next
- cn
- schemas.py
- study_notes.py
- PodcastApiTests
- CreatePodcast
- .test_raises_when_request_blocked
- formula-sheet/page.tsx
- context.tsx
- ProviderError
- useStudy
- Settings
- ScriptSchemaTests
- PodcastPlayer
- QuickGenerationTests
- gemini.py
- openrouter.py
- GenerationTests
- BudgetTests
- ModelRegistrationTests
- SynthesizePodcastAudioTests
- test_exams.py

## God Nodes (most connected - your core abstractions)
1. `Material` - 49 edges
2. `request()` - 34 edges
3. `useStudy()` - 31 edges
4. `README.md (Architecture & Runbook)` - 30 edges
5. `react` - 28 edges
6. `lucide-react` - 24 edges
7. `Button()` - 24 edges
8. `Base` - 23 edges
9. `get_db()` - 20 edges
10. `PodcastApiTests` - 20 edges

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

## Communities (74 total, 25 thin omitted)

### Community 0 - "transcript.py"
Cohesion: 0.19
Nodes (12): fetch_transcript(), _flatten(), _pick_transcript(), Exception, Choose the best available transcript for a video. Raises the library's…, Join transcript snippet text into one readable block., User-facing error raised when a video's transcript cannot be retrieved., Return the plain-text transcript for a YouTube video. Prefers an English… (+4 more)

### Community 1 - "study-plan/page.tsx"
Cohesion: 0.14
Nodes (14): ACTIVITY_ICONS, ActivityRow(), formatDate(), ProgressDashboard(), StudyPlanPage(), handleGenerate(), CardDescription(), CardHeader() (+6 more)

### Community 2 - "README.md (Architecture & Runbook)"
Cohesion: 0.07
Nodes (58): AGENTS.md (Agent Gotchas & Rules), Typed API Helpers (src/lib/api.ts), Frontend API Proxy (next.config.ts rewrites), shadcn base-nova Style (Base UI, not Radix), Env Config Read-Once Gotcha (pydantic-settings), React set-state-in-effect eslint Rule, Gemini Client Singleton Reuse, Graphify Knowledge Graph (+50 more)

### Community 3 - "api.ts"
Cohesion: 0.08
Nodes (33): MODE_SHORT, PodcastPage(), handleDelete(), readEpisodeId(), MODE_LABELS, Props, SPEEDS, ChatReply (+25 more)

### Community 4 - "quick.py"
Cohesion: 0.11
Nodes (37): _band(), _cloze(), _contains_term(), _count_words(), _default_exam_distribution(), _from_sentence(), generate_chat_reply(), _keywords() (+29 more)

### Community 5 - "components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 6 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 7 - "youtube.py"
Cohesion: 0.19
Nodes (14): create_youtube_material(), post, Session, canonical_url(), _extract_video_id(), fetch_video_metadata(), _first_path_segment(), _is_valid_video_id() (+6 more)

### Community 8 - "package.json"
Cohesion: 0.12
Nodes (15): name, private, version, @base-ui/react, eslint, eslint-config-next, react-dom, shadcn (+7 more)

### Community 9 - "materials.py"
Cohesion: 0.08
Nodes (39): create_material(), get_material(), list_materials(), get, post, Session, UploadFile, _to_out() (+31 more)

### Community 10 - "exam.py"
Cohesion: 0.07
Nodes (40): _build_eval_prompt(), _build_generation_prompt(), _coerce_status(), _display_answer(), _error_detail(), evaluate_exam(), _expected_display(), generate_exam() (+32 more)

### Community 11 - "openai_compat.py"
Cohesion: 0.18
Nodes (21): _badge_error(), chat_completion(), chat_json(), chat_text(), CompatConfig, _error_message(), generate_chat_reply(), generate_flashcards() (+13 more)

### Community 12 - "test_youtube_ingestion.py"
Cohesion: 0.21
Nodes (6): FakeSnippet, FakeTranscript, FakeTranscriptList, TranscriptRetrievalTests, contextlib, sqlalchemy_pool

### Community 15 - "object"
Cohesion: 0.13
Nodes (6): FailureFallbackTests, FakeResponse, ok_completion(), ProviderRoutingTests, object, MetadataTests

### Community 16 - "ai.py"
Cohesion: 0.16
Nodes (14): _error_detail(), _fix_model(), generate_flashcards(), generate_quiz(), generate_study_notes(), _normalize_flashcard(), _normalize_question(), _normalize_study_notes() (+6 more)

### Community 17 - "generate_chat_reply"
Cohesion: 0.24
Nodes (7): generate_chat_reply(), Generate a chat reply grounded in the material. Returns (generated_by,…, _chat_text(), generate_chat_reply(), Free-form chat completion (no forced JSON format)., Answer the last user message, grounded in the study material., ChatDispatchTests

### Community 19 - "eslint.config.mjs"
Cohesion: 0.40
Nodes (4): eslintConfig, ref_eslint_config, ref_eslint_config_next_core_web_vitals, ref_eslint_config_next_typescript

### Community 20 - "flashcards/page.tsx"
Cohesion: 0.27
Nodes (8): Flashcards(), handleGenerate(), QuizResults(), handleCreateFlashcards(), FlashcardOut, generateFlashcards(), getFlashcards(), reviewFlashcard()

### Community 21 - "exams.py"
Cohesion: 0.21
Nodes (23): Exam, ExamAttempt, ExamEvaluation, ExamQuestion, A generated exam: a configured set of mixed-type questions., create_exam(), _exam_out(), get_exam() (+15 more)

### Community 22 - "podcast.py"
Cohesion: 0.10
Nodes (24): _build_script_prompt(), Line, max_words_for(), min_lines_for(), min_words_for(), _mock_script(), _provider_generate_json(), Any (+16 more)

### Community 23 - "request"
Cohesion: 0.22
Nodes (17): AddMaterial(), handleContinue(), isYoutubeUrl(), Chat(), handleClear(), handleKeyDown(), handleSend(), clearChat() (+9 more)

### Community 24 - "layout.tsx"
Cohesion: 0.19
Nodes (9): ref_next_font_google, next-themes, src_app_globals, geistMono, geistSans, metadata, Navbar(), ThemeProvider() (+1 more)

### Community 26 - "chat.py"
Cohesion: 0.27
Nodes (14): ChatMessage, clear_chat(), create_chat_message(), get_chat_messages(), _history(), delete, get, post (+6 more)

### Community 27 - "ollama.py"
Cohesion: 0.21
Nodes (15): generate_summary_text(), Generate 1-min summary text. Returns (generated_by, summary_text)., generate_formula_sheet(), Extract formulas and key equations. Returns (generated_by, formulas)., _robust_json_loads(), available_models(), _chat_json(), generate_flashcards() (+7 more)

### Community 36 - "routers/formula_sheet.py"
Cohesion: 0.36
Nodes (10): _build_pdf_bytes(), create_formula_sheet(), download_formula_sheet_pdf(), _get_material_text(), post, Session, Generate PDF and return as file download., CreateFormulaSheet (+2 more)

### Community 38 - "chat/page.tsx"
Cohesion: 0.10
Nodes (34): ref_base_ui_react_button, ref_base_ui_react_merge_props, ref_base_ui_react_use_render, class-variance-authority, lucide-react, ref_next_link, ref_next_navigation, sonner (+26 more)

### Community 40 - "exam/page.tsx"
Cohesion: 0.12
Nodes (12): ref_base_ui_react_progress, AnswerState, ExamScreen(), mapAnswers(), readStored(), storageKey(), StoredAnswers, TYPE_LABELS (+4 more)

### Community 41 - "AudioPlayer"
Cohesion: 0.83
Nodes (4): AudioPlayer(), toggle(), toggleBrowser(), toggleGemini()

### Community 42 - "Material"
Cohesion: 0.16
Nodes (28): Material, PodcastEpisode, A generated Study Podcast episode. The structured script (``lines``) is always…, _confirm_audio_exists(), create_podcast(), delete_podcast(), _episode_out(), get_podcast() (+20 more)

### Community 43 - "dependencies"
Cohesion: 0.17
Nodes (12): dependencies, @base-ui/react, class-variance-authority, cn, lucide-react, next, next-themes, react (+4 more)

### Community 44 - "flashcards.py"
Cohesion: 0.35
Nodes (11): Flashcard, create_flashcards(), get_flashcards(), get, post, Session, review_flashcard(), _to_out() (+3 more)

### Community 45 - "devDependencies"
Cohesion: 0.22
Nodes (9): devDependencies, eslint, eslint-config-next, tailwindcss, @tailwindcss/postcss, @types/node, @types/react, @types/react-dom (+1 more)

### Community 47 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, start

### Community 49 - "groq.py"
Cohesion: 0.33
Nodes (12): _cfg(), generate_chat_reply(), generate_flashcards(), generate_formula_sheet(), generate_json(), generate_quiz(), generate_study_notes(), list_models() (+4 more)

### Community 50 - "main.py"
Cohesion: 0.13
Nodes (23): Base, get_db(), lifespan(), create_audio_summary(), post, Session, _to_out(), AudioSummaryOut (+15 more)

### Community 53 - "cn"
Cohesion: 0.18
Nodes (5): ref_base_ui_react_separator, ref_base_ui_react_slider, ref_base_ui_react_switch, cn, Switch()

### Community 54 - "schemas.py"
Cohesion: 0.11
Nodes (41): health(), list_models(), get, Question, Quiz, QuizResult, get_analytics(), get (+33 more)

### Community 55 - "study_notes.py"
Cohesion: 0.32
Nodes (11): StudyNote, create_study_notes(), get_study_notes(), get, post, Session, _to_out(), CreateStudyNotes (+3 more)

### Community 57 - "CreatePodcast"
Cohesion: 0.28
Nodes (3): CreatePodcast, field_validator, CreatePodcastSchemaTests

### Community 59 - "formula-sheet/page.tsx"
Cohesion: 0.36
Nodes (7): FormulaSheetPage(), handleDownload(), handleGenerate(), Textarea(), downloadFormulaSheetPdf(), FormulaSheet, generateFormulaSheet()

### Community 60 - "context.tsx"
Cohesion: 0.20
Nodes (14): Exam, ExamResult, Material, Quiz, QuizResult, ExamConfig, loadModel(), ModelOption (+6 more)

### Community 61 - "ProviderError"
Cohesion: 0.18
Nodes (10): _extract_json(), ProviderError, A provider request failed. ``user_message`` is a safe, end-user-friendly reason…, True when the provider/model told us it can't do json_object mode., Robustly parse JSON out of a completion that may add prose/fences., _unsupported_json_mode(), _error_detail(), Exception (+2 more)

### Community 62 - "useStudy"
Cohesion: 0.13
Nodes (28): ref_base_ui_react_input, react, difficulties, durationOptions, ExamSetup(), handleStart(), questionCounts, modes (+20 more)

### Community 63 - "Settings"
Cohesion: 0.67
Nodes (3): Settings, EnvConfigTests, BaseSettings

### Community 65 - "PodcastPlayer"
Cohesion: 0.27
Nodes (7): formatTime(), PodcastPlayer(), retryAudio(), speakBrowserLine(), stopBrowser(), toggleBrowser(), regeneratePodcastAudio()

### Community 66 - "QuickGenerationTests"
Cohesion: 0.20
Nodes (3): _assert_alternation(), object, QuickGenerationTests

### Community 67 - "gemini.py"
Cohesion: 0.19
Nodes (15): _client(), generate_chat_reply_raw(), generate_flashcards_raw(), generate_json(), generate_quiz_raw(), generate_study_notes_raw(), Call Gemini and return raw flashcard dicts (no normalization)., Parse JSON even with markdown fences and trailing commas. (+7 more)

### Community 68 - "openrouter.py"
Cohesion: 0.33
Nodes (12): _cfg(), generate_chat_reply(), generate_flashcards(), generate_formula_sheet(), generate_json(), generate_quiz(), generate_study_notes(), list_models() (+4 more)

### Community 73 - "test_exams.py"
Cohesion: 0.19
Nodes (9): ExamOutSchemaTests, QuickFlashcardTests, QuickStudyNotesTests, fastapi_testclient, json, pathlib, sys, tempfile (+1 more)

## Knowledge Gaps
- **131 isolated node(s):** `$schema`, `style`, `rsc`, `tsx`, `config` (+126 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 396 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Material` connect `Material` to `routers/formula_sheet.py`, `youtube.py`, `materials.py`, `test_exams.py`, `flashcards.py`, `ExamApiTests`, `main.py`, `exams.py`, `schemas.py`, `study_notes.py`, `PodcastApiTests`, `chat.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `UrlValidationTests` connect `UrlValidationTests` to `test_youtube_ingestion.py`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `PodcastApiTests` connect `PodcastApiTests` to `main.py`, `Material`, `schemas.py`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `Material` (e.g. with `get_analytics()` and `create_audio_summary()`) actually correct?**
  _`Material` has 30 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `style`, `rsc` to the rest of the system?**
  _131 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `study-plan/page.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.13852813852813853 - nodes in this community are weakly interconnected._
- **Should `README.md (Architecture & Runbook)` be split into smaller, more focused modules?**
  _Cohesion score 0.06957047791893527 - nodes in this community are weakly interconnected._