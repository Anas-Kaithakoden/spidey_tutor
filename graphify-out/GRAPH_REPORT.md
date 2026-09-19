# Graph Report - spidey_tutor  (2026-09-19)

## Corpus Check
- 95 files · ~51,214 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .example 1, .ico 1)

## Summary
- 1137 nodes · 2733 edges · 75 communities (49 shown, 26 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 182 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `611e311e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- quizzes.py
- progress/page.tsx
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
- TranscriptRetrievalTests
- select.tsx
- QuickChatReplyTests
- object
- ai.py
- generate_chat_reply
- QuickQuizTests
- eslint.config.mjs
- useStudy
- exams.py
- podcast.py
- request
- layout.tsx
- UrlValidationTests
- chat.py
- services/audio.py
- postcss.config.mjs
- File SVG Icon
- Globe SVG Icon
- Next.js Logo
- Vercel Logo
- Window Icon (SVG)
- logging
- YoutubeMaterialEndpointTests
- chat/page.tsx
- quiz/page.tsx
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
- separator.tsx
- schemas.py
- button.tsx
- PodcastApiTests
- CreatePodcast
- generate_podcast_script
- formula-sheet/page.tsx
- context.tsx
- ProviderError
- react
- _split_sentences
- ScriptSchemaTests
- PodcastPlayer
- QuickGenerationTests
- _provider_generate_json
- openrouter.py
- GenerationTests
- BudgetTests
- ModelRegistrationTests
- SynthesizePodcastAudioTests
- QuickStudyNotesTests
- slider.tsx

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

## Communities (75 total, 26 thin omitted)

### Community 0 - "quizzes.py"
Cohesion: 0.26
Nodes (15): Question, Quiz, create_quiz(), get_quiz(), get, post, Session, _quiz_out() (+7 more)

### Community 1 - "progress/page.tsx"
Cohesion: 0.14
Nodes (15): Preview(), ACTIVITY_ICONS, ActivityRow(), formatDate(), ProgressDashboard(), Props, Card(), CardContent() (+7 more)

### Community 2 - "README.md (Architecture & Runbook)"
Cohesion: 0.07
Nodes (58): AGENTS.md (Agent Gotchas & Rules), Typed API Helpers (src/lib/api.ts), Frontend API Proxy (next.config.ts rewrites), shadcn base-nova Style (Base UI, not Radix), Env Config Read-Once Gotcha (pydantic-settings), React set-state-in-effect eslint Rule, Gemini Client Singleton Reuse, Graphify Knowledge Graph (+50 more)

### Community 3 - "api.ts"
Cohesion: 0.08
Nodes (32): MODE_SHORT, PodcastPage(), handleDelete(), readEpisodeId(), MODE_LABELS, Props, SPEEDS, ChatReply (+24 more)

### Community 4 - "quick.py"
Cohesion: 0.18
Nodes (19): _band(), _cloze(), _contains_term(), _default_exam_distribution(), _from_sentence(), generate_exam(), generate_quiz(), _mcq_from() (+11 more)

### Community 5 - "components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 6 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 7 - "youtube.py"
Cohesion: 0.10
Nodes (26): create_youtube_material(), post, Session, fetch_transcript(), _flatten(), _pick_transcript(), Exception, Choose the best available transcript for a video. Raises the library's… (+18 more)

### Community 8 - "package.json"
Cohesion: 0.12
Nodes (15): name, private, version, @base-ui/react, eslint, eslint-config-next, react-dom, shadcn (+7 more)

### Community 9 - "materials.py"
Cohesion: 0.11
Nodes (30): create_material(), get_material(), list_materials(), get, post, Session, UploadFile, _to_out() (+22 more)

### Community 10 - "exam.py"
Cohesion: 0.06
Nodes (42): _build_eval_prompt(), _build_generation_prompt(), _coerce_status(), _display_answer(), _error_detail(), evaluate_exam(), _expected_display(), generate_exam() (+34 more)

### Community 11 - "openai_compat.py"
Cohesion: 0.19
Nodes (19): _badge_error(), chat_completion(), chat_json(), chat_text(), CompatConfig, _error_message(), generate_chat_reply(), generate_flashcards() (+11 more)

### Community 12 - "TranscriptRetrievalTests"
Cohesion: 0.16
Nodes (5): FakeSnippet, FakeTranscript, FakeTranscriptList, TranscriptRetrievalTests, _list()

### Community 15 - "object"
Cohesion: 0.13
Nodes (6): FailureFallbackTests, FakeResponse, ok_completion(), ProviderRoutingTests, object, MetadataTests

### Community 16 - "ai.py"
Cohesion: 0.15
Nodes (15): _error_detail(), _fix_model(), generate_flashcards(), generate_quiz(), generate_study_notes(), _normalize_flashcard(), _normalize_question(), _normalize_study_notes() (+7 more)

### Community 17 - "generate_chat_reply"
Cohesion: 0.31
Nodes (5): generate_chat_reply(), Generate a chat reply grounded in the material. Returns (generated_by,…, generate_chat_reply(), Deterministically answer a question using only the material text. ``history``…, ChatDispatchTests

### Community 19 - "eslint.config.mjs"
Cohesion: 0.40
Nodes (4): eslintConfig, ref_eslint_config, ref_eslint_config_next_core_web_vitals, ref_eslint_config_next_typescript

### Community 20 - "useStudy"
Cohesion: 0.14
Nodes (18): ref_base_ui_react_merge_props, ref_base_ui_react_use_render, class-variance-authority, ExamResults(), STATUS_META, TYPE_LABELS, Flashcards(), handleGenerate() (+10 more)

### Community 21 - "exams.py"
Cohesion: 0.18
Nodes (23): Exam, ExamQuestion, A generated exam: a configured set of mixed-type questions., create_exam(), _exam_out(), get_exam(), get_latest_result(), list_exams() (+15 more)

### Community 22 - "podcast.py"
Cohesion: 0.11
Nodes (25): _build_script_prompt(), _error_detail(), generate_podcast_script(), Line, max_words_for(), min_lines_for(), min_words_for(), _mock_script() (+17 more)

### Community 23 - "request"
Cohesion: 0.20
Nodes (21): AddMaterial(), handleContinue(), isYoutubeUrl(), ExamSetup(), handleStart(), PodcastSetup(), handleGenerate(), QuizSetup() (+13 more)

### Community 24 - "layout.tsx"
Cohesion: 0.19
Nodes (9): ref_next_font_google, next-themes, src_app_globals, geistMono, geistSans, metadata, Navbar(), ThemeProvider() (+1 more)

### Community 26 - "chat.py"
Cohesion: 0.27
Nodes (14): ChatMessage, clear_chat(), create_chat_message(), get_chat_messages(), _history(), delete, get, post (+6 more)

### Community 27 - "services/audio.py"
Cohesion: 0.06
Nodes (49): create_audio_summary(), post, Session, generate_summary_text(), generate_tts_audio(), _pcm_to_wav_base64(), podcast_duration_seconds(), Wrap raw PCM (L16, mono) bytes in a WAV container browsers can play. (+41 more)

### Community 36 - "logging"
Cohesion: 0.13
Nodes (22): Settings, _build_pdf_bytes(), create_formula_sheet(), download_formula_sheet_pdf(), _get_material_text(), post, Session, Generate PDF and return as file download. (+14 more)

### Community 38 - "chat/page.tsx"
Cohesion: 0.14
Nodes (20): ref_next_navigation, sonner, Chat(), handleClear(), handleKeyDown(), handleSend(), SUGGESTIONS, SUGGESTIONS_ML (+12 more)

### Community 39 - "quiz/page.tsx"
Cohesion: 0.18
Nodes (4): ref_base_ui_react_progress, QuizScreen(), Progress(), submitQuiz()

### Community 40 - "exam/page.tsx"
Cohesion: 0.19
Nodes (10): AnswerState, ExamScreen(), mapAnswers(), readStored(), storageKey(), StoredAnswers, TYPE_LABELS, ExamQuestionType (+2 more)

### Community 41 - "AudioPlayer"
Cohesion: 0.83
Nodes (4): AudioPlayer(), toggle(), toggleBrowser(), toggleGemini()

### Community 42 - "Material"
Cohesion: 0.21
Nodes (23): Material, PodcastEpisode, A generated Study Podcast episode. The structured script (``lines``) is always…, _confirm_audio_exists(), create_podcast(), delete_podcast(), _episode_out(), get_podcast() (+15 more)

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
Cohesion: 0.35
Nodes (11): _cfg(), generate_chat_reply(), generate_flashcards(), generate_json(), generate_quiz(), generate_study_notes(), list_models(), _model() (+3 more)

### Community 50 - "main.py"
Cohesion: 0.18
Nodes (22): Base, get_db(), lifespan(), ExamAttempt, ExamEvaluation, QuizResult, get_analytics(), get (+14 more)

### Community 54 - "schemas.py"
Cohesion: 0.12
Nodes (33): health(), list_models(), get, StudyNote, create_study_notes(), get_study_notes(), get, post (+25 more)

### Community 55 - "button.tsx"
Cohesion: 0.30
Nodes (6): ref_base_ui_react_button, lucide-react, ref_next_link, ThemeToggle(), Button(), buttonVariants

### Community 57 - "CreatePodcast"
Cohesion: 0.28
Nodes (3): CreatePodcast, field_validator, CreatePodcastSchemaTests

### Community 58 - "generate_podcast_script"
Cohesion: 0.28
Nodes (9): _count_words(), _keywords(), generate_podcast_script(), _podcast_focus_terms(), _podcast_reorder(), Move sentences touching the given keywords to the front (stable)., Build a deterministic, material-grounded two-host podcast script. Returns the…, _term_counts() (+1 more)

### Community 59 - "formula-sheet/page.tsx"
Cohesion: 0.36
Nodes (7): FormulaSheetPage(), handleDownload(), handleGenerate(), Textarea(), downloadFormulaSheetPdf(), FormulaSheet, generateFormulaSheet()

### Community 60 - "context.tsx"
Cohesion: 0.20
Nodes (14): Exam, ExamResult, Material, Quiz, QuizResult, ExamConfig, loadModel(), ModelOption (+6 more)

### Community 61 - "ProviderError"
Cohesion: 0.25
Nodes (7): _extract_json(), ProviderError, A provider request failed. ``user_message`` is a safe, end-user-friendly reason…, True when the provider/model told us it can't do json_object mode., Robustly parse JSON out of a completion that may add prose/fences., _unsupported_json_mode(), RuntimeError

### Community 62 - "react"
Cohesion: 0.11
Nodes (25): ref_base_ui_react_input, ref_base_ui_react_switch, cn, react, difficulties, durationOptions, questionCounts, modes (+17 more)

### Community 63 - "_split_sentences"
Cohesion: 0.29
Nodes (7): generate_flashcards(), generate_study_notes(), _heading_for(), Deterministically build term-definition flashcards from the material., Deterministically structure the material into study notes., Split material into reasonably long, deterministic sentences., _split_sentences()

### Community 65 - "PodcastPlayer"
Cohesion: 0.27
Nodes (7): formatTime(), PodcastPlayer(), retryAudio(), speakBrowserLine(), stopBrowser(), toggleBrowser(), regeneratePodcastAudio()

### Community 66 - "QuickGenerationTests"
Cohesion: 0.20
Nodes (3): _assert_alternation(), object, QuickGenerationTests

### Community 67 - "_provider_generate_json"
Cohesion: 0.50
Nodes (4): generate_json(), Generic strict-JSON completion (used by Exam Mode prompts)., _provider_generate_json(), Pipe a strict-JSON prompt through the selected provider.

### Community 68 - "openrouter.py"
Cohesion: 0.35
Nodes (11): _cfg(), generate_chat_reply(), generate_flashcards(), generate_json(), generate_quiz(), generate_study_notes(), list_models(), _model() (+3 more)

## Knowledge Gaps
- **131 isolated node(s):** `$schema`, `style`, `rsc`, `tsx`, `config` (+126 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 395 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Material` connect `Material` to `quizzes.py`, `logging`, `youtube.py`, `materials.py`, `flashcards.py`, `ExamApiTests`, `main.py`, `exams.py`, `schemas.py`, `PodcastApiTests`, `chat.py`, `services/audio.py`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `PodcastApiTests` connect `PodcastApiTests` to `quizzes.py`, `main.py`, `Material`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `get_db()` connect `main.py` to `quizzes.py`, `logging`, `materials.py`, `Material`, `flashcards.py`, `StudyPlanApiTests`, `ExamApiTests`, `exams.py`, `schemas.py`, `PodcastApiTests`, `chat.py`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `Material` (e.g. with `get_analytics()` and `create_audio_summary()`) actually correct?**
  _`Material` has 30 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `style`, `rsc` to the rest of the system?**
  _131 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `progress/page.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.13768115942028986 - nodes in this community are weakly interconnected._
- **Should `README.md (Architecture & Runbook)` be split into smaller, more focused modules?**
  _Cohesion score 0.06957047791893527 - nodes in this community are weakly interconnected._