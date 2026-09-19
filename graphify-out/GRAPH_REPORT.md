# Graph Report - spidey_tutor  (2026-09-19)

## Corpus Check
- 69 files · ~25,152 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 3, .example 1, .ico 1)

## Summary
- 645 nodes · 1405 edges · 42 communities (26 shown, 16 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 102 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f1d35389`
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
- ai.py
- package.json
- services/audio.py
- gemini.py
- openai_compat.py
- dependencies
- select.tsx
- QuickChatReplyTests
- object
- generate_quiz
- generate_chat_reply
- QuickQuizTests
- eslint.config.mjs
- flashcards/page.tsx
- radio-group.tsx
- preview/page.tsx
- setup/page.tsx
- context.tsx
- add/page.tsx
- separator.tsx
- slider.tsx
- postcss.config.mjs
- File SVG Icon
- Globe SVG Icon
- Next.js Logo
- Vercel Logo
- Window Icon (SVG)
- chat/page.tsx
- groq.py
- openrouter.py
- progress.tsx
- ModelRegistrationTests
- AudioPlayer

## God Nodes (most connected - your core abstractions)
1. `README.md (Architecture & Runbook)` - 30 edges
2. `Material` - 22 edges
3. `react` - 20 edges
4. `AGENTS.md (Agent Gotchas & Rules)` - 20 edges
5. `useStudy()` - 19 edges
6. `request()` - 17 edges
7. `lucide-react` - 16 edges
8. `compilerOptions` - 16 edges
9. `generate_chat_reply()` - 15 edges
10. `Button()` - 15 edges

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

## Communities (42 total, 16 thin omitted)

### Community 0 - "schemas.py"
Cohesion: 0.05
Nodes (101): Base, get_db(), health(), lifespan(), list_models(), get, ChatMessage, Flashcard (+93 more)

### Community 1 - "progress/page.tsx"
Cohesion: 0.14
Nodes (13): ACTIVITY_ICONS, ActivityRow(), formatDate(), ProgressDashboard(), Props, Card(), CardContent(), CardDescription() (+5 more)

### Community 2 - "README.md (Architecture & Runbook)"
Cohesion: 0.07
Nodes (58): AGENTS.md (Agent Gotchas & Rules), Typed API Helpers (src/lib/api.ts), Frontend API Proxy (next.config.ts rewrites), shadcn base-nova Style (Base UI, not Radix), Env Config Read-Once Gotcha (pydantic-settings), React set-state-in-effect eslint Rule, Gemini Client Singleton Reuse, Graphify Knowledge Graph (+50 more)

### Community 3 - "api.ts"
Cohesion: 0.13
Nodes (20): Notes(), handleGenerate(), ModelSelect(), PROVIDER_BADGE, providerBadge(), ChatMessage, ChatReply, CreateQuizPayload (+12 more)

### Community 4 - "quick.py"
Cohesion: 0.13
Nodes (26): _band(), _cloze(), _contains_term(), generate_chat_reply(), _keywords(), generate_flashcards(), generate_quiz(), generate_study_notes() (+18 more)

### Community 5 - "components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 6 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 7 - "ai.py"
Cohesion: 0.17
Nodes (9): Settings, EnvConfigTests, QuickFlashcardTests, QuickStudyNotesTests, BaseSettings, pathlib, pydantic_settings, sys (+1 more)

### Community 8 - "package.json"
Cohesion: 0.05
Nodes (41): nextConfig, devDependencies, eslint, eslint-config-next, tailwindcss, @tailwindcss/postcss, @types/node, @types/react (+33 more)

### Community 9 - "services/audio.py"
Cohesion: 0.22
Nodes (13): _pcm_to_wav_base64(), Convert raw PCM base64 (L16) to WAV base64 so <audio> can play it., available_models(), _chat_json(), generate_flashcards(), generate_quiz(), generate_study_notes(), Query Ollama for available models. (+5 more)

### Community 10 - "gemini.py"
Cohesion: 0.21
Nodes (12): _client(), generate_chat_reply_raw(), generate_flashcards_raw(), generate_quiz_raw(), generate_study_notes_raw(), Call Gemini and return a grounded answer to the last user message. ``history``…, Call Gemini and return raw quiz dicts (no normalization)., Call Gemini and return raw flashcard dicts (no normalization). (+4 more)

### Community 11 - "openai_compat.py"
Cohesion: 0.14
Nodes (24): _badge_error(), chat_completion(), chat_json(), chat_text(), CompatConfig, _error_message(), _extract_json(), generate_chat_reply() (+16 more)

### Community 12 - "dependencies"
Cohesion: 0.17
Nodes (12): dependencies, @base-ui/react, class-variance-authority, cn, lucide-react, next, next-themes, react (+4 more)

### Community 15 - "object"
Cohesion: 0.18
Nodes (5): FailureFallbackTests, FakeResponse, ok_completion(), ProviderRoutingTests, object

### Community 16 - "generate_quiz"
Cohesion: 0.14
Nodes (13): _error_detail(), generate_flashcards(), generate_quiz(), generate_study_notes(), _normalize_flashcard(), _normalize_question(), _normalize_study_notes(), A safe, user-facing reason a provider/generation failed. (+5 more)

### Community 17 - "generate_chat_reply"
Cohesion: 0.24
Nodes (7): generate_chat_reply(), Generate a chat reply grounded in the material. Returns (generated_by,…, _chat_text(), generate_chat_reply(), Free-form chat completion (no forced JSON format)., Answer the last user message, grounded in the study material., ChatDispatchTests

### Community 19 - "eslint.config.mjs"
Cohesion: 0.40
Nodes (4): eslintConfig, ref_eslint_config, ref_eslint_config_next_core_web_vitals, ref_eslint_config_next_typescript

### Community 20 - "flashcards/page.tsx"
Cohesion: 0.16
Nodes (13): ref_base_ui_react_button, lucide-react, ref_next_link, Flashcards(), handleGenerate(), QuizResults(), handleCreateFlashcards(), Button() (+5 more)

### Community 22 - "preview/page.tsx"
Cohesion: 0.18
Nodes (11): ref_base_ui_react_merge_props, ref_base_ui_react_use_render, class-variance-authority, sonner, Preview(), QuizScreen(), Badge(), badgeVariants (+3 more)

### Community 23 - "setup/page.tsx"
Cohesion: 0.18
Nodes (12): ref_base_ui_react_switch, cn, ref_next_navigation, difficulties, questionCounts, QuizSetup(), handleStart(), timerOptions (+4 more)

### Community 24 - "context.tsx"
Cohesion: 0.24
Nodes (11): Material, Quiz, QuizResult, loadModel(), ModelOption, QuizConfig, saveModel(), StudyContext (+3 more)

### Community 25 - "add/page.tsx"
Cohesion: 0.33
Nodes (8): ref_base_ui_react_input, react, AddMaterial(), handleContinue(), Input(), Textarea(), createMaterial(), uploadPdf()

### Community 36 - "chat/page.tsx"
Cohesion: 0.33
Nodes (9): Chat(), handleClear(), handleKeyDown(), handleSend(), SUGGESTIONS, clearChat(), getChatMessages(), request() (+1 more)

### Community 37 - "groq.py"
Cohesion: 0.42
Nodes (9): _cfg(), generate_chat_reply(), generate_flashcards(), generate_quiz(), generate_study_notes(), list_models(), _model(), Provider/models advertised to the UI (must have a matching provider key). (+1 more)

### Community 38 - "openrouter.py"
Cohesion: 0.42
Nodes (9): _cfg(), generate_chat_reply(), generate_flashcards(), generate_quiz(), generate_study_notes(), list_models(), _model(), Provider/models advertised to the UI (must have a matching provider key).… (+1 more)

### Community 41 - "AudioPlayer"
Cohesion: 0.83
Nodes (4): AudioPlayer(), toggle(), toggleBrowser(), toggleGemini()

## Knowledge Gaps
- **106 isolated node(s):** `$schema`, `style`, `rsc`, `tsx`, `config` (+101 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 248 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `react` connect `add/page.tsx` to `progress/page.tsx`, `api.ts`, `chat/page.tsx`, `package.json`, `select.tsx`, `flashcards/page.tsx`, `preview/page.tsx`, `setup/page.tsx`, `context.tsx`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `cn` connect `setup/page.tsx` to `progress/page.tsx`, `progress.tsx`, `package.json`, `select.tsx`, `flashcards/page.tsx`, `radio-group.tsx`, `preview/page.tsx`, `add/page.tsx`, `separator.tsx`, `slider.tsx`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `Material` (e.g. with `get_analytics()` and `create_audio_summary()`) actually correct?**
  _`Material` has 12 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `style`, `rsc` to the rest of the system?**
  _106 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `schemas.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05110602593440122 - nodes in this community are weakly interconnected._
- **Should `progress/page.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._
- **Should `README.md (Architecture & Runbook)` be split into smaller, more focused modules?**
  _Cohesion score 0.06957047791893527 - nodes in this community are weakly interconnected._