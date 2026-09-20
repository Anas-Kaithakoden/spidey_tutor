# Spidey Tutor — UI/UX Master Plan

**Purpose:** Single source of direction for the Spidey Tutor UI/UX overhaul.

**Prepared from:**
- `UIUX_AUDIT(1).md` — latest code-level frontend audit; treat this as the authority for current implementation facts.
- `DESIGN_CRITIQUE(2).md` — detailed live first-user critique; treat recommendations as design guidance and older observations as stale where they conflict with the latest source audit.

---

## 1. Product Definition

Spidey Tutor is a study workspace that turns uploaded or pasted learning material into multiple study experiences:

- quizzes
- flashcards
- study notes
- material-grounded AI chat
- practice exams
- podcasts/audio
- study plans
- formula/reference sheets
- progress analytics

The central product loop is:

**Material → Choose how to study → Learn / Practice → Review → Continue**

The product should feel like **one coherent study workspace**, not a collection of separate AI utilities.

---

## 2. Source Reconciliation

### Current-source facts

The latest UI/UX audit explicitly states that current source code is the authority and that earlier design documents are stale where implementation has changed.

The latest audit identifies:
- session recovery problems
- accessibility gaps
- inconsistent loading/error/retry/fallback states
- unclear material-to-study-mode flow
- overexposed model/provider controls
- duplicated page-level UI patterns
- responsive risks
- the need to finalize visual direction before page-by-page redesign

See the audit executive summary and product structure.

### Important reconciliation with the design critique

The design critique says the visual system is entirely grayscale. The latest source audit says the current source already contains chromatic teal/gold brand tokens in `globals.css`, although the token system is not fully reconciled.

**Decision:** Do not throw away the existing color work and do not assume it is already solved. Instead, deliberately reconcile the existing teal/gold tokens into one semantic color system and have the design reviewer approve the result.

The design critique describes the product as "functionally complete." For QA purposes, this must NOT be treated as proof that every workflow is currently working end to end. Code presence and manual UX inspection are not substitutes for verification.

---

## 3. Non-Negotiable Product Principles

### 3.1 Student-first language

Primary UI language should describe the student's task, not implementation details.

Avoid making these primary concepts:
- provider
- model name
- mock
- generated_by
- quick mode

Advanced settings can exist behind progressive disclosure.

### 3.2 The material is the center of the product

A student should always know what material they are studying.

Active material identity should persist across relevant study routes.

### 3.3 The core flow is sacred

The primary experience must feel like:

**Add material → understand what was parsed → choose a study mode → generate/use it → review → choose the next useful action**

Preview must not force users into Quiz only.

### 3.4 Progressive disclosure

Default experience:
**"Just make it work."**

Power-user settings:
- study assistant/model
- language
- advanced generation preferences

These should not dominate the primary task.

### 3.5 Color has semantic meaning

Use the approved semantic system consistently:

- Brand / primary action
- Secondary action
- Surface
- Muted surface
- Focus
- Success / mastered
- Warning / in progress
- Destructive / needs attention
- Information
- Charts

Do not use provider/mock/quick implementation states as prominent brand colors.

### 3.6 Motion supports comprehension

Important motion opportunities:
- flashcard reveal
- score reveal
- meaningful generation/loading transitions
- state changes

All motion must have reduced-motion behavior.

### 3.7 Mobile-first

Design and validate for:
- 320px
- 375px
- 390px
- 768px
- desktop

No horizontal overflow at target widths.

Interactive controls should be comfortable touch targets.

---

## 4. Navigation / Information Architecture

Current flat navigation is too dense and lacks hierarchy.

### Target model

Use a compact hierarchy rather than a flat list.

Suggested conceptual groups:

**Home**
- Home

**Study**
- Materials
- Quiz
- Flashcards
- Notes
- AI Tutor
- Exams

**Tools**
- Podcast / Audio
- Study Plan
- Reference Sheet

**Progress**
- Progress

The exact final labels should be approved after visual review, but the structural principle is fixed:

- fewer top-level choices
- clear active state
- obvious current mode
- obvious current material
- dedicated mobile navigation

### Current-material context

A persistent context element should communicate something like:

`Currently studying · Operating Systems`

Do not show raw implementation metadata.

---

## 5. Global App Shell

The shell is the first shared implementation layer.

It must provide:
- consistent page container
- navigation hierarchy
- active navigation state
- current material context
- theme support
- mobile navigation
- accessible focus treatment
- consistent responsive behavior

Do not redesign 14 pages independently before the shell is stable.

---

## 6. Shared Component System

Existing primitives include:

- Button
- Card
- Input
- Textarea
- Label
- Badge
- Progress
- Switch
- Select
- Slider
- Dialog
- Tabs
- Skeleton
- EmptyState
- PageHeader
- SectionHeader
- ThemeProvider
- Navbar
- ModelSelect
- LanguageToggle
- ThemeToggle
- AudioPlayer
- PodcastPlayer

### Required adoption rule

A reusable component is not "done" merely because it exists.

Representative routes must actually adopt it before page redesign spreads.

### Required shared patterns

Create/standardize:
- PageHeader
- SectionHeader
- EmptyState
- Loading/Skeleton state
- Error + Retry state
- Generation state
- Dialog confirmation
- Material summary/context
- Setup-form sections
- Student-facing status badges

Avoid stacking cards inside cards unless each frame has a clear semantic purpose.

---

## 7. P0 Reliability + Accessibility Gate

This is now a mandatory gate before broad feature-page redesign.

### Session/recovery

Define and implement behavior for:
- refresh
- direct URL entry
- browser back
- browser forward
- missing material
- missing quiz
- missing quiz result
- missing exam
- missing exam result

Particular attention:
- active quiz
- quiz result
- active exam
- exam result
- material hydration

### Material identity

Eliminate hydration races.

Ensure query parameters cannot silently reference a different material from the current context.

### Durable errors

Critical failures must not depend solely on disappearing toasts.

Use:
- inline explanation
- clear recovery action
- retry where appropriate

### Accessibility

Fix:
- keyboard-operable upload surfaces
- semantic flashcard interaction
- accessible question navigation
- named icon-only controls
- visible focus
- selected-state semantics
- labeled ranges/selects
- proper tabs semantics
- dialog confirmation
- durable live-region treatment where appropriate

### Touch targets

Compact interactive controls should have adequate touch size. The audit specifies a minimum target of 44px.

---

## 8. P1 Shared UX Architecture

After the P0 gate:

### Standardize setup flows

Use a reusable setup pattern for:
- Quiz
- Exam
- Podcast
- Study Plan
- Reference Sheet

Common structure:

1. Material/source
2. Main task settings
3. Optional/advanced settings
4. Clear primary action
5. Generation state
6. Success / fallback / error

### Model control

Move model/provider selection into:
- global preferences
- advanced settings
- or an explicit study-assistant control

Do not make it the first field in every workflow.

---

## 9. Core Screen Redesign Order

### 1. Home

Goals:
- explain value immediately
- primary upload/start action
- useful returning-user continuation
- discoverable study capabilities

### 2. Add Material

Goals:
- make input method obvious
- support clear file interaction
- explain supported sources
- keep Continue/Process action clear
- show errors inline

### 3. Material Preview / Study Hub

This is a critical architectural screen.

Goals:
- show material identity and parsing status
- provide a clear "How do you want to study?" decision
- offer the supported study modes with clear hierarchy
- separate optional audio features from mode selection
- preserve access to raw material where useful

Possible study modes:
- Quiz
- Flashcards
- Notes
- AI Tutor
- Exam
- Podcast/Audio

### 4. Quiz Setup

Goals:
- show selected material
- make difficulty and length understandable
- treat timer as optional
- hide advanced model details unless requested
- provide meaningful generation feedback

### 5. Quiz

Goals:
- distraction-free answering
- strong question hierarchy
- clear answered/unanswered status
- accessible navigation
- strong timer handling
- safe submission confirmation

### 6. Quiz Results

Goals:
- prominent score
- explain mistakes
- readable explanations
- clear next-step actions
- make learning opportunities obvious
- provide continuity into another study mode

### 7. Flashcards

Goals:
- real flip/reveal interaction
- readable dynamic content
- clear position counter
- accessible navigation
- self-assessment where product support is added
- mobile-friendly interaction

### 8. Notes

Goals:
- document-like reading experience
- strong heading hierarchy
- key-concepts/summary visibility
- remove developer-facing labels
- clear regeneration behavior
- copy/export only where supported

### 9. AI Tutor

Goals:
- strong material context
- conversation first
- advanced settings secondary
- safe clear behavior
- useful suggestions
- understandable waiting/error states

---

## 10. Secondary Feature Redesign

After the core loop is validated:

### Exam
- strong exam-specific hierarchy
- prominent time and answered count
- accessible question map
- custom confirmation dialog
- robust timeout/recovery states

### Exam Results
- strong feedback hierarchy
- actionable weak-area review
- clear recovery behavior

### Progress
- reduce stat-card dumping
- emphasize actionable weak topics
- give the student a clear "what next?" path
- improve chart readability

### Study Plan
- deadline first
- clear source precedence
- explicit daily-hours control
- group long plans by week
- preserve readable structure

### Podcast / Audio
- explain the experience
- distinguish generated script vs available audio
- handle audio-unavailable states clearly
- keep player usable at narrow widths

### Reference Sheet
- use terminology that works beyond mathematics where appropriate
- clearly explain when the material does not contain useful formulas/definitions
- separate generation from download states

---

## 11. AI/Fallback Transparency

The backend can fall back to mock/deterministic output when provider generation fails.

The UI must not make this confusing.

Primary student-facing language should remain understandable.

Examples of acceptable user-facing concepts:
- Ready
- Generated
- Generation unavailable
- Needs attention
- Retry

A transparent detail surface may explain fallback behavior.

Do not expose implementation jargon as the primary UX.

---

## 12. Responsive QA Requirements

Every major screen must be tested at:

- 320px
- 375px
- 390px
- 768px
- desktop

Special attention:
- upload/source controls
- quiz/exam choices
- question navigation
- timers
- flashcards
- chat keyboard
- podcast player
- long titles
- generated long answers
- Malayalam text
- charts
- API errors
- setup grids

Acceptance criterion:
**No horizontal overflow at required widths.**

---

## 13. Visual System Direction

### Typography

Use a documented hierarchy:

- Display
- Page title
- Section title
- Body
- Supporting text

Do not let every screen collapse into the same 24px title + muted subtitle pattern.

Generated content must remain readable.

### Color

Current source already contains teal/gold chromatic tokens.

Decision:
- retain them as the candidate foundation
- reconcile them into semantic tokens
- validate contrast
- use color to communicate state and mode
- avoid decorative overuse

Do not change palettes repeatedly during development.

### Visual character

Target feeling:
- modern
- focused
- intelligent
- student-centered
- slightly playful/technical
- calm enough for long study sessions

Avoid:
- generic AI SaaS visual language
- excessive neon
- heavy gamification
- decorative spider/Marvel imitation
- visual noise

---

## 14. Content and Copy Rules

Prefer:

`Start a new study session`

over:

`Start Studying`

Prefer:

`Study Assistant`

over:

`AI Model`

Prefer:

`Reference Sheet`

or another approved student-facing term

over:

`Formula Sheet`

when the feature covers more than mathematics.

Avoid:
- "mock"
- "quick mode"
- provider names in primary workflow copy
- internal field names
- implementation details

---

## 15. Testing Architecture

A dedicated QA GPT is responsible for validation.

The QA GPT should distinguish:

- observed
- expected
- inferred
- unverified

Never report a fix as verified without retesting.

Every meaningful implementation pass should trigger focused regression tests.

### Core regression path

Home
→ Add Material
→ Preview
→ Choose Study Mode
→ Generate
→ Use Result
→ Review
→ Continue

### Important regression categories

- navigation
- material context
- session recovery
- quiz
- flashcards
- notes
- chat
- exam
- audio/podcast
- progress
- study plan
- reference sheet
- responsive
- accessibility
- light/dark themes
- AI/fallback behavior

---

## 16. Agent Responsibilities

### Main Chat

Product/UI lead.

Responsible for:
- direction
- prioritization
- architecture of the experience
- reviewing agent output
- resolving conflicts
- approving transitions between phases

### VS Code Agent

Implementation lead.

Responsible for:
- frontend code
- shared components
- styling
- responsive behavior
- accessibility implementation
- API integration

Rules:
- preserve API contracts
- preserve backend behavior
- avoid speculative rewrites
- do not redesign every page in one pass

### Antigravity

Design reviewer.

Responsible for:
- visual critique
- UX critique
- consistency
- interaction quality
- responsive visual inspection

Rules:
- review rather than arbitrarily modify product direction
- compare against the approved system

### QA GPT

Testing lead.

Responsible for:
- manual test guidance
- regression
- bug reproduction
- responsive testing
- accessibility testing
- verification of claimed fixes

Rules:
- evidence-driven
- no invented results
- no unverified "works"
- no redesign decisions

---

## 17. Implementation Gates

### Gate A — Direction

Approve:
- information architecture
- navigation hierarchy
- student-facing vocabulary
- visual system

### Gate B — Foundation

Complete:
- shell
- navigation
- material context
- semantic color/tokens
- shared primitives

### Gate C — Reliability/Accessibility

Complete:
- session recovery
- hydration behavior
- durable errors
- keyboard/focus
- semantic controls
- responsive safety

### Gate D — Core Flow

Complete and test:
- Home
- Add
- Preview
- Quiz Setup
- Quiz
- Results
- Flashcards

### Gate E — Secondary Features

Complete and test:
- Notes
- Chat
- Exam
- Progress
- Podcast
- Study Plan
- Reference Sheet

### Gate F — Final Polish

Complete:
- motion
- contrast
- responsive refinements
- content hierarchy
- visual consistency
- build/lint/typecheck
- full regression pass

---

## 18. Acceptance Criteria

The overhaul is ready to progress only when:

- Core study flow has no confusing redirects.
- Refresh/direct-entry behavior is defined on session routes.
- Current material is correct and visible across relevant screens.
- Critical errors have durable explanations and recovery.
- Core controls are keyboard accessible.
- Interactive controls have accessible names/states.
- No required mobile width has horizontal overflow.
- Shared primitives are genuinely adopted.
- API routes, request payloads, response contracts, database behavior, and backend logic have not been unintentionally changed.
- Light and dark themes are readable.
- Fallback behavior is not misleading.
- Feature pages are redesigned in connected groups rather than as unrelated screens.

---

## 19. Immediate Execution Order

At the current point in the project:

### RIGHT NOW

Finish only the already-authorized shared shell/foundation work if it is in progress.

Do NOT start redesigning all feature pages yet.

### NEXT

Run the P0 reliability/accessibility pass.

### THEN

Stabilize shared primitives and setup/generation patterns.

### THEN

Redesign the core material-to-study flow as one connected product:

**Home → Add → Preview → Quiz Setup → Quiz → Results → Flashcards**

### THEN

Redesign the secondary features.

### FINALLY

Run complete QA, responsive, accessibility, and visual-polish passes.

---

## 20. Decision Rule for Future Changes

Before accepting a proposed UI change, ask:

1. Does it make the student's main task clearer?
2. Does it preserve material context?
3. Does it reduce cognitive load rather than add controls?
4. Does it fit the shared design system?
5. Does it remain accessible?
6. Does it work on small screens?
7. Does it preserve current API/backend contracts?
8. Has it been tested?
9. Is the change supported by the product direction rather than personal taste?

If any answer is uncertain, pause and review before expanding the change.

---

## 21. Current North Star

Spidey Tutor should make a student feel:

> "I gave it my material. It understood what I'm studying. Now it helps me study it in whatever way works best."

The interface should make that experience obvious without exposing the machinery underneath it.
