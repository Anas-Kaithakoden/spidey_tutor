# Graph Report - spidey_tutor  (2026-09-19)

## Corpus Check
- 91 files · ~48,599 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .example 1, .ico 1)

## Summary
- 1107 nodes · 2622 edges · 72 communities (46 shown, 26 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 175 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c0c865ef`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- schemas.py
- react
- README.md (Architecture & Runbook)
- api.ts
- quick.py
- components.json
- compilerOptions
- youtube.py
- package.json
- Material
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
- Flashcards
- exams.py
- podcasts.py
- useStudy
- layout.tsx
- UrlValidationTests
- chat.py
- gemini.py
- postcss.config.mjs
- File SVG Icon
- Globe SVG Icon
- Next.js Logo
- Vercel Logo
- Window Icon (SVG)
- chat/page.tsx
- YoutubeMaterialEndpointTests
- QuizScreen
- progress/page.tsx
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
- models.py
- radio-group.tsx
- next
- separator.tsx
- slider.tsx
- generate_podcast_script
- PodcastApiTests
- office.py
- main.py
- QuickStudyNotesTests
- context.tsx
- podcast/page.tsx
- study-plan/page.tsx
- groq.py
- ScriptSchemaTests
- PodcastPlayer
- QuickGenerationTests
- ModelRegistrationTests
- openrouter.py
- GenerationTests
- BudgetTests
- _provider_generate_json

## God Nodes (most connected - your core abstractions)
1. `Material` - 45 edges
2. `request()` - 33 edges
3. `README.md (Architecture & Runbook)` - 30 edges
4. `useStudy()` - 29 edges
5. `react` - 27 edges
6. `Base` - 23 edges
7. `lucide-react` - 23 edges
8. `Button()` - 22 edges
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

## Communities (72 total, 26 thin omitted)

### Community 0 - "schemas.py"
Cohesion: 0.13
Nodes (36): Question, Quiz, QuizResult, StudyNote, get_analytics(), get, Session, create_quiz() (+28 more)

### Community 1 - "react"
Cohesion: 0.15
Nodes (23): ref_base_ui_react_button, ref_base_ui_react_merge_props, ref_base_ui_react_use_render, class-variance-authority, lucide-react, ref_next_link, ref_next_navigation, next-themes (+15 more)

### Community 2 - "README.md (Architecture & Runbook)"
Cohesion: 0.07
Nodes (58): AGENTS.md (Agent Gotchas & Rules), Typed API Helpers (src/lib/api.ts), Frontend API Proxy (next.config.ts rewrites), shadcn base-nova Style (Base UI, not Radix), Env Config Read-Once Gotcha (pydantic-settings), React set-state-in-effect eslint Rule, Gemini Client Singleton Reuse, Graphify Knowledge Graph (+50 more)

### Community 3 - "api.ts"
Cohesion: 0.08
Nodes (39): AddMaterial(), handleContinue(), isYoutubeUrl(), ExamResults(), Notes(), handleGenerate(), Preview(), ChatReply (+31 more)

### Community 4 - "quick.py"
Cohesion: 0.15
Nodes (24): _band(), _cloze(), _contains_term(), _default_exam_distribution(), _from_sentence(), generate_exam(), generate_flashcards(), generate_quiz() (+16 more)

### Community 5 - "components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 6 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 7 - "youtube.py"
Cohesion: 0.10
Nodes (25): create_youtube_material(), post, Session, fetch_transcript(), _flatten(), _pick_transcript(), Exception, Choose the best available transcript for a video. Raises the library's… (+17 more)

### Community 8 - "package.json"
Cohesion: 0.12
Nodes (15): name, private, version, @base-ui/react, eslint, eslint-config-next, react-dom, shadcn (+7 more)

### Community 9 - "Material"
Cohesion: 0.21
Nodes (20): Material, create_material(), get_material(), list_materials(), get, post, Session, UploadFile (+12 more)

### Community 10 - "exam.py"
Cohesion: 0.07
Nodes (39): _build_eval_prompt(), _build_generation_prompt(), _coerce_status(), _display_answer(), _error_detail(), evaluate_exam(), _expected_display(), generate_exam() (+31 more)

### Community 11 - "openai_compat.py"
Cohesion: 0.14
Nodes (24): _badge_error(), chat_completion(), chat_json(), chat_text(), CompatConfig, _error_message(), _extract_json(), generate_chat_reply() (+16 more)

### Community 12 - "TranscriptRetrievalTests"
Cohesion: 0.16
Nodes (5): FakeSnippet, FakeTranscript, FakeTranscriptList, TranscriptRetrievalTests, _list()

### Community 15 - "object"
Cohesion: 0.13
Nodes (6): FailureFallbackTests, FakeResponse, ok_completion(), ProviderRoutingTests, object, MetadataTests

### Community 16 - "ai.py"
Cohesion: 0.14
Nodes (15): _error_detail(), _fix_model(), generate_flashcards(), generate_quiz(), generate_study_notes(), _normalize_flashcard(), _normalize_question(), _normalize_study_notes() (+7 more)

### Community 17 - "generate_chat_reply"
Cohesion: 0.24
Nodes (7): generate_chat_reply(), Generate a chat reply grounded in the material. Returns (generated_by,…, generate_chat_reply(), Deterministically answer a question using only the material text. ``history``…, Match a term as a word, or a common inflection of it (e.g. add ~ adds). Used by…, _term_matches_sentence(), ChatDispatchTests

### Community 19 - "eslint.config.mjs"
Cohesion: 0.40
Nodes (4): eslintConfig, ref_eslint_config, ref_eslint_config_next_core_web_vitals, ref_eslint_config_next_typescript

### Community 20 - "Flashcards"
Cohesion: 0.28
Nodes (7): Flashcards(), handleGenerate(), QuizResults(), handleCreateFlashcards(), generateFlashcards(), getFlashcards(), reviewFlashcard()

### Community 21 - "exams.py"
Cohesion: 0.15
Nodes (30): Base, Exam, ExamAttempt, ExamEvaluation, ExamQuestion, A generated exam: a configured set of mixed-type questions., create_exam(), _exam_out() (+22 more)

### Community 22 - "podcasts.py"
Cohesion: 0.05
Nodes (58): PodcastEpisode, A generated Study Podcast episode. The structured script (``lines``) is always…, _confirm_audio_exists(), create_podcast(), delete_podcast(), _episode_out(), get_podcast(), get_podcast_audio() (+50 more)

### Community 23 - "useStudy"
Cohesion: 0.11
Nodes (31): ref_base_ui_react_input, ref_base_ui_react_switch, difficulties, durationOptions, ExamSetup(), handleStart(), questionCounts, modes (+23 more)

### Community 24 - "layout.tsx"
Cohesion: 0.20
Nodes (8): ref_next_font_google, src_app_globals, geistMono, geistSans, metadata, Navbar(), ThemeProvider(), Toaster()

### Community 26 - "chat.py"
Cohesion: 0.27
Nodes (14): ChatMessage, clear_chat(), create_chat_message(), get_chat_messages(), _history(), delete, get, post (+6 more)

### Community 27 - "gemini.py"
Cohesion: 0.14
Nodes (20): _client(), generate_chat_reply_raw(), generate_flashcards_raw(), generate_quiz_raw(), generate_study_notes_raw(), Call Gemini and return raw flashcard dicts (no normalization)., Parse JSON even with markdown fences and trailing commas., Call Gemini and return raw study-notes dict (no normalization). (+12 more)

### Community 36 - "chat/page.tsx"
Cohesion: 0.24
Nodes (10): Chat(), handleClear(), handleKeyDown(), handleSend(), SUGGESTIONS, Textarea(), ChatMessage, clearChat() (+2 more)

### Community 39 - "progress/page.tsx"
Cohesion: 0.12
Nodes (11): ref_base_ui_react_progress, ACTIVITY_ICONS, ActivityRow(), formatDate(), ProgressDashboard(), CardDescription(), CardHeader(), CardTitle() (+3 more)

### Community 40 - "exam/page.tsx"
Cohesion: 0.19
Nodes (10): AnswerState, ExamScreen(), mapAnswers(), readStored(), storageKey(), StoredAnswers, TYPE_LABELS, ExamQuestionType (+2 more)

### Community 41 - "AudioPlayer"
Cohesion: 0.83
Nodes (4): AudioPlayer(), toggle(), toggleBrowser(), toggleGemini()

### Community 42 - "services/audio.py"
Cohesion: 0.12
Nodes (25): generate_summary_text(), generate_tts_audio(), _pcm_to_wav_base64(), Wrap raw PCM (L16, mono) bytes in a WAV container browsers can play., Convert raw PCM base64 (L16) to WAV base64 so <audio> can play it., Generate audio via Gemini TTS. Returns (mime_type, base64_data, generated_by)., Generate 1-min summary text. Returns (generated_by, summary_text)., _wav_bytes_from_pcm() (+17 more)

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

### Community 50 - "models.py"
Cohesion: 0.17
Nodes (15): Settings, get_db(), CreateYoutubeMaterial, SynthesizePodcastAudioTests, EnvConfigTests, BaseSettings, fastapi_testclient, pathlib (+7 more)

### Community 55 - "generate_podcast_script"
Cohesion: 0.28
Nodes (9): _count_words(), _keywords(), generate_podcast_script(), _podcast_focus_terms(), _podcast_reorder(), Move sentences touching the given keywords to the front (stable)., Build a deterministic, material-grounded two-host podcast script. Returns the…, _term_counts() (+1 more)

### Community 57 - "office.py"
Cohesion: 0.43
Nodes (6): _extract_docx(), extract_office_text(), _extract_pptx(), _extract_xlsx(), Extract text from office documents: docx, pptx, xlsx, txt, odt., io

### Community 58 - "main.py"
Cohesion: 0.16
Nodes (15): health(), lifespan(), list_models(), get, create_audio_summary(), post, Session, AudioSummaryOut (+7 more)

### Community 60 - "context.tsx"
Cohesion: 0.20
Nodes (14): Exam, ExamResult, Material, Quiz, QuizResult, ExamConfig, loadModel(), ModelOption (+6 more)

### Community 61 - "podcast/page.tsx"
Cohesion: 0.22
Nodes (10): cn, MODE_SHORT, PodcastPage(), handleDelete(), readEpisodeId(), Props, deletePodcast(), getPodcast() (+2 more)

### Community 62 - "study-plan/page.tsx"
Cohesion: 0.60
Nodes (5): StudyPlanPage(), handleGenerate(), generateStudyPlan(), generateStudyPlanFromPdf(), StudyPlan

### Community 63 - "groq.py"
Cohesion: 0.35
Nodes (11): _cfg(), generate_chat_reply(), generate_flashcards(), generate_json(), generate_quiz(), generate_study_notes(), list_models(), _model() (+3 more)

### Community 65 - "PodcastPlayer"
Cohesion: 0.27
Nodes (7): formatTime(), PodcastPlayer(), retryAudio(), speakBrowserLine(), stopBrowser(), toggleBrowser(), regeneratePodcastAudio()

### Community 66 - "QuickGenerationTests"
Cohesion: 0.20
Nodes (3): _assert_alternation(), object, QuickGenerationTests

### Community 68 - "openrouter.py"
Cohesion: 0.35
Nodes (11): _cfg(), generate_chat_reply(), generate_flashcards(), generate_json(), generate_quiz(), generate_study_notes(), list_models(), _model() (+3 more)

### Community 71 - "_provider_generate_json"
Cohesion: 0.33
Nodes (6): _provider_generate_json(), Pipe a strict-JSON prompt through the selected provider., generate_json(), Generic strict-JSON completion (used by Exam Mode prompts)., _provider_generate_json(), Pipe a strict-JSON prompt through the selected provider.

## Knowledge Gaps
- **128 isolated node(s):** `$schema`, `style`, `rsc`, `tsx`, `config` (+123 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 391 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Material` connect `Material` to `schemas.py`, `chat.py`, `youtube.py`, `flashcards.py`, `ExamApiTests`, `routers/study_plan.py`, `models.py`, `exams.py`, `podcasts.py`, `PodcastApiTests`, `main.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `PodcastApiTests` connect `PodcastApiTests` to `schemas.py`, `Material`, `models.py`, `exams.py`, `podcasts.py`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Why does `ScriptSchemaTests` connect `ScriptSchemaTests` to `models.py`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `Material` (e.g. with `get_analytics()` and `create_audio_summary()`) actually correct?**
  _`Material` has 27 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `style`, `rsc` to the rest of the system?**
  _128 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `schemas.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Should `react` be split into smaller, more focused modules?**
  _Cohesion score 0.14982578397212543 - nodes in this community are weakly interconnected._