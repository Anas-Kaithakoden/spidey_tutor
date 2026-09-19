# Graph Report - spidey_tutor  (2026-09-19)

## Corpus Check
- 75 files · ~28,669 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .example 1, .ico 1)

## Summary
- 748 nodes · 1614 edges · 48 communities (35 shown, 13 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 114 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f6baaa42`
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
- test_youtube_ingestion.py
- package.json
- routers/audio.py
- transcript.py
- openai_compat.py
- TranscriptRetrievalTests
- cn
- QuickChatReplyTests
- object
- ai.py
- generate_chat_reply
- QuickQuizTests
- eslint.config.mjs
- flashcards/page.tsx
- ollama.py
- quiz/page.tsx
- setup/page.tsx
- layout.tsx
- add/page.tsx
- button.tsx
- UrlValidationTests
- postcss.config.mjs
- File SVG Icon
- Globe SVG Icon
- Next.js Logo
- Vercel Logo
- Window Icon (SVG)
- chat/page.tsx
- YoutubeMaterialEndpointTests
- preview/page.tsx
- config.py
- ModelRegistrationTests
- AudioPlayer
- youtube.py
- dependencies
- context.tsx
- devDependencies
- office.py
- scripts

## God Nodes (most connected - your core abstractions)
1. `README.md (Architecture & Runbook)` - 30 edges
2. `Material` - 27 edges
3. `react` - 20 edges
4. `request()` - 20 edges
5. `AGENTS.md (Agent Gotchas & Rules)` - 20 edges
6. `useStudy()` - 19 edges
7. `lucide-react` - 16 edges
8. `compilerOptions` - 16 edges
9. `generate_chat_reply()` - 15 edges
10. `UrlValidationTests` - 15 edges

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

## Communities (48 total, 13 thin omitted)

### Community 0 - "schemas.py"
Cohesion: 0.05
Nodes (103): Base, get_db(), health(), lifespan(), list_models(), get, ChatMessage, Flashcard (+95 more)

### Community 1 - "progress/page.tsx"
Cohesion: 0.16
Nodes (10): ACTIVITY_ICONS, ActivityRow(), formatDate(), ProgressDashboard(), Card(), CardDescription(), CardHeader(), CardTitle() (+2 more)

### Community 2 - "README.md (Architecture & Runbook)"
Cohesion: 0.07
Nodes (58): AGENTS.md (Agent Gotchas & Rules), Typed API Helpers (src/lib/api.ts), Frontend API Proxy (next.config.ts rewrites), shadcn base-nova Style (Base UI, not Radix), Env Config Read-Once Gotcha (pydantic-settings), React set-state-in-effect eslint Rule, Gemini Client Singleton Reuse, Graphify Knowledge Graph (+50 more)

### Community 3 - "api.ts"
Cohesion: 0.14
Nodes (19): Notes(), handleGenerate(), ModelSelect(), PROVIDER_BADGE, providerBadge(), ChatReply, CreateQuizPayload, generateStudyNotes() (+11 more)

### Community 4 - "quick.py"
Cohesion: 0.13
Nodes (26): _band(), _cloze(), _contains_term(), generate_chat_reply(), _keywords(), generate_flashcards(), generate_quiz(), generate_study_notes() (+18 more)

### Community 5 - "components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 6 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 7 - "test_youtube_ingestion.py"
Cohesion: 0.22
Nodes (7): QuickFlashcardTests, QuickStudyNotesTests, fastapi_testclient, pathlib, sqlalchemy_pool, sys, unittest

### Community 8 - "package.json"
Cohesion: 0.12
Nodes (15): name, private, version, @base-ui/react, eslint, eslint-config-next, react-dom, shadcn (+7 more)

### Community 9 - "routers/audio.py"
Cohesion: 0.12
Nodes (21): create_audio_summary(), post, Session, generate_summary_text(), generate_tts_audio(), _pcm_to_wav_base64(), Convert raw PCM base64 (L16) to WAV base64 so <audio> can play it., Generate audio via Gemini TTS. Returns (mime_type, base64_data, generated_by). (+13 more)

### Community 10 - "transcript.py"
Cohesion: 0.19
Nodes (12): fetch_transcript(), _flatten(), _pick_transcript(), Exception, Choose the best available transcript for a video. Raises the library's…, Join transcript snippet text into one readable block., User-facing error raised when a video's transcript cannot be retrieved., Return the plain-text transcript for a YouTube video. Prefers an English… (+4 more)

### Community 11 - "openai_compat.py"
Cohesion: 0.10
Nodes (42): _cfg(), generate_chat_reply(), generate_flashcards(), generate_quiz(), generate_study_notes(), list_models(), _model(), Provider/models advertised to the UI (must have a matching provider key). (+34 more)

### Community 12 - "TranscriptRetrievalTests"
Cohesion: 0.16
Nodes (5): FakeSnippet, FakeTranscript, FakeTranscriptList, TranscriptRetrievalTests, _list()

### Community 13 - "cn"
Cohesion: 0.06
Nodes (10): ref_base_ui_react_progress, ref_base_ui_react_radio, ref_base_ui_react_radio_group, ref_base_ui_react_select, ref_base_ui_react_separator, ref_base_ui_react_slider, ref_base_ui_react_switch, cn (+2 more)

### Community 15 - "object"
Cohesion: 0.13
Nodes (6): FailureFallbackTests, FakeResponse, ok_completion(), ProviderRoutingTests, MetadataTests, object

### Community 16 - "ai.py"
Cohesion: 0.15
Nodes (13): _error_detail(), generate_flashcards(), generate_quiz(), generate_study_notes(), _normalize_flashcard(), _normalize_question(), _normalize_study_notes(), Exception (+5 more)

### Community 17 - "generate_chat_reply"
Cohesion: 0.31
Nodes (5): generate_chat_reply(), Generate a chat reply grounded in the material. Returns (generated_by,…, generate_chat_reply_raw(), Call Gemini and return a grounded answer to the last user message. ``history``…, ChatDispatchTests

### Community 19 - "eslint.config.mjs"
Cohesion: 0.40
Nodes (4): eslintConfig, ref_eslint_config, ref_eslint_config_next_core_web_vitals, ref_eslint_config_next_typescript

### Community 20 - "flashcards/page.tsx"
Cohesion: 0.20
Nodes (10): sonner, Flashcards(), handleGenerate(), QuizResults(), handleCreateFlashcards(), Toaster(), FlashcardOut, generateFlashcards() (+2 more)

### Community 21 - "ollama.py"
Cohesion: 0.24
Nodes (12): available_models(), _chat_json(), _chat_text(), generate_chat_reply(), generate_flashcards(), generate_quiz(), generate_study_notes(), Free-form chat completion (no forced JSON format). (+4 more)

### Community 22 - "quiz/page.tsx"
Cohesion: 0.21
Nodes (7): ref_base_ui_react_merge_props, ref_base_ui_react_use_render, class-variance-authority, QuizScreen(), Badge(), badgeVariants, submitQuiz()

### Community 23 - "setup/page.tsx"
Cohesion: 0.27
Nodes (9): ref_next_navigation, difficulties, questionCounts, QuizSetup(), handleStart(), timerOptions, Label(), createQuiz() (+1 more)

### Community 24 - "layout.tsx"
Cohesion: 0.15
Nodes (10): nextConfig, next, ref_next_font_google, next-themes, src_app_globals, geistMono, geistSans, metadata (+2 more)

### Community 25 - "add/page.tsx"
Cohesion: 0.36
Nodes (11): ref_base_ui_react_input, AddMaterial(), handleContinue(), isYoutubeUrl(), Input(), createMaterial(), createYoutubeMaterial(), request() (+3 more)

### Community 26 - "button.tsx"
Cohesion: 0.30
Nodes (6): ref_base_ui_react_button, lucide-react, ref_next_link, ThemeToggle(), Button(), buttonVariants

### Community 36 - "chat/page.tsx"
Cohesion: 0.23
Nodes (11): react, Chat(), handleClear(), handleKeyDown(), handleSend(), SUGGESTIONS, Textarea(), ChatMessage (+3 more)

### Community 38 - "preview/page.tsx"
Cohesion: 0.43
Nodes (6): Preview(), Props, CardContent(), AudioSummaryOut, generateAudioSummary(), useStudy()

### Community 39 - "config.py"
Cohesion: 0.40
Nodes (4): Settings, EnvConfigTests, BaseSettings, pydantic_settings

### Community 41 - "AudioPlayer"
Cohesion: 0.83
Nodes (4): AudioPlayer(), toggle(), toggleBrowser(), toggleGemini()

### Community 42 - "youtube.py"
Cohesion: 0.23
Nodes (11): canonical_url(), _extract_video_id(), fetch_video_metadata(), _first_path_segment(), _is_valid_video_id(), parse_youtube_url(), Extract and return a valid YouTube video ID from ``url``. Raises ``ValueError``…, Return the canonical watch URL for a video ID. (+3 more)

### Community 43 - "dependencies"
Cohesion: 0.17
Nodes (12): dependencies, @base-ui/react, class-variance-authority, cn, lucide-react, next, next-themes, react (+4 more)

### Community 44 - "context.tsx"
Cohesion: 0.24
Nodes (11): Material, Quiz, QuizResult, loadModel(), ModelOption, QuizConfig, saveModel(), StudyContext (+3 more)

### Community 45 - "devDependencies"
Cohesion: 0.22
Nodes (9): devDependencies, eslint, eslint-config-next, tailwindcss, @tailwindcss/postcss, @types/node, @types/react, @types/react-dom (+1 more)

### Community 46 - "office.py"
Cohesion: 0.43
Nodes (6): _extract_docx(), extract_office_text(), _extract_pptx(), _extract_xlsx(), Extract text from office documents: docx, pptx, xlsx, txt, odt., io

### Community 47 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, start

## Knowledge Gaps
- **106 isolated node(s):** `$schema`, `style`, `rsc`, `tsx`, `config` (+101 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 293 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Material` connect `schemas.py` to `routers/audio.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `UrlValidationTests` connect `UrlValidationTests` to `test_youtube_ingestion.py`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `react` connect `chat/page.tsx` to `progress/page.tsx`, `api.ts`, `preview/page.tsx`, `package.json`, `context.tsx`, `cn`, `flashcards/page.tsx`, `quiz/page.tsx`, `setup/page.tsx`, `layout.tsx`, `add/page.tsx`, `button.tsx`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `Material` (e.g. with `get_analytics()` and `create_audio_summary()`) actually correct?**
  _`Material` has 16 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `style`, `rsc` to the rest of the system?**
  _106 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `schemas.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05142941349837902 - nodes in this community are weakly interconnected._
- **Should `README.md (Architecture & Runbook)` be split into smaller, more focused modules?**
  _Cohesion score 0.06957047791893527 - nodes in this community are weakly interconnected._