# Graph Report - spidey_tutor  (2026-09-19)

## Corpus Check
- 73 files · ~27,368 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .example 1, .ico 1)

## Summary
- 734 nodes · 1569 edges · 43 communities (27 shown, 16 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 112 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `34fc0d8b`
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
- services/audio.py
- youtube.py
- openai_compat.py
- TranscriptRetrievalTests
- select.tsx
- QuickChatReplyTests
- object
- ai.py
- generate_chat_reply
- QuickQuizTests
- eslint.config.mjs
- flashcards/page.tsx
- radio-group.tsx
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
- Settings
- ModelRegistrationTests
- AudioPlayer
- QuickStudyNotesTests

## God Nodes (most connected - your core abstractions)
1. `README.md (Architecture & Runbook)` - 30 edges
2. `Material` - 25 edges
3. `react` - 20 edges
4. `AGENTS.md (Agent Gotchas & Rules)` - 20 edges
5. `useStudy()` - 19 edges
6. `request()` - 18 edges
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

## Communities (43 total, 16 thin omitted)

### Community 0 - "schemas.py"
Cohesion: 0.05
Nodes (96): Base, get_db(), health(), lifespan(), list_models(), get, ChatMessage, Flashcard (+88 more)

### Community 1 - "progress/page.tsx"
Cohesion: 0.16
Nodes (10): ACTIVITY_ICONS, ActivityRow(), formatDate(), ProgressDashboard(), Card(), CardDescription(), CardHeader(), CardTitle() (+2 more)

### Community 2 - "README.md (Architecture & Runbook)"
Cohesion: 0.07
Nodes (58): AGENTS.md (Agent Gotchas & Rules), Typed API Helpers (src/lib/api.ts), Frontend API Proxy (next.config.ts rewrites), shadcn base-nova Style (Base UI, not Radix), Env Config Read-Once Gotcha (pydantic-settings), React set-state-in-effect eslint Rule, Gemini Client Singleton Reuse, Graphify Knowledge Graph (+50 more)

### Community 3 - "api.ts"
Cohesion: 0.11
Nodes (26): Notes(), handleGenerate(), ModelSelect(), PROVIDER_BADGE, providerBadge(), ChatReply, CreateQuizPayload, generateStudyNotes() (+18 more)

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
Cohesion: 0.27
Nodes (7): QuickFlashcardTests, contextlib, fastapi_testclient, pathlib, sqlalchemy_pool, sys, unittest

### Community 8 - "package.json"
Cohesion: 0.05
Nodes (41): dependencies, @base-ui/react, class-variance-authority, cn, lucide-react, next, next-themes, react (+33 more)

### Community 9 - "services/audio.py"
Cohesion: 0.08
Nodes (35): create_audio_summary(), post, Session, generate_summary_text(), generate_tts_audio(), _pcm_to_wav_base64(), Convert raw PCM base64 (L16) to WAV base64 so <audio> can play it., Generate audio via Gemini TTS. Returns (mime_type, base64_data, generated_by). (+27 more)

### Community 10 - "youtube.py"
Cohesion: 0.10
Nodes (26): create_youtube_material(), post, Session, fetch_transcript(), _flatten(), _pick_transcript(), Exception, Choose the best available transcript for a video. Raises the library's… (+18 more)

### Community 11 - "openai_compat.py"
Cohesion: 0.10
Nodes (42): _cfg(), generate_chat_reply(), generate_flashcards(), generate_quiz(), generate_study_notes(), list_models(), _model(), Provider/models advertised to the UI (must have a matching provider key). (+34 more)

### Community 12 - "TranscriptRetrievalTests"
Cohesion: 0.16
Nodes (5): FakeSnippet, FakeTranscript, FakeTranscriptList, TranscriptRetrievalTests, _list()

### Community 15 - "object"
Cohesion: 0.13
Nodes (6): FailureFallbackTests, FakeResponse, ok_completion(), ProviderRoutingTests, MetadataTests, object

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
Cohesion: 0.27
Nodes (8): Flashcards(), handleGenerate(), QuizResults(), handleCreateFlashcards(), FlashcardOut, generateFlashcards(), getFlashcards(), reviewFlashcard()

### Community 22 - "quiz/page.tsx"
Cohesion: 0.13
Nodes (9): ref_base_ui_react_merge_props, ref_base_ui_react_progress, ref_base_ui_react_use_render, class-variance-authority, QuizScreen(), Badge(), badgeVariants, Progress() (+1 more)

### Community 23 - "setup/page.tsx"
Cohesion: 0.15
Nodes (13): ref_base_ui_react_separator, ref_base_ui_react_switch, cn, ref_next_navigation, difficulties, questionCounts, QuizSetup(), handleStart() (+5 more)

### Community 24 - "layout.tsx"
Cohesion: 0.10
Nodes (15): nextConfig, ref_base_ui_react_slider, next, ref_next_font_google, src_app_globals, geistMono, geistSans, metadata (+7 more)

### Community 25 - "add/page.tsx"
Cohesion: 0.29
Nodes (11): ref_base_ui_react_input, react, AddMaterial(), handleContinue(), isYoutubeUrl(), Input(), Textarea(), createMaterial() (+3 more)

### Community 26 - "button.tsx"
Cohesion: 0.23
Nodes (8): ref_base_ui_react_button, lucide-react, ref_next_link, next-themes, sonner, ThemeToggle(), Button(), buttonVariants

### Community 36 - "chat/page.tsx"
Cohesion: 0.29
Nodes (9): Chat(), handleClear(), handleKeyDown(), handleSend(), SUGGESTIONS, ChatMessage, clearChat(), getChatMessages() (+1 more)

### Community 38 - "preview/page.tsx"
Cohesion: 0.43
Nodes (6): Preview(), Props, CardContent(), AudioSummaryOut, generateAudioSummary(), useStudy()

### Community 39 - "Settings"
Cohesion: 0.67
Nodes (3): Settings, EnvConfigTests, BaseSettings

### Community 41 - "AudioPlayer"
Cohesion: 0.83
Nodes (4): AudioPlayer(), toggle(), toggleBrowser(), toggleGemini()

## Knowledge Gaps
- **106 isolated node(s):** `$schema`, `style`, `rsc`, `tsx`, `config` (+101 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 291 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Material` connect `schemas.py` to `services/audio.py`, `youtube.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `UrlValidationTests` connect `UrlValidationTests` to `test_youtube_ingestion.py`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `react` connect `add/page.tsx` to `progress/page.tsx`, `api.ts`, `chat/page.tsx`, `preview/page.tsx`, `package.json`, `select.tsx`, `flashcards/page.tsx`, `quiz/page.tsx`, `setup/page.tsx`, `layout.tsx`, `button.tsx`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `Material` (e.g. with `get_analytics()` and `create_audio_summary()`) actually correct?**
  _`Material` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `style`, `rsc` to the rest of the system?**
  _106 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `schemas.py` be split into smaller, more focused modules?**
  _Cohesion score 0.054858429858429855 - nodes in this community are weakly interconnected._
- **Should `README.md (Architecture & Runbook)` be split into smaller, more focused modules?**
  _Cohesion score 0.06957047791893527 - nodes in this community are weakly interconnected._