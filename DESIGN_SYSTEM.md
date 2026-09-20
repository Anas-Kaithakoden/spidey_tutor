# Spidey Tutor Design System

**Status:** Approved visual direction for foundation work
**Date:** 2026-09-20
**Scope:** Visual foundation, app shell, reusable patterns, and future screen redesigns

## Product Character

Spidey Tutor is a polished study workspace with a friendly, original spider/web personality. The target balance is:

- 70% modern, focused product
- 20% playful learning energy
- 10% spider/web personality

The interface should feel warm, intelligent, youthful, and credible for college students. Personality comes from interaction, illustration, meaningful color, copy, and restrained web geometry rather than decoration piled onto every surface.

## Non-Goals

- No Marvel or Spider-Man imitation
- No giant spider webs covering the interface
- No superhero red/blue palette
- No childish cartoon overload
- No generic AI SaaS dashboard language
- No gradient-everywhere treatment
- No decorative blobs, confetti, or animation without a product purpose
- No provider, model, mock, or generated-by terminology in primary student-facing copy

## Visual Foundation

### Theme

Dark-first, with deep blue-black surfaces rather than pure black:

- Canvas: deep blue-black
- Elevated surface: blue-black with a small lift in lightness
- Raised surface: slightly brighter blue-black
- Light mode: warm paper/off-white canvas with softly tinted surfaces

### Brand palette

- Teal/cyan: brand, primary actions, active progress, links, focus
- Gold: highlights, achievement, important moments, selected emphasis
- Green: mastered/success
- Amber: learning/in progress
- Coral: needs attention/destructive
- Violet: restrained AI-related emphasis only

Color must communicate state and hierarchy. It should not be used as decoration without meaning.

### Typography

Keep Geist. Establish a clear scale:

- Display: 48-64px for home/product statements
- Page title: 32-40px
- Section title: 20-24px
- Body: 15-17px
- Supporting text: 13-14px
- Generated study content: comfortable line-height and readable measure

Do not let every route collapse into the same small title and muted subtitle pattern.

### Surfaces and shape

- Use cards for meaningful framed objects, not every section.
- Prefer clear surface hierarchy over excessive borders.
- Use moderate radii consistently; avoid giant pills except for compact status or segmented controls.
- Use restrained elevation: soft shadow, thin ring, or tinted surface, not all three everywhere.
- Avoid nested cards unless each frame has a distinct semantic purpose.

## Spider/Web Language

Use a subtle, original web language in:

- hero backgrounds
- empty/loading/success illustrations
- progress connections
- section separators
- connected study-mode nodes
- focused hover or loading states

Web geometry should generally remain low opacity and secondary to content. A small original spider companion may appear in contextual empty, loading, success, and error states with varied expressions.

The mascot must be original and must not resemble copyrighted Spider-Man/Marvel artwork.

## Motion

Motion should clarify state and reward progress:

- page entrance: small opacity and vertical reveal
- cards: restrained hover lift where interactive
- upload: drop-zone response when dragging
- generation: staged progress language and web-strand motion
- quiz: subtle answer selection feedback
- flashcards: real 3D flip
- results: score reveal and restrained celebration for strong performance
- navigation: clear active/open transitions

All motion must respect `prefers-reduced-motion`. Reduced motion should preserve state changes without decorative movement.

## Shared Interaction Rules

- Primary actions are visually distinct from selection states.
- Selected navigation and tabs use a consistent selected treatment.
- Icon-only controls have accessible names and tooltips where unfamiliar.
- Compact interactive controls target at least 44px where practical.
- Loading states explain what is happening and disable duplicate submission.
- Critical errors persist inline with a clear retry/recovery action.
- Empty states explain the next useful action.
- Advanced model/language controls use progressive disclosure and do not dominate student workflows.

## Student-Facing Vocabulary

Prefer:

- `Start a new study session`
- `Study Assistant`
- `Reference Sheet`
- `Generated`
- `Ready`
- `Needs attention`
- `Try again`

Avoid as primary copy:

- provider
- model name
- mock
- generated_by
- quick mode

Technical detail may remain available in secondary diagnostics when necessary for transparency.

## Study Mode Identity

Study modes should share the same foundation while receiving restrained visual cues:

- Quiz: teal/cyan, progress and challenge
- Flashcards: gold, recall and reveal
- Notes: warm paper/document treatment
- AI Tutor: restrained violet accent
- Exam: focused amber/coral timing cues
- Podcast: audio/cyan rhythm
- Progress: semantic green/amber/coral performance cues

These identities must not become unrelated themes or require separate component systems.

## Responsive Rules

Design and validate at 320px, 375px, 390px, 768px, and desktop widths.

- No horizontal overflow
- Primary actions remain reachable
- Long titles and generated content wrap safely
- Malayalam text remains readable
- Audio and chat controls remain usable with mobile browser chrome and keyboard
- Navigation has a dedicated mobile pattern

## Implementation Boundaries

- Preserve all existing API routes, request payloads, response contracts, backend behavior, database logic, and feature functionality.
- Keep API calls in `src/lib/api.ts`.
- Use existing Next.js, Tailwind, Base UI/shadcn-style architecture.
- Build shared primitives before spreading page-level patterns.
- Implement the P0 reliability/accessibility gate before broad feature-page redesign.
- Redesign the core flow as one connected product before secondary features.

## Review Checklist

Before accepting a visual change, verify:

1. It makes the student's task clearer.
2. It preserves material context.
3. It reduces cognitive load.
4. It fits the shared system.
5. It is keyboard and screen-reader usable.
6. It works at mobile widths.
7. It preserves API/backend contracts.
8. Its behavior has been tested.
9. Its personality comes from purposeful product language, motion, color, or illustration rather than decoration alone.
