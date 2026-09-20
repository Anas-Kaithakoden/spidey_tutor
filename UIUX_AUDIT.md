# Spidey Tutor UI/UX Audit

**Scope:** Read-only frontend audit for the current Next.js application.
**Date:** 2026-09-20
**Audit rule:** Current source code is the authority. Existing design documents are treated as prior observations and are marked stale where the implementation has changed.

## Executive Summary

Spidey Tutor is a study workspace that turns uploaded or pasted material into quizzes, flashcards, notes, chat answers, exams, podcasts, study plans, formula sheets, and progress analytics.

The frontend has a working feature surface, but its experience is still assembled from page-level patterns rather than one coherent product system. The most important issues are:

1. Core study sessions are not consistently recoverable after refresh or direct URL entry.
2. Several important controls are not fully keyboard or screen-reader accessible.
3. Loading, empty, error, retry, and generation-fallback states are inconsistent.
4. The main material-to-study flow does not present all study modes with equal clarity.
5. Model/provider controls are exposed too prominently in student workflows.
6. Reusable primitives exist, but most pages still use duplicated markup and styling.
7. Responsive behavior needs systematic testing at narrow mobile widths and with long/generated content.
8. The visual direction should be finalized before individual feature pages are redesigned.

## Product Structure

### Core product loop

```text
Home
  -> Add material
  -> Preview material
  -> Configure quiz
  -> Take quiz
  -> Review results
  -> Continue with flashcards, notes, chat, or another study mode
```

### Core screens

- `/`
- `/add`
- `/preview`
- `/quiz/setup`
- `/quiz`
- `/quiz/results`

### Secondary screens

- `/flashcards`
- `/notes`
- `/chat`
- `/exam/setup`
- `/exam`
- `/exam/results`
- `/podcast/setup`
- `/podcast`
- `/progress`
- `/study-plan`
- `/formula-sheet`

## Route Audit

### `/`

**Purpose:** Product entry point.

**Main user goal:** Understand the product and begin studying.

**Current sections/components:** Brand mark, product title, description, Start Studying CTA, three static feature cards.

**Primary action:** Start Studying -> `/add`.

**Secondary actions:** None.

**Data/API dependencies:** None.

**Current UX problems:** Returning users have no resume action. The page describes only upload, quiz, and flashcards although the product has many more tools. Feature cards are not navigation targets.

**Current visual problems:** Hero hierarchy is generic and has large unused space. The product icon and visual identity need a deliberate approved direction.

**Important states:** First visit, returning user with material, dark mode, light mode, narrow mobile width.

**Recommendation:** Redesign from scratch after the shell and product direction are approved.

### `/add`

**Purpose:** Create material from text, PDF, image, Office file, or YouTube URL.

**Main user goal:** Add study material quickly.

**Current sections/components:** Source-type tab buttons, text title/input, file upload surfaces, YouTube URL/title inputs, word/character count, Continue button.

**Primary action:** Continue/process material.

**Secondary action:** Switch source type.

**Data/API dependencies:** `createMaterial`, `uploadPdf`, `uploadImage`, `uploadOffice`, `createYoutubeMaterial`, `useStudy`.

**Current UX problems:** Five source types have equal visual weight. There is no visible drag-and-drop behavior, file-size guidance, or clear explanation of the next step. The title field is not strongly explained.

**Current visual problems:** Repeated custom tab styling. File upload surfaces are large but pointer-oriented. Continue may be far below the input on mobile.

**Important states:** Empty input, invalid YouTube URL, selected file, upload in progress, upload failure, unsupported file, successful material creation.

**Recommendation:** Redesign from scratch as the first core workflow screen, while preserving all existing upload APIs.

### `/preview`

**Purpose:** Confirm parsed material and begin studying.

**Main user goal:** Verify the material and choose what to do next.

**Current sections/components:** Material metadata, raw text preview, Chat button, Notes button, language toggle, audio speed control, audio summary button, Continue -> quiz setup.

**Primary action:** Choose a study mode.

**Secondary actions:** Open source, chat, notes, generate audio summary, continue to quiz.

**Data/API dependencies:** `useStudy`, `generateAudioSummary`, `AudioPlayer`.

**Current UX problems:** The raw content box dominates. Actions compete with one another. Continue funnels primarily to quiz even though several other modes exist.

**Current visual problems:** Dense bottom action row. Audio settings appear before audio exists. No clear “what next?” hierarchy.

**Important states:** Material hydration, no material redirect, long text, audio loading, audio fallback, audio failure, English/Malayalam.

**Recommendation:** Redesign from scratch as the central study-mode decision screen.

### `/quiz/setup`

**Purpose:** Configure and generate a quiz.

**Main user goal:** Choose quiz difficulty and length, then start.

**Current sections/components:** ModelSelect, difficulty choices, question-count choices, timer switch and duration choices, generation button.

**Primary action:** Start Quiz.

**Secondary actions:** Change difficulty, count, timer, and model.

**Data/API dependencies:** `getMaterial`, `createQuiz`, `useStudy`, `ModelSelect`.

**Current UX problems:** Model selection is too prominent. The selected material is not clearly shown. Difficulty and count lack simple guidance. Long generation is represented mainly by a spinner.

**Current visual problems:** Repeated setup layout and custom selection buttons.

**Important states:** Missing material, material loaded by query parameter, model loading/failure, generation, fallback/mock result, API failure.

**Recommendation:** Light refactor first, then visual redesign after shared setup patterns are approved.

### `/quiz`

**Purpose:** Answer and submit a generated quiz.

**Main user goal:** Answer questions with minimal distraction.

**Current sections/components:** Question counter, difficulty badge, timer, progress bar, question card, answer buttons, Previous/Next, Finish Quiz, question dots.

**Primary action:** Select an answer and advance.

**Secondary actions:** Previous, question navigation, finish.

**Data/API dependencies:** Active quiz from `useStudy`, `submitQuiz`.

**Current UX problems:** Refresh/direct entry loses the active quiz because it is mainly in memory. Unanswered questions can be skipped. There is no flag/review workflow or explicit final confirmation.

**Current visual problems:** Small question dots. Timer emphasis is limited until the final minute. Difficulty is less important than answer progress.

**Important states:** Missing active quiz, timer disabled, timer running, timer nearly complete, unanswered questions, submit loading, submission failure.

**Recommendation:** Preserve the quiz interaction model but redesign the study surface after recovery and accessibility requirements are resolved.

### `/quiz/results`

**Purpose:** Explain quiz performance and offer next steps.

**Main user goal:** Understand mistakes and continue studying.

**Current sections/components:** Percentage score, correct/incorrect counts, answer review cards, Retry Quiz, Create Flashcards.

**Primary action:** Review mistakes and choose a next study action.

**Secondary actions:** Retry, create flashcards.

**Data/API dependencies:** `useStudy`, `generateFlashcards`.

**Current UX problems:** Refresh/direct entry can lose results. Score has no contextual message. Incorrect answers and explanations are not emphasized enough. Action priority does not adapt to score.

**Current visual problems:** Score treatment is too small for the emotional importance. Explanations use very small muted text.

**Important states:** No result, result loading/recovery, high score, low score, flashcard generation, generation failure.

**Recommendation:** Redesign from scratch after result-state and recovery behavior is defined.

### `/flashcards`

**Purpose:** Generate and review flashcards.

**Main user goal:** Practice active recall one concept at a time.

**Current sections/components:** Loading state, empty state, ModelSelect, flashcard surface, Previous/Next, dots, Take a Quiz.

**Primary action:** Reveal the answer.

**Secondary actions:** Navigate cards, generate cards, take a quiz.

**Data/API dependencies:** `getFlashcards`, `generateFlashcards`, `reviewFlashcard`, `useStudy`.

**Current UX problems:** Flip is text replacement without a real flip transition. There is no self-rating such as “Got it” or “Still learning.” Model selection is exposed in the empty state. Refresh depends on material context.

**Current visual problems:** Dots are too small for mobile. Long answers may make the card feel cramped.

**Important states:** No material, material loading, no cards, generation, card review, tracking failure, long front/back text.

**Recommendation:** Redesign from scratch as a focused active-recall experience.

### `/notes`

**Purpose:** Generate and read structured study notes.

**Main user goal:** Review a clear study guide derived from material.

**Current sections/components:** Loading state, empty state, ModelSelect, language toggle, generated summary card, section cards, key concepts, regenerate action.

**Primary action:** Generate or read notes.

**Secondary actions:** Change language/model, regenerate.

**Data/API dependencies:** `getStudyNotes`, `generateStudyNotes`, `useStudy`.

**Current UX problems:** Key concepts are buried. Regeneration replaces content without a strong confirmation or comparison. There is no copy/export action.

**Current visual problems:** Notes read as unrelated cards rather than one document. Repeated language controls and developer-oriented generation labels add noise.

**Important states:** No material, loading, empty, generating, generated, mock/quick fallback, generation failure, Malayalam content.

**Recommendation:** Redesign as a document-reading experience.

### `/chat`

**Purpose:** Ask questions grounded in uploaded material.

**Main user goal:** Clarify concepts with an AI tutor.

**Current sections/components:** Material context card, ModelSelect, language toggle, Clear, conversation log, suggestions, textarea, send button, thinking state.

**Primary action:** Ask a question.

**Secondary actions:** Suggestions, language/model changes, clear chat.

**Data/API dependencies:** `getChatMessages`, `sendChatMessage`, `clearChat`, `useStudy`.

**Current UX problems:** Clear has no confirmation. Suggestions disappear after the first message. Model controls compete with the conversation. Responses are not streamed.

**Current visual problems:** Material context is visually weak. Assistant icon placement creates noise inside message bubbles.

**Important states:** No material, conversation loading, empty conversation, optimistic message, thinking, error, clear confirmation, Malayalam.

**Recommendation:** Light structural refactor followed by focused redesign.

### `/exam/setup`

**Purpose:** Select material and configure a mixed-question timed exam.

**Main user goal:** Start a realistic practice exam.

**Current sections/components:** ModelSelect, material selector, title, difficulty, question count, duration, Start Exam.

**Primary action:** Start Exam.

**Secondary actions:** Select material and configure exam.

**Data/API dependencies:** `listMaterials`, `getMaterial`, `createExam`, `useStudy`.

**Current UX problems:** Setup is long and the primary action can be below the fold. Model selection is overemphasized.

**Current visual problems:** Repeats quiz setup layout without enough exam-specific hierarchy.

**Important states:** Materials loading, no materials, material loading, generation, failure, fallback.

**Recommendation:** Light refactor after shared setup components exist.

### `/exam`

**Purpose:** Run and submit a timed mixed-question exam.

**Main user goal:** Complete an exam under time pressure.

**Current sections/components:** Timer, progress, answered count, question card, MCQ/input/textarea controls, navigation, question dots, sessionStorage persistence.

**Primary action:** Answer questions.

**Secondary actions:** Navigate and submit.

**Data/API dependencies:** `getExam`, `submitExam`, `useStudy`, URL query, `sessionStorage`.

**Current UX problems:** Uses native `window.confirm` for incomplete submission. No essay word count. Timer and question map need stronger scanning hierarchy.

**Current visual problems:** Two progress indicators compete. Dots are too small and unlabeled.

**Important states:** Fresh exam, refresh recovery, missing exam, timer warning, auto-submit, incomplete submit, submit failure.

**Recommendation:** Redesign after quiz/exam interaction primitives are standardized.

### `/exam/results`

**Purpose:** Display grading, feedback, and recommendations.

**Main user goal:** Understand exam performance and what to improve.

**Current sections/components:** Score, grading badges, summary, strengths, weak areas, recommendations, question reviews, Retake, Progress.

**Primary action:** Review feedback and practice weak areas.

**Secondary actions:** Retake, view progress.

**Data/API dependencies:** `getExamResult`, `useStudy`, URL/sessionStorage result identity.

**Current UX problems:** Result recovery is inconsistent with quiz results. Time-expiry state is not strongly represented. Empty insight groups create variable layouts.

**Current visual problems:** Many cards compete for attention. Feedback hierarchy needs stronger prioritization.

**Important states:** Result loading, missing result, fetch failure, AI/hybrid/fallback grading, empty insight groups.

**Recommendation:** Light refactor followed by result redesign.

### `/podcast/setup`

**Purpose:** Configure and generate a study podcast.

**Main user goal:** Choose material, style, duration, and optional focus topic.

**Current sections/components:** ModelSelect, material selector, mode choices, duration choices, focus topic, title, Generate Podcast.

**Primary action:** Generate Podcast.

**Secondary actions:** Choose source, mode, duration, focus, title, model.

**Data/API dependencies:** `listMaterials`, `getMaterial`, `createPodcast`, `useStudy`.

**Current UX problems:** Model selection is too prominent. The distinction between script generation and audio availability is not clear before starting.

**Current visual problems:** Repeated setup layout and dense choice groups.

**Important states:** Materials loading, no materials, generation, mock/quick script, audio unavailable, audio failure.

**Recommendation:** Light refactor after shared generation/setup patterns exist.

### `/podcast`

**Purpose:** Browse, play, retry, and delete saved podcast episodes.

**Main user goal:** Listen to study material as audio.

**Current sections/components:** Episode list, active episode, PodcastPlayer, delete action, empty state.

**Primary action:** Play an episode.

**Secondary actions:** Retry audio, transcript, speed, delete, create new episode.

**Data/API dependencies:** `listPodcasts`, `getPodcast`, `deletePodcast`, `regeneratePodcastAudio`, `PodcastPlayer`, browser speech synthesis.

**Current UX problems:** Empty state lacks active material context and does not explain the experience clearly. Audio may be unavailable after script generation.

**Current visual problems:** Player has many controls and needs narrow-screen validation.

**Important states:** Loading, empty, episode selected, audio ready, audio unavailable, audio error, browser TTS, delete confirmation.

**Recommendation:** Redesign after media-player and empty-state patterns are approved.

### `/progress`

**Purpose:** Show study activity and performance analytics.

**Main user goal:** Understand strengths and decide what to practice next.

**Current sections/components:** Overall accuracy, stat cards, topic rows, score chart, recent activity, empty/error/loading states.

**Primary action:** Practice a weak topic.

**Secondary actions:** Browse analytics and recent activity.

**Data/API dependencies:** `getAnalytics`.

**Current UX problems:** Eight stats create a data dump. Best Score is redundant. Weak topics need more actionable priority. Motivation and goal framing are limited.

**Current visual problems:** Chart lacks axes/baseline. Cards compete with the main story.

**Important states:** Loading, API error/retry, no activity, populated data, empty topics, long titles.

**Recommendation:** Redesign from scratch as an actionable dashboard.

### `/study-plan`

**Purpose:** Generate a dated plan from a syllabus, material, or PDF.

**Main user goal:** Turn an exam deadline into a realistic schedule.

**Current sections/components:** ModelSelect, language toggle, PDF input, syllabus textarea, exam date, daily-hours slider, generated day cards, tips.

**Primary action:** Generate Plan.

**Secondary actions:** Upload PDF, paste syllabus, language/model settings.

**Data/API dependencies:** `generateStudyPlan`, `generateStudyPlanFromPdf`, `useStudy`.

**Current UX problems:** PDF versus pasted syllabus relationship needs clearer explanation. Slider lacks exact-value affordance. Long plans become many individual cards. No save/export.

**Current visual problems:** Dense inline controls and weak date/deadline hierarchy.

**Important states:** Empty sources, PDF selected, invalid/past date, loading, failure, generated plan, long plan, Malayalam.

**Recommendation:** Redesign from scratch as a deadline-first planning tool.

### `/formula-sheet`

**Purpose:** Generate and download a reference sheet.

**Main user goal:** Extract formulas, equations, or key definitions for quick revision.

**Current sections/components:** ModelSelect, language toggle, syllabus/material textarea, generate button, PDF download, grouped formula cards.

**Primary action:** Generate or download the reference sheet.

**Secondary actions:** Enter alternate syllabus, change language/model.

**Data/API dependencies:** `generateFormulaSheet`, `downloadFormulaSheetPdf`, `useStudy`.

**Current UX problems:** “Formula Sheet” may be unclear for non-mathematical material. No-material behavior is not strongly guided. PDF download is separate from generation and lacks persistent failure recovery.

**Current visual problems:** Dense inline styling and nested cards reduce scanability.

**Important states:** Empty source, loading, generated, PDF download loading, download failure, Malayalam, no formulas.

**Recommendation:** Redesign from scratch as a general “Reference Sheet” tool if product naming is approved.

## Shared Component Audit

### Existing shared components

- `Navbar`: global navigation and current-material context.
- `ModelSelect`: model list loading, fallback option, persisted model choice.
- `LanguageToggle`: English/Malayalam segmented control.
- `ThemeToggle`: light/dark switching.
- `AudioPlayer`: one-minute audio/browser TTS playback.
- `PodcastPlayer`: audio, browser TTS, transcript, speed, retry.
- `ThemeProvider`: next-themes integration.
- `Button`, `Card`, `Input`, `Textarea`, `Label`, `Badge`, `Progress`, `Switch`, `Select`, `Slider`, `Dialog`, `Tabs`, `Skeleton`, `EmptyState`, `PageHeader`, `SectionHeader`.

### Repetition and inconsistency

- Most routes hand-build page headings instead of using `PageHeader`.
- Most routes hand-build centered spinner states instead of `Skeleton` or a shared loading state.
- Empty states are repeated as dashed containers with different copy and spacing.
- Setup pages duplicate difficulty, count, duration, model, and generation layouts.
- `/add` uses custom tab buttons instead of the shared Tabs primitive.
- Native `<select>` and `<input type="range">` controls coexist with shared controls.
- Generation feedback is spread between buttons, toasts, badges, footnotes, and silent fallback behavior.
- Cards are used for both meaningful framed objects and ordinary document sections.

### Primitive requirements

- Button: consistent hierarchy, loading/disabled state, icon-only accessible names, minimum touch target.
- Card: reserve framing for real objects; avoid stacking cards inside cards.
- Input/Textarea: explicit labels, error/help text, long-content behavior.
- Select: one control style for model/material choices.
- Tabs: keyboard behavior, selected state, panel association, mobile overflow.
- Badge: student-facing status language; do not expose provider implementation details by default.
- Dialog: use for destructive/important confirmations instead of `window.confirm`.
- Progress: accessible label/value and useful semantics, not decorative bars only.
- Skeleton: use for known content shapes, not only generic spinners.
- EmptyState: explain next action and provide one clear CTA.
- PageHeader/SectionHeader: adopt consistently before page-by-page redesign.

## Global Visual Audit

### Typography

The app uses Geist through `next/font`. The intended hierarchy should be:

- Display: product/home statement.
- Page title: one dominant title per screen.
- Section title: clear grouping within a page.
- Body: readable generated content.
- Supporting text: restrained but not low-contrast.

Current pages frequently use the same small `text-2xl` heading pattern, making every route feel structurally identical. Typography should be finalized as tokens and then adopted through shared headers.

### Color

The current source includes chromatic teal/gold brand tokens in `globals.css`, but the token system is not fully reconciled: sidebar/chart families and several page-level color classes need a deliberate semantic mapping.

Required semantic categories:

- Brand/primary action
- Secondary action
- Surface/card
- Muted surface
- Focus ring
- Success/mastered
- Warning/in progress
- Destructive/needs attention
- Information
- Chart series

Do not use provider/mock/quick implementation states as prominent brand colors. Translate them into student-facing status such as “Generated,” “Ready,” or “Needs attention,” while retaining a transparent detail view where useful.

### Spacing and layout

Page widths vary between `max-w-lg`, `max-w-2xl`, `max-w-3xl`, and `max-w-4xl` without a documented content model. Setup screens use repeated large vertical gaps and equal-width option grids. Generated content needs readable measure and stable responsive constraints.

### Motion

Transitions exist mainly on buttons, selected states, progress indicators, and audio controls. Important missing motion opportunities include flashcard reveal, score/result reveal, loading transitions, and meaningful page-level state changes. Add motion only after reduced-motion behavior and information hierarchy are defined.

## Accessibility Audit

### P0

- File upload surfaces in `/add` are clickable `div` elements around hidden inputs. They need keyboard activation, accessible names, visible focus, and clear selected-file state.
- Flashcard flipping is attached to a non-semantic clickable `div` and needs keyboard access and a clear pressed/state relationship.
- Quiz, exam, and flashcard navigation dots have no accessible names and are too small for comfortable touch use.
- Active quiz/results routes need clear missing-session recovery instead of silent or confusing redirects.

### P1

- Theme toggle needs an accessible name and current-state communication.
- Range inputs and native selects need explicit labels.
- Segmented English/Malayalam controls need selected-state semantics.
- Generation, timer, error, and fallback updates need durable live-region treatment where appropriate.
- Replace `window.confirm` in exam submission with the shared dialog pattern.
- Shared Tabs needs stronger keyboard roving behavior and linked tab/panel semantics before broad adoption.

### Validation requirements

- Keyboard-only completion of every core flow.
- Screen-reader names for all icon-only controls.
- Visible focus at light and dark themes.
- Minimum 44px touch targets for compact navigation controls.
- Reduced-motion behavior for future transitions.
- Contrast checks for muted content, badges, chart labels, and focus rings.

## Responsive and Mobile Audit

Test at minimum:

- 320px
- 375px
- 390px
- 768px
- Desktop width

Pay special attention to:

- `/add` source tabs and file surfaces.
- `/preview` action cluster and audio controls.
- Quiz/exam answer choices and question navigation.
- Chat header controls and mobile keyboard behavior.
- Podcast player controls and transcript.
- Study plan and formula sheet action rows.
- Long material titles, generated answers, transcript lines, Malayalam text, and API error strings.
- Overflow caused by equal-width setup grids.

## State, Persistence, and API Assumptions

The redesign must preserve these contracts:

- All frontend API calls remain in `src/lib/api.ts`.
- Backend routes, request payloads, response payloads, database behavior, and provider routing remain unchanged.
- Material and model state are available through `useStudy()`.
- Material/model persistence uses `localStorage`.
- Active quiz, quiz result, active exam, and exam result are primarily context state.
- Exam in-progress recovery additionally uses URL parameters and `sessionStorage`.
- Backend persistence exists for materials, generated content, results, analytics, and podcast records.

Risks to resolve before visual redesign:

1. Material hydration and redirects can race on refresh/direct entry.
2. Quiz and quiz-result refresh behavior is weaker than exam recovery.
3. Query parameters can refer to a material different from the current context.
4. Empty/missing session states are inconsistent between routes.
5. Long-running generation exposes a spinner but not a durable progress or retry model.
6. Provider failure can produce fallback content; the UI must avoid presenting fallback content ambiguously.

## Cross-Screen State Matrix

| Screen | Required context | Refresh/direct entry | Main empty/error concern | Recommended handling |
|---|---|---|---|---|
| `/add` | None | Safe | Upload/API failure | Inline error and retry |
| `/preview` | Material | Material hydration | Missing material/audio failure | Hydration gate and clear redirect |
| `/quiz/setup` | Material or `material_id` | Can reload material | Missing material/generation failure | Resolve identity before render |
| `/quiz` | Active quiz | Currently fragile | Lost quiz | Durable quiz identity/recovery |
| `/quiz/results` | Quiz result | Currently fragile | Lost result | Durable result identity/recovery |
| `/flashcards` | Material | Depends on context | No cards/load failure | Material identity and empty CTA |
| `/notes` | Material | Depends on context | No notes/generation failure | Shared empty/error state |
| `/chat` | Material | Depends on context | Load/send/clear failure | Durable inline errors and confirmation |
| `/exam/setup` | Material list | Safe | No materials/list failure | Explicit empty state |
| `/exam` | Active exam/query/session | Has partial recovery | Lost/expired exam | Keep recovery and improve messaging |
| `/exam/results` | Exam result/query/session | Has recovery path | Result unavailable | Loading, retry, and missing-result state |
| `/podcast/setup` | Material list | Safe | No materials/generation failure | Explicit empty state |
| `/podcast` | Backend episodes | Safe | No episodes/audio unavailable | Explain script/audio states |
| `/progress` | Backend analytics | Safe | No activity/API failure | Actionable empty/error state |
| `/study-plan` | Material, text, or PDF | Local form state | Missing source/date/API failure | Clear source precedence |
| `/formula-sheet` | Material or text | Local form state | Missing source/PDF failure | Durable generation/download states |

## UI/UX Overhaul Priorities

### P0 — Must solve before feature-page redesign

1. **Core accessibility:** keyboard-operable uploads, flashcard flip, labeled question navigation, named icon controls, explicit selected states.
2. **Session recovery:** define behavior for refresh/direct URL/back-forward on quiz, quiz results, exam, and exam results.
3. **Material identity:** eliminate hydration races and make the active material reliable across routes.
4. **Durable errors:** replace toast-only critical failures with inline error and retry states.
5. **Fallback transparency:** clearly distinguish unavailable generation, deterministic local generation, and generated content without exposing developer jargon in primary copy.
6. **Responsive safety:** prevent overflow and preserve usable touch targets at 320px and 375px.
7. **Contract protection:** preserve all current API routes, payloads, response types, backend logic, and database behavior.

### P1 — Important product quality work

1. Adopt shared PageHeader, SectionHeader, EmptyState, Skeleton, Dialog, Tabs, and generation-state patterns across representative routes, then migrate the rest.
2. Establish a coherent material-to-study-mode flow from Preview.
3. Simplify navigation hierarchy and make the active material/current mode obvious.
4. Move model/provider controls into progressive disclosure or a global preference surface.
5. Standardize setup screens for quiz, exam, podcast, study plan, and formula sheet.
6. Replace native confirmation dialogs with the shared Dialog.
7. Improve result hierarchy so mistakes and next actions are more actionable.
8. Validate long content, Malayalam, charts, audio, and chat at mobile widths.

### P2 — Polish and discoverability

1. Finalize brand mark and visual identity direction.
2. Apply typography tokens consistently to every page.
3. Refine chart/sidebar semantic tokens and contrast.
4. Add purposeful transitions, including flashcard reveal and score reveal, with reduced-motion support.
5. Improve home-page return-user continuation and clickable feature discovery.
6. Add export/copy affordances where supported by existing data and product direction.
7. Replace repeated page-level Tailwind patterns with stable reusable primitives.

## Recommended Implementation Sequence

### Phase 0: Freeze and approve direction

- Approve the visual direction, navigation hierarchy, and student-facing vocabulary.
- Treat current shell/token experiments as provisional until reviewed.
- Do not redesign individual feature pages yet.

### Phase 1: Reliability and accessibility

- Fix route/session recovery behavior.
- Fix upload, flashcard, quiz/exam navigation, labels, focus, and confirmation semantics.
- Add durable loading/error/retry states.
- Validate at mobile widths.

### Phase 2: Shared foundation adoption

- Migrate page headers.
- Migrate empty/loading/error states.
- Standardize setup controls, model/language settings, buttons, cards, dialogs, tabs, and progress.
- Remove duplicated patterns only after behavior is preserved.

### Phase 3: Core flow redesign

- Redesign Home, Add Material, Preview, Quiz Setup, Quiz, Results, and Flashcards as one connected experience.
- Validate the full material-to-study loop before touching secondary tools.

### Phase 4: Secondary feature redesign

- Redesign Notes, Chat, Exam, Progress, Podcast, Study Plan, and Formula Sheet using the approved core system.

### Phase 5: Polish and verification

- Apply motion, responsive refinements, chart improvements, content export decisions, and visual polish.
- Run lint, typecheck, build, keyboard audit, mobile audit, and light/dark contrast checks.

## Acceptance Criteria

The overhaul is ready for the next stage only when:

- The core study loop works with no confusing redirects.
- Refresh and direct entry have defined behavior on every session route.
- All core interactions are keyboard accessible.
- Every loading state has a clear explanation and every critical error has a retry path.
- Material context is visible and correct across study routes.
- No API route, request shape, response shape, backend behavior, or database behavior has changed unintentionally.
- Shared primitives are actually adopted instead of merely defined.
- The app has no horizontal overflow at 320px, 375px, or 390px.
- Light and dark themes have readable contrast and consistent semantic colors.
- Feature-page redesigns are reviewed one group at a time rather than changed wholesale.

## Scope Boundary

This audit does not authorize feature-page redesigns by itself. The next implementation should begin only after this document and the visual direction are reviewed. Backend code, API routes, payloads, database logic, AI provider behavior, and existing feature functionality are intentionally outside the redesign scope.
