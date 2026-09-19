# Graph Report - spidey_tutor  (2026-09-19)

## Corpus Check
- 92 files · ~49,229 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .example 1, .ico 1)

## Summary
- 1114 nodes · 2638 edges · 65 communities (43 shown, 22 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 175 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7fe1f26b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- schemas.py
- button.tsx
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
- test_providers.py
- ai.py
- generate_chat_reply
- QuickQuizTests
- eslint.config.mjs
- useStudy
- models.py
- podcasts.py
- quiz/setup/page.tsx
- layout.tsx
- UrlValidationTests
- Material
- logging
- postcss.config.mjs
- File SVG Icon
- Globe SVG Icon
- Next.js Logo
- Vercel Logo
- Window Icon (SVG)
- request
- YoutubeMaterialEndpointTests
- chat/page.tsx
- quiz/page.tsx
- exam/page.tsx
- AudioPlayer
- services/audio.py
- dependencies
- flashcards.py
- devDependencies
- StudyPlanApiTests
- scripts
- ExamApiTests
- routers/study_plan.py
- test_podcast.py
- radio-group.tsx
- next
- separator.tsx
- study_notes.py
- PodcastApiTests
- main.py
- context.tsx
- react
- ScriptSchemaTests
- PodcastPlayer
- QuickGenerationTests
- openrouter.py
- GenerationTests
- BudgetTests

## God Nodes (most connected - your core abstractions)
1. `Material` - 45 edges
2. `request()` - 33 edges
3. `README.md (Architecture & Runbook)` - 30 edges
4. `useStudy()` - 29 edges
5. `react` - 27 edges
6. `Base` - 23 edges
7. `lucide-react` - 23 edges
8. `Button()` - 23 edges
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

## Communities (65 total, 22 thin omitted)

### Community 0 - "schemas.py"
Cohesion: 0.20
Nodes (23): Quiz, get_analytics(), get, Session, create_quiz(), get_quiz(), get, post (+15 more)

### Community 1 - "button.tsx"
Cohesion: 0.11
Nodes (21): ref_base_ui_react_button, lucide-react, ref_next_link, Preview(), ACTIVITY_ICONS, ActivityRow(), formatDate(), ProgressDashboard() (+13 more)

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
Cohesion: 0.10
Nodes (26): create_youtube_material(), post, Session, fetch_transcript(), _flatten(), _pick_transcript(), Exception, Choose the best available transcript for a video. Raises the library's… (+18 more)

### Community 8 - "package.json"
Cohesion: 0.12
Nodes (15): name, private, version, @base-ui/react, eslint, eslint-config-next, react-dom, shadcn (+7 more)

### Community 9 - "materials.py"
Cohesion: 0.15
Nodes (23): create_material(), get_material(), list_materials(), get, post, Session, UploadFile, _to_out() (+15 more)

### Community 10 - "exam.py"
Cohesion: 0.07
Nodes (39): _build_eval_prompt(), _build_generation_prompt(), _coerce_status(), _display_answer(), _error_detail(), evaluate_exam(), _expected_display(), generate_exam() (+31 more)

### Community 11 - "openai_compat.py"
Cohesion: 0.11
Nodes (37): _cfg(), generate_chat_reply(), generate_flashcards(), generate_json(), generate_quiz(), generate_study_notes(), list_models(), _model() (+29 more)

### Community 12 - "TranscriptRetrievalTests"
Cohesion: 0.16
Nodes (5): FakeSnippet, FakeTranscript, FakeTranscriptList, TranscriptRetrievalTests, _list()

### Community 15 - "test_providers.py"
Cohesion: 0.10
Nodes (10): Settings, EnvConfigTests, FailureFallbackTests, FakeResponse, ModelRegistrationTests, ok_completion(), ProviderRoutingTests, object (+2 more)

### Community 16 - "ai.py"
Cohesion: 0.13
Nodes (16): _error_detail(), _fix_model(), generate_flashcards(), generate_quiz(), generate_study_notes(), _normalize_flashcard(), _normalize_question(), _normalize_study_notes() (+8 more)

### Community 17 - "generate_chat_reply"
Cohesion: 0.24
Nodes (7): generate_chat_reply(), Generate a chat reply grounded in the material. Returns (generated_by,…, _chat_text(), generate_chat_reply(), Free-form chat completion (no forced JSON format)., Answer the last user message, grounded in the study material., ChatDispatchTests

### Community 19 - "eslint.config.mjs"
Cohesion: 0.40
Nodes (4): eslintConfig, ref_eslint_config, ref_eslint_config_next_core_web_vitals, ref_eslint_config_next_typescript

### Community 20 - "useStudy"
Cohesion: 0.14
Nodes (18): ref_base_ui_react_merge_props, ref_base_ui_react_use_render, class-variance-authority, ExamResults(), STATUS_META, TYPE_LABELS, Flashcards(), handleGenerate() (+10 more)

### Community 21 - "models.py"
Cohesion: 0.16
Nodes (30): Base, Exam, ExamAttempt, ExamEvaluation, ExamQuestion, Question, QuizResult, A generated exam: a configured set of mixed-type questions. (+22 more)

### Community 22 - "podcasts.py"
Cohesion: 0.05
Nodes (58): PodcastEpisode, A generated Study Podcast episode. The structured script (``lines``) is always…, _confirm_audio_exists(), create_podcast(), delete_podcast(), _episode_out(), get_podcast(), get_podcast_audio() (+50 more)

### Community 23 - "quiz/setup/page.tsx"
Cohesion: 0.18
Nodes (16): ref_base_ui_react_switch, ExamSetup(), handleStart(), PodcastSetup(), handleGenerate(), difficulties, questionCounts, QuizSetup() (+8 more)

### Community 24 - "layout.tsx"
Cohesion: 0.19
Nodes (9): ref_next_font_google, next-themes, src_app_globals, geistMono, geistSans, metadata, Navbar(), ThemeProvider() (+1 more)

### Community 26 - "Material"
Cohesion: 0.27
Nodes (15): ChatMessage, Material, clear_chat(), create_chat_message(), get_chat_messages(), _history(), delete, get (+7 more)

### Community 27 - "logging"
Cohesion: 0.12
Nodes (23): generate_tts_audio(), Generate audio via Gemini TTS. Returns (mime_type, base64_data, generated_by)., _client(), generate_chat_reply_raw(), generate_flashcards_raw(), generate_quiz_raw(), generate_study_notes_raw(), Call Gemini and return raw flashcard dicts (no normalization). (+15 more)

### Community 36 - "request"
Cohesion: 0.22
Nodes (17): AddMaterial(), handleContinue(), isYoutubeUrl(), Chat(), handleClear(), handleKeyDown(), handleSend(), clearChat() (+9 more)

### Community 38 - "chat/page.tsx"
Cohesion: 0.20
Nodes (13): ref_next_navigation, sonner, SUGGESTIONS, SUGGESTIONS_ML, Notes(), handleGenerate(), LanguageToggle(), LanguageToggleProps (+5 more)

### Community 39 - "quiz/page.tsx"
Cohesion: 0.18
Nodes (4): ref_base_ui_react_progress, QuizScreen(), Progress(), submitQuiz()

### Community 40 - "exam/page.tsx"
Cohesion: 0.19
Nodes (10): AnswerState, ExamScreen(), mapAnswers(), readStored(), storageKey(), StoredAnswers, TYPE_LABELS, ExamQuestionType (+2 more)

### Community 41 - "AudioPlayer"
Cohesion: 0.83
Nodes (4): AudioPlayer(), toggle(), toggleBrowser(), toggleGemini()

### Community 42 - "services/audio.py"
Cohesion: 0.18
Nodes (17): generate_summary_text(), _pcm_to_wav_base64(), Wrap raw PCM (L16, mono) bytes in a WAV container browsers can play., Convert raw PCM base64 (L16) to WAV base64 so <audio> can play it., Generate 1-min summary text. Returns (generated_by, summary_text)., _wav_bytes_from_pcm(), available_models(), _chat_json() (+9 more)

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

### Community 49 - "routers/study_plan.py"
Cohesion: 0.31
Nodes (10): _build_plan_out(), create_study_plan(), create_study_plan_from_pdf(), post, Session, UploadFile, _validate_exam_date(), CreateStudyPlan (+2 more)

### Community 50 - "test_podcast.py"
Cohesion: 0.15
Nodes (16): get_db(), _to_out(), CreateYoutubeMaterial, ExamResultOut, MaterialOut, ExamOutSchemaTests, SynthesizePodcastAudioTests, fastapi_testclient (+8 more)

### Community 54 - "study_notes.py"
Cohesion: 0.32
Nodes (11): StudyNote, create_study_notes(), get_study_notes(), get, post, Session, _to_out(), CreateStudyNotes (+3 more)

### Community 58 - "main.py"
Cohesion: 0.16
Nodes (15): health(), lifespan(), list_models(), get, create_audio_summary(), post, Session, AudioSummaryOut (+7 more)

### Community 60 - "context.tsx"
Cohesion: 0.20
Nodes (14): Exam, ExamResult, Material, Quiz, QuizResult, ExamConfig, loadModel(), ModelOption (+6 more)

### Community 62 - "react"
Cohesion: 0.13
Nodes (20): ref_base_ui_react_input, ref_base_ui_react_slider, cn, react, difficulties, durationOptions, questionCounts, modes (+12 more)

### Community 65 - "PodcastPlayer"
Cohesion: 0.27
Nodes (7): formatTime(), PodcastPlayer(), retryAudio(), speakBrowserLine(), stopBrowser(), toggleBrowser(), regeneratePodcastAudio()

### Community 66 - "QuickGenerationTests"
Cohesion: 0.20
Nodes (3): _assert_alternation(), object, QuickGenerationTests

### Community 68 - "openrouter.py"
Cohesion: 0.20
Nodes (17): _provider_generate_json(), Pipe a strict-JSON prompt through the selected provider., generate_json(), Generic strict-JSON completion (used by Exam Mode prompts)., _cfg(), generate_chat_reply(), generate_flashcards(), generate_json() (+9 more)

## Knowledge Gaps
- **130 isolated node(s):** `$schema`, `style`, `rsc`, `tsx`, `config` (+125 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 394 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Material` connect `Material` to `schemas.py`, `youtube.py`, `materials.py`, `flashcards.py`, `ExamApiTests`, `routers/study_plan.py`, `test_podcast.py`, `models.py`, `podcasts.py`, `study_notes.py`, `PodcastApiTests`, `main.py`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `PodcastApiTests` connect `PodcastApiTests` to `schemas.py`, `test_podcast.py`, `models.py`, `podcasts.py`, `Material`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `Base` connect `models.py` to `schemas.py`, `main.py`, `YoutubeMaterialEndpointTests`, `flashcards.py`, `ExamApiTests`, `test_podcast.py`, `podcasts.py`, `study_notes.py`, `PodcastApiTests`, `Material`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `Material` (e.g. with `get_analytics()` and `create_audio_summary()`) actually correct?**
  _`Material` has 27 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `style`, `rsc` to the rest of the system?**
  _130 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `button.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.10793650793650794 - nodes in this community are weakly interconnected._
- **Should `README.md (Architecture & Runbook)` be split into smaller, more focused modules?**
  _Cohesion score 0.06957047791893527 - nodes in this community are weakly interconnected._