# Graph Report - spidey_tutor  (2026-09-18)

## Corpus Check
- Corpus is ~20,203 words - fits in a single context window. You may not need a graph.

## Summary
- 542 nodes · 1121 edges · 36 communities (19 shown, 17 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 97 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Backend API Core
- Frontend Dependencies
- Agent Collaboration Rules
- Feature Pages
- Quick Generation
- Component Registry Config
- TypeScript Configuration
- AI Provider Dispatcher
- Frontend Package Config
- Ollama Provider
- Gemini Provider
- App Layout & Theme
- UI Dependencies
- Select Component
- Chat Quick Tests
- Dev Dependencies
- Quiz Dispatch Tests
- Chat Dispatch Tests
- Quiz Quick Tests
- ESLint Config
- NPM Scripts
- Radio Group Component
- Backend Settings
- PDF Ingestion
- Notes Quick Tests
- Next Config
- Separator Component
- Slider Component
- PostCSS Config
- File SVG Icon
- Globe SVG Icon
- Next.js Logo
- Vercel Logo
- Window SVG Icon

## God Nodes (most connected - your core abstractions)
1. `README.md (Architecture & Runbook)` - 30 edges
2. `Material` - 20 edges
3. `AGENTS.md (Agent Gotchas & Rules)` - 20 edges
4. `react` - 19 edges
5. `useStudy()` - 19 edges
6. `request()` - 16 edges
7. `compilerOptions` - 16 edges
8. `lucide-react` - 15 edges
9. `cn` - 14 edges
10. `Button()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Env Config Read-Once Gotcha (pydantic-settings)` --semantically_similar_to--> `Env Config (backend/.env, config.py)`  [INFERRED] [semantically similar]
  AGENTS.md → README.md
- `Typed API Helpers (src/lib/api.ts)` --semantically_similar_to--> `Typed API Client (src/lib/api.ts)`  [INFERRED] [semantically similar]
  AGENTS.md → README.md
- `Verification Pipeline (lint, tsc, build, import)` --semantically_similar_to--> `Quality Checks (lint, tsc, build, import)`  [INFERRED] [semantically similar]
  AGENTS.md → README.md
- `Schema Change -> Regenerate spidey.db` --semantically_similar_to--> `Database Schema Regeneration Workflow`  [INFERRED] [semantically similar]
  AGENTS.md → README.md
- `Single-Source Pydantic Schema Contract (schemas.py)` --semantically_similar_to--> `Schema Contract (schemas.py <-> api.ts)`  [INFERRED] [semantically similar]
  AGENTS.md → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Pluggable AI Provider System** — readme_ai_dispatcher, readme_gemini_provider, readme_ollama_provider, readme_quick_mode, readme_seed_mock [INFERRED 0.85]
- **Spidey Tutor Study Features** — readme_quiz_flow, readme_flashcards, readme_study_notes, readme_grounded_chat, readme_analytics [INFERRED 0.85]
- **Frontend-Backend Request/Response Contract** — readme_fastapi_backend, readme_schemas_contract, readme_api_client, agents_api_proxy [INFERRED 0.85]

## Communities (36 total, 17 thin omitted)

### Community 0 - "Backend API Core"
Cohesion: 0.06
Nodes (91): Base, get_db(), health(), lifespan(), list_models(), get, ChatMessage, Flashcard (+83 more)

### Community 1 - "Frontend Dependencies"
Cohesion: 0.07
Nodes (49): ref_base_ui_react_button, ref_base_ui_react_input, ref_base_ui_react_merge_props, ref_base_ui_react_progress, ref_base_ui_react_switch, ref_base_ui_react_use_render, class-variance-authority, cn (+41 more)

### Community 2 - "Agent Collaboration Rules"
Cohesion: 0.07
Nodes (58): AGENTS.md (Agent Gotchas & Rules), Typed API Helpers (src/lib/api.ts), Frontend API Proxy (next.config.ts rewrites), shadcn base-nova Style (Base UI, not Radix), Env Config Read-Once Gotcha (pydantic-settings), React set-state-in-effect eslint Rule, Gemini Client Singleton Reuse, Graphify Knowledge Graph (+50 more)

### Community 3 - "Feature Pages"
Cohesion: 0.06
Nodes (46): AddMaterial(), handleContinue(), Chat(), handleClear(), handleKeyDown(), handleSend(), Flashcards(), handleGenerate() (+38 more)

### Community 4 - "Quick Generation"
Cohesion: 0.13
Nodes (26): _band(), _cloze(), _contains_term(), generate_chat_reply(), _keywords(), generate_flashcards(), generate_quiz(), generate_study_notes() (+18 more)

### Community 5 - "Component Registry Config"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 6 - "TypeScript Configuration"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 7 - "AI Provider Dispatcher"
Cohesion: 0.18
Nodes (10): generate_flashcards(), generate_study_notes(), _normalize_flashcard(), _normalize_study_notes(), Generate study notes. Returns (generated_by, notes dict)., Generate flashcards. Returns (generated_by, flashcards)., QuickFlashcardTests, pathlib (+2 more)

### Community 8 - "Frontend Package Config"
Cohesion: 0.12
Nodes (15): name, private, version, @base-ui/react, eslint, eslint-config-next, react-dom, shadcn (+7 more)

### Community 9 - "Ollama Provider"
Cohesion: 0.22
Nodes (13): available_models(), _chat_json(), _chat_text(), generate_chat_reply(), generate_flashcards(), generate_quiz(), generate_study_notes(), Free-form chat completion (no forced JSON format). (+5 more)

### Community 10 - "Gemini Provider"
Cohesion: 0.21
Nodes (12): _client(), generate_chat_reply_raw(), generate_flashcards_raw(), generate_quiz_raw(), generate_study_notes_raw(), Call Gemini and return a grounded answer to the last user message. ``history``…, Call Gemini and return raw quiz dicts (no normalization)., Call Gemini and return raw flashcard dicts (no normalization). (+4 more)

### Community 11 - "App Layout & Theme"
Cohesion: 0.19
Nodes (9): ref_next_font_google, next-themes, src_app_globals, geistMono, geistSans, metadata, Navbar(), ThemeProvider() (+1 more)

### Community 12 - "UI Dependencies"
Cohesion: 0.17
Nodes (12): dependencies, @base-ui/react, class-variance-authority, cn, lucide-react, next, next-themes, react (+4 more)

### Community 15 - "Dev Dependencies"
Cohesion: 0.22
Nodes (9): devDependencies, eslint, eslint-config-next, tailwindcss, @tailwindcss/postcss, @types/node, @types/react, @types/react-dom (+1 more)

### Community 16 - "Quiz Dispatch Tests"
Cohesion: 0.32
Nodes (4): generate_quiz(), _normalize_question(), Generate quiz questions. Returns (generated_by, questions)., QuickDispatchTests

### Community 17 - "Chat Dispatch Tests"
Cohesion: 0.43
Nodes (3): generate_chat_reply(), Generate a chat reply grounded in the material. ``history`` is the conversation…, ChatDispatchTests

### Community 19 - "ESLint Config"
Cohesion: 0.40
Nodes (4): eslintConfig, ref_eslint_config, ref_eslint_config_next_core_web_vitals, ref_eslint_config_next_typescript

### Community 20 - "NPM Scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, start

### Community 22 - "Backend Settings"
Cohesion: 0.50
Nodes (3): Settings, BaseSettings, pydantic_settings

## Knowledge Gaps
- **105 isolated node(s):** `$schema`, `style`, `rsc`, `tsx`, `config` (+100 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 220 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `react` connect `Frontend Dependencies` to `Frontend Package Config`, `App Layout & Theme`, `Select Component`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `cn` connect `Frontend Dependencies` to `Frontend Package Config`, `Select Component`, `Radio Group Component`, `Separator Component`, `Slider Component`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `lucide-react` connect `Frontend Dependencies` to `Frontend Package Config`, `App Layout & Theme`, `Select Component`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `Material` (e.g. with `get_analytics()` and `clear_chat()`) actually correct?**
  _`Material` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `style`, `rsc` to the rest of the system?**
  _105 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Backend API Core` be split into smaller, more focused modules?**
  _Cohesion score 0.05825242718446602 - nodes in this community are weakly interconnected._
- **Should `Frontend Dependencies` be split into smaller, more focused modules?**
  _Cohesion score 0.06729356450191008 - nodes in this community are weakly interconnected._