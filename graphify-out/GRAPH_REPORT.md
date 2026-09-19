# Graph Report - spidey_tutor  (2026-09-19)

## Corpus Check
- 87 files · ~45,668 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .example 1, .ico 1)

## Summary
- 1065 nodes · 2479 edges · 72 communities (49 shown, 23 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 171 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `39b71d88`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- study_notes.py
- progress/page.tsx
- README.md (Architecture & Runbook)
- api.ts
- quick.py
- components.json
- compilerOptions
- generate_exam
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
- useStudy
- exams.py
- Material
- exam/setup/page.tsx
- layout.tsx
- podcast.py
- chat.py
- schemas.py
- postcss.config.mjs
- File SVG Icon
- Globe SVG Icon
- Next.js Logo
- Vercel Logo
- Window Icon (SVG)
- react
- YoutubeMaterialEndpointTests
- button.tsx
- models.py
- exam/page.tsx
- AudioPlayer
- ollama.py
- dependencies
- flashcards.py
- devDependencies
- main.py
- scripts
- ExamApiTests
- podcast/page.tsx
- test_exams.py
- radio-group.tsx
- next
- separator.tsx
- slider.tsx
- services/audio.py
- PodcastApiTests
- gemini.py
- evaluate_exam
- normalize_question
- context.tsx
- groq.py
- request
- openrouter.py
- ScriptSchemaTests
- PodcastPlayer
- QuickGenerationTests
- ModelRegistrationTests
- CreatePodcast
- GenerationTests
- BudgetTests
- SynthesizePodcastAudioTests

## God Nodes (most connected - your core abstractions)
1. `Material` - 43 edges
2. `request()` - 31 edges
3. `README.md (Architecture & Runbook)` - 30 edges
4. `useStudy()` - 27 edges
5. `react` - 26 edges
6. `Base` - 23 edges
7. `lucide-react` - 22 edges
8. `Button()` - 21 edges
9. `PodcastApiTests` - 20 edges
10. `AGENTS.md (Agent Gotchas & Rules)` - 20 edges

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

## Communities (72 total, 23 thin omitted)

### Community 0 - "study_notes.py"
Cohesion: 0.32
Nodes (11): StudyNote, create_study_notes(), get_study_notes(), get, post, Session, _to_out(), CreateStudyNotes (+3 more)

### Community 1 - "progress/page.tsx"
Cohesion: 0.11
Nodes (11): ref_base_ui_react_progress, ACTIVITY_ICONS, ActivityRow(), formatDate(), ProgressDashboard(), CardDescription(), CardHeader(), CardTitle() (+3 more)

### Community 2 - "README.md (Architecture & Runbook)"
Cohesion: 0.07
Nodes (58): AGENTS.md (Agent Gotchas & Rules), Typed API Helpers (src/lib/api.ts), Frontend API Proxy (next.config.ts rewrites), shadcn base-nova Style (Base UI, not Radix), Env Config Read-Once Gotcha (pydantic-settings), React set-state-in-effect eslint Rule, Gemini Client Singleton Reuse, Graphify Knowledge Graph (+50 more)

### Community 3 - "api.ts"
Cohesion: 0.09
Nodes (27): Notes(), handleGenerate(), ModelSelect(), PROVIDER_BADGE, providerBadge(), ChatReply, CreateExamPayload, CreatePodcastPayload (+19 more)

### Community 4 - "quick.py"
Cohesion: 0.11
Nodes (37): _band(), _cloze(), _contains_term(), _count_words(), _default_exam_distribution(), _from_sentence(), generate_chat_reply(), _keywords() (+29 more)

### Community 5 - "components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 6 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 7 - "generate_exam"
Cohesion: 0.15
Nodes (12): _build_generation_prompt(), _error_detail(), generate_exam(), _min_variety(), plan_exam_distribution(), _provider_generate_json(), Exception, Pipe a strict-JSON prompt through the selected provider. (+4 more)

### Community 8 - "package.json"
Cohesion: 0.12
Nodes (15): name, private, version, @base-ui/react, eslint, eslint-config-next, react-dom, shadcn (+7 more)

### Community 9 - "materials.py"
Cohesion: 0.15
Nodes (23): create_material(), get_material(), list_materials(), get, post, Session, _to_out(), upload_image() (+15 more)

### Community 10 - "exam.py"
Cohesion: 0.18
Nodes (19): _build_eval_prompt(), _coerce_status(), _display_answer(), _expected_display(), grade_deterministic(), _llm_score_review(), _LLMExamEvaluation, _LLMReview (+11 more)

### Community 11 - "openai_compat.py"
Cohesion: 0.14
Nodes (24): _badge_error(), chat_completion(), chat_json(), chat_text(), CompatConfig, _error_message(), _extract_json(), generate_chat_reply() (+16 more)

### Community 12 - "test_youtube_ingestion.py"
Cohesion: 0.05
Nodes (21): fetch_transcript(), _flatten(), _pick_transcript(), Exception, Choose the best available transcript for a video. Raises the library's…, Join transcript snippet text into one readable block., User-facing error raised when a video's transcript cannot be retrieved., Return the plain-text transcript for a YouTube video. Prefers an English… (+13 more)

### Community 15 - "object"
Cohesion: 0.13
Nodes (6): FailureFallbackTests, FakeResponse, ok_completion(), ProviderRoutingTests, object, MetadataTests

### Community 16 - "ai.py"
Cohesion: 0.15
Nodes (13): _error_detail(), generate_flashcards(), generate_quiz(), generate_study_notes(), _normalize_flashcard(), _normalize_question(), _normalize_study_notes(), Exception (+5 more)

### Community 17 - "generate_chat_reply"
Cohesion: 0.43
Nodes (3): generate_chat_reply(), Generate a chat reply grounded in the material. Returns (generated_by,…, ChatDispatchTests

### Community 19 - "eslint.config.mjs"
Cohesion: 0.40
Nodes (4): eslintConfig, ref_eslint_config, ref_eslint_config_next_core_web_vitals, ref_eslint_config_next_typescript

### Community 20 - "useStudy"
Cohesion: 0.15
Nodes (19): ExamResults(), STATUS_META, TYPE_LABELS, Flashcards(), handleGenerate(), Preview(), QuizResults(), handleCreateFlashcards() (+11 more)

### Community 21 - "exams.py"
Cohesion: 0.19
Nodes (25): Exam, ExamAttempt, ExamEvaluation, ExamQuestion, A generated exam: a configured set of mixed-type questions., create_exam(), _exam_out(), get_exam() (+17 more)

### Community 22 - "Material"
Cohesion: 0.14
Nodes (31): Material, PodcastEpisode, A generated Study Podcast episode. The structured script (``lines``) is always…, _confirm_audio_exists(), create_podcast(), delete_podcast(), _episode_out(), get_podcast() (+23 more)

### Community 23 - "exam/setup/page.tsx"
Cohesion: 0.12
Nodes (26): ref_base_ui_react_input, ref_base_ui_react_switch, ref_next_navigation, sonner, difficulties, durationOptions, ExamSetup(), handleStart() (+18 more)

### Community 24 - "layout.tsx"
Cohesion: 0.19
Nodes (9): ref_next_font_google, next-themes, src_app_globals, geistMono, geistSans, metadata, Navbar(), ThemeProvider() (+1 more)

### Community 25 - "podcast.py"
Cohesion: 0.10
Nodes (25): _build_script_prompt(), _error_detail(), Line, max_words_for(), min_lines_for(), min_words_for(), _mock_script(), Any (+17 more)

### Community 26 - "chat.py"
Cohesion: 0.27
Nodes (14): ChatMessage, clear_chat(), create_chat_message(), get_chat_messages(), _history(), delete, get, post (+6 more)

### Community 27 - "schemas.py"
Cohesion: 0.17
Nodes (27): Quiz, get_analytics(), get, Session, create_quiz(), get_quiz(), get, post (+19 more)

### Community 36 - "react"
Cohesion: 0.23
Nodes (11): react, Chat(), handleClear(), handleKeyDown(), handleSend(), SUGGESTIONS, Textarea(), ChatMessage (+3 more)

### Community 38 - "button.tsx"
Cohesion: 0.19
Nodes (8): ref_base_ui_react_button, lucide-react, ref_next_link, QuizScreen(), ThemeToggle(), Button(), buttonVariants, submitQuiz()

### Community 39 - "models.py"
Cohesion: 0.31
Nodes (9): Base, get_db(), Question, QuizResult, _to_out(), base64, DeclarativeBase, sqlalchemy (+1 more)

### Community 40 - "exam/page.tsx"
Cohesion: 0.13
Nodes (15): ref_base_ui_react_merge_props, ref_base_ui_react_use_render, class-variance-authority, AnswerState, ExamScreen(), mapAnswers(), readStored(), storageKey() (+7 more)

### Community 41 - "AudioPlayer"
Cohesion: 0.83
Nodes (4): AudioPlayer(), toggle(), toggleBrowser(), toggleGemini()

### Community 42 - "ollama.py"
Cohesion: 0.10
Nodes (28): create_youtube_material(), post, Session, available_models(), _chat_json(), _chat_text(), generate_chat_reply(), generate_flashcards() (+20 more)

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

### Community 49 - "podcast/page.tsx"
Cohesion: 0.17
Nodes (14): cn, MODE_SHORT, PodcastPage(), handleDelete(), readEpisodeId(), MODE_LABELS, Props, SPEEDS (+6 more)

### Community 50 - "test_exams.py"
Cohesion: 0.15
Nodes (11): Settings, ExamOutSchemaTests, EnvConfigTests, QuickFlashcardTests, QuickStudyNotesTests, BaseSettings, json, pathlib (+3 more)

### Community 55 - "services/audio.py"
Cohesion: 0.18
Nodes (15): create_audio_summary(), post, Session, AudioSummaryOut, CreateAudioSummary, generate_summary_text(), generate_tts_audio(), _pcm_to_wav_base64() (+7 more)

### Community 57 - "gemini.py"
Cohesion: 0.17
Nodes (15): _client(), generate_chat_reply_raw(), generate_flashcards_raw(), generate_json(), generate_quiz_raw(), generate_study_notes_raw(), Call Gemini and return raw study-notes dict (no normalization)., Call Gemini and return a grounded answer to the last user message. ``history``… (+7 more)

### Community 58 - "evaluate_exam"
Cohesion: 0.34
Nodes (5): evaluate_exam(), Grade an exam attempt. Returns ``(grading_method, result_dict, error_detail)``…, _validate_eval(), EvaluationTests, object

### Community 59 - "normalize_question"
Cohesion: 0.24
Nodes (5): normalize_question(), Validate + normalize a raw provider question into a canonical dict. Raises…, DeterministicGradingTests, NormalizeQuestionTests, _question()

### Community 60 - "context.tsx"
Cohesion: 0.20
Nodes (14): Exam, ExamResult, Material, Quiz, QuizResult, ExamConfig, loadModel(), ModelOption (+6 more)

### Community 61 - "groq.py"
Cohesion: 0.35
Nodes (11): _cfg(), generate_chat_reply(), generate_flashcards(), generate_json(), generate_quiz(), generate_study_notes(), list_models(), _model() (+3 more)

### Community 62 - "request"
Cohesion: 0.45
Nodes (10): AddMaterial(), handleContinue(), isYoutubeUrl(), createMaterial(), createYoutubeMaterial(), listExams(), request(), uploadImage() (+2 more)

### Community 63 - "openrouter.py"
Cohesion: 0.35
Nodes (11): _cfg(), generate_chat_reply(), generate_flashcards(), generate_json(), generate_quiz(), generate_study_notes(), list_models(), _model() (+3 more)

### Community 65 - "PodcastPlayer"
Cohesion: 0.27
Nodes (7): formatTime(), PodcastPlayer(), retryAudio(), speakBrowserLine(), stopBrowser(), toggleBrowser(), regeneratePodcastAudio()

### Community 66 - "QuickGenerationTests"
Cohesion: 0.20
Nodes (3): _assert_alternation(), object, QuickGenerationTests

### Community 68 - "CreatePodcast"
Cohesion: 0.32
Nodes (3): CreatePodcast, field_validator, CreatePodcastSchemaTests

## Knowledge Gaps
- **127 isolated node(s):** `$schema`, `style`, `rsc`, `tsx`, `config` (+122 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 383 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Material` connect `Material` to `study_notes.py`, `models.py`, `materials.py`, `ollama.py`, `flashcards.py`, `main.py`, `ExamApiTests`, `test_exams.py`, `exams.py`, `services/audio.py`, `PodcastApiTests`, `chat.py`, `schemas.py`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `FailureFallbackTests` connect `object` to `test_exams.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `PodcastApiTests` connect `PodcastApiTests` to `schemas.py`, `Material`, `models.py`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `Material` (e.g. with `get_analytics()` and `create_audio_summary()`) actually correct?**
  _`Material` has 26 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `style`, `rsc` to the rest of the system?**
  _127 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `progress/page.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.11067193675889328 - nodes in this community are weakly interconnected._
- **Should `README.md (Architecture & Runbook)` be split into smaller, more focused modules?**
  _Cohesion score 0.06957047791893527 - nodes in this community are weakly interconnected._