# Spidey Tutor — Design Critique

> **Role**: Senior Product Designer + UX Critic
> **Date**: September 2026
> **Methodology**: Live inspection of all screens as a first-time student user, combined with code-level analysis of state handling, flow logic, and information architecture.

---

## Executive Summary

Spidey Tutor has a **functionally complete** product but is presenting itself as a developer scaffold rather than a student-facing application. The core loop works: upload material > generate content > study. But the product hides this loop behind a flat, undifferentiated interface where every screen looks and feels roughly the same. There is no sense of momentum, no celebration of progress, and no design language that communicates this is built for you, the student.

The single most critical problem is **navigation architecture**: 9 nav items in a flat bar with no hierarchy means students have no mental model of the app. They cannot tell which features depend on others, what the intended flow is, or where they currently are in a session.

The color scheme (pure dark background with oklch(0.145 0 0) and an achromatic primary) is completely **desaturated**. There is zero color identity. The app could belong to any domain. For a student product built around energy and recall, this is a significant missed opportunity.

---

## Global / Cross-Cutting Issues

### Navigation Bar

**What students see**: A horizontal strip with 9 ghost-style text links: Study | Notes | Flashcards | Exam | Podcast | Chat | Progress | Plan | Formulas.

**Problems**:
1. **No active state indicator.** There is no visual cue for the current page. The user cannot orient themselves.
2. **No hierarchy or grouping.** All 9 items have identical visual weight. Students are forced to mentally parse all 9 links every time they need to navigate.
3. **9 items is too many.** Top-level navigation should have at most 5-7 items before it collapses into a menu.
4. **Ambiguous labels.** "Study" navigates to /add (uploading material). This is not what the word "Study" implies.
5. **No mobile nav.** At narrower viewports the navbar overflows with no hamburger menu or bottom tab bar.
6. **"Study" is the entry point but not emphasized.** The primary CTA of the entire product is a ghost button identical to every other nav item.
7. **No context of current material.** Once a student has uploaded material, there is no persistent reminder of what they're studying.

**Ideal**: A simplified top nav with 4-5 items max, a clear active state, and a persistent "studying: [Material Title]" badge or chip.

---

### Visual Identity & Color System

**Problems**:
1. The entire app uses **zero chromatic color**. Both light and dark themes use achromatic greyscale as the primary color.
2. There is **no brand color**, no accent that communicates energy, intelligence, or academic motivation. Compare to Anki (blue), Duolingo (green), Khan Academy (green/purple).
3. Feature cards on the homepage have no visual differentiation.
4. Dark mode background is so dark (oklch(0.145)) that it feels oppressive rather than focused.

---

### Typography

**Problems**:
1. h1 on every page is text-2xl font-bold — 24px. This is too small for a primary heading.
2. Subtitle text is muted grey. On a dark background this achieves very low contrast ratios.
3. Every page has the exact same title structure. A quiz page and a study plan page look structurally identical.

---

### Loading States

**Problems**:
1. **No skeleton screens.** When content is loading, the user sees an empty page.
2. The "Redirecting..." state feels like a crash, not a helpful redirect.
3. The spinner floats in the center of a large empty page with excessive padding.

---

### Empty States

**What is missing**:
1. **No illustration or warmth.** An empty state is a prime moment to build connection with the student.
2. **No explanation of what happens next.**
3. **The Model Select dropdown appears inside empty states.** Students don't know what a "model" is at the point where they just want flashcards to generate.

---

### Error States

**Problems**:
1. **Transient toasts for critical errors.** If AI generation fails, a toast appears and disappears. The student is left with an empty page and no persistent indication of what went wrong.
2. **"mock" mode is invisible.** When the backend falls back to mock data, students may dismiss the toast quickly and think the content is real.
3. **No retry affordances** after errors.

---

## Screen-by-Screen Analysis

---

### Screen 1: Home Page (/)

#### What the student is trying to accomplish
A new student lands here. They need to understand: What is this? Is it for me? How do I start?

#### What currently gets in the way
1. **The logo is a Bug icon.** A Bug lucide icon creates an unfortunate association (software bugs) and breaks the "Spidey" metaphor. There is no spider anywhere on the page.
2. **The headline ("Spidey Tutor") tells them nothing.** It's a product name, not a value proposition.
3. **Feature cards are dead ends.** "Upload Material", "Take a Quiz", "Study Flashcards" — none of these are clickable.
4. **Single CTA "Start Studying" goes to /add**, but "studying" implies active recall, not setup/upload.
5. **Massive vertical whitespace** at py-24 creates an empty, unfinished feel.
6. **The feature cards only describe 3 features** but the app has 9+ features. This is a significant discoverability gap.
7. **Returning students get the same homepage as new students.** No shortcuts to resume studying.

#### What information should be visually dominant
1. The core value proposition: "Upload your notes. Get quizzes, flashcards, and study tools — instantly."
2. The primary action: upload or paste study material.

#### What should be reduced or removed
- The large py-24 gap between hero and feature cards.
- The Bug icon (replace with a spider or more relevant symbol).
- The static, non-clickable feature cards.

#### What should be grouped together
- The hero headline + CTA + illustrative graphic of the workflow (upload > generate > study).

#### What actions should be primary
- **Upload / Start a new session**

#### What actions should be secondary
- "Continue studying [last material]" (for returning students)

#### What the ideal layout should communicate
"This is where studying gets smarter. Drop your notes here, and in seconds you'll have personalized quizzes, flashcards, and an AI tutor waiting for you."

---

### Screen 2: Add Study Material (/add)

#### What the student is trying to accomplish
Get their study material into the system as quickly as possible.

#### What currently gets in the way
1. **The tab switcher is unnecessarily wide.** 5 equal-width tabs feel like buttons for 5 separate apps.
2. **"Office" is a confusing label.** Students think "slides" or "presentation", not "Office."
3. **"Continue" button is bottom-right aligned** and may be off-screen until the student scrolls.
4. **No drag-and-drop.** The most natural file interaction pattern for desktop users is missing.
5. **No file size limit is shown** until presumably it fails.
6. **Title field is optional but positioned first.** Students don't understand why it exists.
7. **No example of what happens next** after clicking "Continue."

#### What information should be visually dominant
1. The primary input method (text or file drop zone) — this should occupy 70%+ of the page.
2. The "Continue" button — always visible even when disabled, with tooltip explaining why.

#### What should be reduced or removed
- The 5-equal-tab switcher (condense into a compact pill toggle or small dropdown).
- "Office" label — rename to "Slides & Docs" or "Word / PPT / Excel".

#### What should be grouped together
- Input method selector + input area as one logical unit.
- File name/size metadata + remove button once a file is selected.

#### What actions should be primary
- **Continue** (sticky, always visible)

#### What actions should be secondary
- Switching input type (tab switcher).

#### What the ideal layout should communicate
"I just need your notes. Pick any format — paste, file, video — and I'll handle the rest in seconds."

---

### Screen 3: Material Preview (/preview)

#### What the student is trying to accomplish
Confirm the material was parsed correctly, then move into a study mode fast.

#### What currently gets in the way
1. **The preview is a wall of raw text** in a small scrollable box (max-h-80). A student with a 50-page PDF cannot meaningfully review this.
2. **Too many actions competing at once.** The bottom row has 6 separate controls: Chat, Study Notes, language toggle, speed slider, Audio Summary button, Continue.
3. **Language toggle and speed slider appear before audio is generated.**
4. **"Continue" navigates only to /quiz/setup.** The student may want Flashcards instead. This is a false funnel.
5. **The audio summary feature is buried** among other controls.

#### What information should be visually dominant
1. Material title + source type + word count (confirmation it was parsed).
2. "Choose your study mode" — a clear decision point for what to do next.

#### What should be reduced or removed
- The raw text preview box (replace with a parsed summary).
- The pre-audio language/speed controls (move inside the audio player UI).
- The Chat and Notes buttons from the bottom action row.

#### What should be grouped together
- All "What do you want to do?" actions as equally-weighted cards: Quiz, Flashcards, Study Notes, Chat, Exam, Podcast.
- The audio summary as its own card or module.

#### What actions should be primary
- **Select a study mode** (Quiz / Flashcards / Notes / Chat / Exam).

#### What actions should be secondary
- Generate audio summary.
- Open the raw material.

#### What the ideal layout should communicate
"Your material is ready. Now, how do you want to study? Pick your mode and let's go."

---

### Screen 4: Quiz Setup (/quiz/setup)

#### What the student is trying to accomplish
Configure and quickly start a quiz on their material.

#### What currently gets in the way
1. **"AI Model" selector is the first thing on the page.** This is a power-user setting that most students should never need to change.
2. **No context of which material will be quizzed.** The page shows no material title.
3. **Question count options have no guidance** on which to choose.
4. **Timer is off by default with no explanation** of why timers help.
5. **The "Start Quiz" button can take 10-30 seconds** with no progress indicator. Students will wonder if it crashed.
6. **No difficulty recommendation.** "Medium" is pre-selected but there's no guidance.

#### What information should be visually dominant
1. The material being quizzed (currently invisible).
2. Difficulty selection — this is the most impactful choice.

#### What should be reduced or removed
- AI Model selector — move to a global Settings page or collapsible "Advanced" section.

#### What should be grouped together
- Difficulty + question count (both about quiz intensity).
- Timer toggle + time options (already grouped well).

#### What actions should be primary
- **Start Quiz**

#### What actions should be secondary
- AI model selection.
- Timer.

#### What the ideal layout should communicate
"Choose how hard you want to push yourself. We'll generate [N] questions on [Material Title] right now."

---

### Screen 5: Quiz (/quiz)

#### What the student is trying to accomplish
Answer quiz questions quickly and accurately to test their knowledge.

#### What currently gets in the way
1. **Progress bar doesn't show answered questions.** A student can advance without answering — the bar looks complete even if they skipped everything.
2. **The question dots at the bottom are too small** (size-3, ~3px circles). Nearly invisible and not finger-tappable on mobile.
3. **No ability to "flag" a question for review.**
4. **"Finish Quiz" only appears on the last question.** Students who are done but not on the last page can't submit.
5. **The timer turns red when under 60 seconds** but there's no visual pulse for students focused on reading.
6. **No "Submit" confirmation.** Clicking "Finish Quiz" immediately submits.
7. **Difficulty badge in the header** is setup information not useful during the quiz.

#### What information should be visually dominant
1. The question text (h2 — this is correct).
2. The answer options (currently good, large touch targets with border highlight).
3. The timer (should be more prominent when under 2 minutes).

#### What should be reduced or removed
- Difficulty badge from the header.
- Redundant "Question N" label inside the card (the badge already shows N/Total).

#### What should be grouped together
- Question counter + timer (top row — already done, this works).
- All navigation at the bottom (already done, this works).

#### What actions should be primary
- **Selecting an answer** (largest touch area on the page — correct).
- **Next / Finish Quiz** (bottom right — correct).

#### What actions should be secondary
- **Previous** (correctly styled as outline variant).
- Question dots navigation.

#### What the ideal layout should communicate
"You're making progress. Each answer brings you closer to understanding this material."

---

### Screen 6: Quiz Results (/quiz/results)

#### What the student is trying to accomplish
See how they performed, understand where they went wrong, and decide what to do next.

#### What currently gets in the way
1. **The score circle is too small** — 112px. This is the most emotionally significant moment in the quiz flow.
2. **No message or contextual feedback.** Whether the student scores 20% or 100%, they see the same layout.
3. **Review section immediately follows the score** with no visual separation.
4. **The wrong answer the student chose isn't clearly distinguished.** Students need to see: "You chose C. The right answer was B."
5. **Explanation text is text-xs text-muted-foreground** — the smallest, lightest text on the page. Explanations are the most valuable learning content.
6. **"Retry Quiz" and "Create Flashcards" have equal visual weight.** For a student who scored poorly, Retry is more important.
7. **No obvious path back to studying** after reviewing results.

#### What information should be visually dominant
1. The score — large, visually distinct, with contextual message.
2. Incorrect answers (the learning opportunities).
3. Explanation text for each wrong answer — promoted from text-xs to readable size.

#### What should be reduced or removed
- Explanation text should be promoted from text-xs to normal readable size.

#### What should be grouped together
- Score + context message + correct/incorrect counts (one "debrief" section).
- All answer reviews in a scrollable section below.
- All next-step actions at the bottom.

#### What actions should be primary
- **Retry Quiz** (if score < 70%) or **Continue to Flashcards** (if score >= 70%).

#### What actions should be secondary
- Go home / upload new material.

#### What the ideal layout should communicate
"Here's where you stand. Here's exactly what you missed and why. Here's what to do about it."

---

### Screen 7: Flashcards (/flashcards)

#### What the student is trying to accomplish
Actively recall information by flipping through concept cards until the material feels memorized.

#### What currently gets in the way
1. **No flip animation.** The card "flips" by toggling text — there's no CSS 3D transform animation despite perspective being set on the parent. This is a major UX gap. The central mechanic of flashcards relies on the satisfying flip reveal.
2. **Card height is fixed at min-h-[250px].** For cards with long back text, the text overflows or gets cramped.
3. **"Front" / "Back" labels in small muted caps** are the only indicator of which side you're on. No visual differentiation between front and back.
4. **Navigation dots are 2.5px circles (size-2.5) for potentially 20+ cards.** Unreadable and untappable on mobile.
5. **No self-assessment mechanism.** No "Got it / Still learning" rating system.
6. **Empty state shows the Model Select dropdown.** Students don't know what a "model" is at this point.
7. **No swipe gesture support on mobile.**

#### What information should be visually dominant
1. The card content (front or back) — currently appropriately large.
2. The flip affordance — needs animation reinforcement.

#### What should be reduced or removed
- Model Select from the empty state (global preference instead).
- Navigation dot cluster — replace with "X of Y" counter + swipe gestures.
- "Quick Mode — no AI call" badge (implementation detail, not student-facing).

#### What should be grouped together
- Card navigation (prev/next buttons + current position counter) — single row.
- Post-review actions in a clear action area.

#### What actions should be primary
- **Flip the card** (tapping anywhere on the card surface).
- **Rate yourself** ("Got it / Still learning" — currently missing).

#### What actions should be secondary
- Previous / Next navigation.
- Generate new flashcards.

#### What the ideal layout should communicate
"One concept at a time. Tap to reveal. Move through at your own pace. The app remembers what you're learning."

---

### Screen 8: Chat (/chat)

#### What the student is trying to accomplish
Ask the AI specific questions about their material — clarifying concepts, requesting examples, or drilling into a topic.

#### What currently gets in the way
1. **The material context card is small and low-contrast.** Students may not be sure the AI knows what they're talking about.
2. **Model Select, Language Toggle, and Clear button compete in the top-right corner.** Three different control categories in one area.
3. **"Clear" is a destructive action with no confirmation dialog.** An accidental tap deletes all messages.
4. **Suggestion chips disappear once any message is sent.** They should remain accessible via a "Suggestions" button.
5. **The assistant bubble has a MessageCircle icon inside the bubble text itself.** Creates awkward text flow and visual noise.
6. **No streaming.** The assistant shows "Thinking..." and then the entire response appears at once.
7. **"Ask Your Material"** as the page title is awkward phrasing.

#### What information should be visually dominant
1. The chat thread (messages) — correctly takes up most of the viewport.
2. The material being discussed — needs more visual presence.

#### What should be reduced or removed
- Model Select — move to a settings panel or collapsible drawer.
- The MessageCircle icon inside assistant bubbles.
- The keyboard shortcut tip — integrate as textarea placeholder text.

#### What should be grouped together
- Language toggle + model preference in a single settings gear/popover.

#### What actions should be primary
- **Send a message.**
- **Suggestion chips** (when empty — correctly shown).

#### What actions should be secondary
- Clear chat.
- Change language.
- Change model.

#### What the ideal layout should communicate
"Your AI tutor knows exactly what you're studying. Ask it anything — it won't make things up."

---

### Screen 9: Study Notes (/notes)

#### What the student is trying to accomplish
Get a structured, organized set of notes from their material — a replacement for manually taking notes.

#### What currently gets in the way
1. **Section content is muted grey text on a dark card.** No visual hierarchy between headings, body text, and bullet points.
2. **Each section is in its own Card**, creating a vertical wall of bordered cards with no sense of document structure.
3. **Key Concepts is the last thing on the page.** For students reviewing, this might be the most valuable section — buried at the bottom.
4. **Regenerate Notes** silently replaces current notes without confirmation.
5. **Language toggle appears twice** — once in the empty state and once at the bottom of generated notes.
6. **No export or copy functionality.** Students can't paste notes into their own documents.
7. **"Quick Mode" badge** leaks developer terminology to students.

#### What information should be visually dominant
1. The notes title and summary (the document header).
2. The section headings — they should feel like real document headings, not card titles.

#### What should be reduced or removed
- Each section in its own Card — replace with a single scrollable document.
- "Quick Mode" and "generated_by" badges — hide from students.
- Duplicate language toggle.

#### What should be grouped together
- Section title + content + bullet points as flowing document sections.
- Key Concepts moved to the top as a "cheat sheet."

#### What actions should be primary
- **Generate Notes** (empty state — correct).
- **Copy / Export** (currently missing).

#### What actions should be secondary
- Regenerate with different settings.
- Language toggle.

#### What the ideal layout should communicate
"Your material, reorganized. Clear sections, key terms highlighted, bullet points where they help. Like a study guide written just for this topic."

---

### Screen 10: Exam Setup (/exam/setup) and Exam (/exam)

#### What the student is trying to accomplish
Simulate a real exam experience with timed, mixed-question-type conditions and AI grading.

#### What currently gets in the way
1. **Exam setup page requires scrolling** — the "Start Exam" button is below the fold.
2. **The browser window.confirm() dialog** is used for the unanswered-questions confirmation. Native browser alert — no styling, blocked on some mobile browsers.
3. **Two progress bars** (question progress + time remaining) have tiny, low-contrast labels. During exam conditions, students need to read these at a glance.
4. **No word count** for essay/paragraph responses.
5. **Auto-submit toast** appears and dismisses. No persistent "Time's up" indicator on the results page.

#### What information should be visually dominant
1. **Time remaining** — during exam conditions this is critical.
2. **Question text** — correctly the largest text in the card.
3. **Answered/unanswered count** — students need this before submitting.

#### What should be reduced or removed
- window.confirm() — replace with a custom in-app confirmation modal.

#### What should be grouped together
- Question navigation dots + answered count in one "question map" panel.

#### What actions should be primary
- **Answering the question.**
- **Next / Submit Exam.**

#### What the ideal layout should communicate
"You're in exam mode. Focus. The timer is running. Answer every question before time's up."

---

### Screen 11: Progress Dashboard (/progress)

#### What the student is trying to accomplish
Understand how they're actually doing — what topics are strong, what needs more work — and get motivation to continue.

#### What currently gets in the way
1. **8 stat cards in a 4-column grid** creates a data dump with no story.
2. **"Best Score" appears twice** — once as a sub-label in "Average Score" and again as its own card.
3. **"Materials Studied" and "Study Sessions"** give no actionable information.
4. **The score trend chart has no axes, no labels, no baseline.**
5. **"Needs practice" badge in red** feels punishing without a follow-up action immediately visible.
6. **The "Practice" button** for weak topics blends with the table row instead of being prominent.
7. **No motivational layer.** Great learning apps include streaks, goals, and encouragement.

#### What information should be visually dominant
1. Overall accuracy — correctly large at text-4xl.
2. Weakest topics ("Needs Practice" items) — the main call-to-action area.
3. Score trend over time.

#### What should be reduced or removed
- 2 redundant stat cards (fold Best Score into Average Score).
- "Materials Studied" and "Study Sessions" as top-level stats.

#### What should be grouped together
- Accuracy + breakdown (correct/incorrect) as one summary.
- Topics sorted by "Needs Practice" first.

#### What actions should be primary
- **Practice [weakest topic]** — contextual call-to-action per topic row.

#### What the ideal layout should communicate
"Here's your honest report card. These topics need work. Here's how to fix it, right now."

---

### Screen 12: Study Plan (/study-plan)

#### What the student is trying to accomplish
Get a structured, day-by-day study schedule leading up to their exam date.

#### What currently gets in the way
1. **AI Model selector is the first field.** A power user setting that most students should never need.
2. **Syllabus PDF + Syllabus textarea relationship isn't clear** to students before they interact.
3. **The date picker is a browser native input type="date"** — renders differently per browser/OS.
4. **Daily hours is a range slider** without tick marks. Students can't easily set an exact value.
5. **The generated plan renders as individual day cards** — 14 cards for 2 weeks, 30 for a month. No calendar view or weekly grouping.
6. **"Generate Plan" button is not sticky** — students must scroll to the bottom.

#### What information should be visually dominant
1. The exam date (the most critical constraint).
2. The plan itself — organized by week, not individual day cards.

#### What should be reduced or removed
- AI Model selector — global preference.

#### What should be grouped together
- Exam date + days remaining counter.

#### What actions should be primary
- **Generate Plan.**
- **Save / export plan** (currently missing).

#### What the ideal layout should communicate
"Tell me your deadline. I'll build your study schedule. Day by day, topic by topic, until you're ready."

---

### Screen 13: Podcast (/podcast)

#### What the student is trying to accomplish
Generate a conversational, audio-based study session — an AI-generated podcast that teaches the material.

#### What currently gets in the way
1. **The Podcast page can be accessed without any study material active.** Students land on an empty state with no context.
2. **The empty state doesn't explain what a Spidey Podcast sounds like.** Students don't know if this is robotic text-to-speech or a conversational dialogue.
3. **The feature is labeled simply "Podcast" in the navbar** — students don't intuitively know this is an AI-generated audio study tool.

#### What the ideal layout should communicate
"Listen to your study material as an engaging AI conversation. Pick a topic and press play."

---

### Screen 14: Formula Sheet (/formula-sheet)

#### What the student is trying to accomplish
Extract and organize all mathematical or conceptual formulas from their material into a quick-reference sheet.

#### What currently gets in the way
1. **"Formulas"** as a nav label is discipline-specific. Students studying history or business won't think this applies to them. Rename to "Reference Sheet" or "Key Terms & Formulas."
2. **Students don't know if this feature is useful for their material** before clicking.
3. **The feature is accessible without any material active**, leading to a confusing empty state.

---

## Summary: Priority Issue Matrix

| Priority | Issue | Impact |
|---|---|---|
| Critical | No active nav state / session context | Orientation, flow |
| Critical | No color identity / zero chromatic design | Brand, engagement |
| Critical | 9-item flat nav with no hierarchy | Navigation, discoverability |
| Critical | Flashcard has no flip animation | Core mechanic broken |
| Critical | Preview page sends users only to Quiz, not all modes | Information architecture |
| High | AI Model selector exposed as a primary field everywhere | Cognitive load |
| High | No streaming in Chat | Perceived performance |
| High | "Mock mode" is invisible to the student | Trust, transparency |
| High | Explanation text in quiz results is text-xs | Learning value buried |
| High | window.confirm() in exam submission | Polish, mobile breakage |
| High | No persistent "currently studying: X" context | Orientation |
| Medium | Notes shown as individual cards, not a document | Readability |
| Medium | Study Plan shows individual day-cards for a month | Scannability |
| Medium | Progress page has no motivational layer | Engagement |
| Medium | No drag-and-drop on file upload | Interaction quality |
| Medium | Empty states lack warmth / illustration | First impression |
| Medium | "Office" and "Plan" nav labels are unclear | Discoverability |
| Low | Navigation dots too small (size-2.5, size-3) | Mobile usability |
| Low | Word count / char count in text input is too quiet | Feedback |
| Low | Language toggle appears in two places on Notes page | Consistency |
| Low | "Quick Mode" badge leaks dev info to students | Polish |

---

## Guiding Design Principles for Redesign

1. **Student-first language.** Every label, button, and message should speak to a student, not a developer. "AI Model" becomes "Study Assistant". "Quick Mode" is hidden entirely.

2. **The flow is sacred.** Upload > Generate > Study is the core loop. Every screen should make this loop feel effortless and obvious. Friction anywhere in this loop kills retention.

3. **Context persistence.** The student should always know what material they're studying. This should appear in the navbar or as a persistent session chip that follows them across all pages.

4. **Progressive disclosure for power features.** AI model selection, language toggle, generation settings — these should be accessible but secondary. The default should always be "just make it work."

5. **Color as a teaching tool.** Use color to distinguish study modes, indicate progress (green for mastered, amber for in progress, red for needs work), and create emotional resonance (celebration on good scores).

6. **Motion and feedback.** The flashcard flip, the score reveal, loading transitions — these micro-animations are the emotional layer that makes the product feel alive. Without them, the UX is functional but forgettable.

7. **Mobile-first study.** Students study on phones. Every interactive element (cards, nav, dots, buttons) must be finger-sized and swipe-aware.
