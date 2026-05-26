# CLAUDE.md

This is `kaleidoscope` — a local-first, markdown-driven pre-decision review tool for engineering leaders working through messy technical, organizational, and strategic calls. *Pressure-tests judgment in gray areas before a decision is socialized; never forces binary answers; never pretends to automate leadership judgment.*

## Think before coding

- Read the existing decision-artifact templates before proposing changes to output shape — Kaleidoscope's value is the *artifact* (a reusable decision doc), not the chat thread
- State the goal in one sentence before writing
- If the goal is unclear, ask. Editorial drift on a leadership-decision tool is high-stakes

## Simplicity first

- Local-first by design — markdown in, markdown out, no cloud
- Prefer boring solutions to clever ones
- One concern per change
- No new dependencies without justification
- The "rotate through multiple lenses" pattern is deliberate; don't add gamification, ranking, or scoring

## Surgical changes

- Don't refactor surrounding code without being asked
- Match existing patterns:
  - Decision artifacts are markdown files; one decision per file
  - Lenses are pluggable but each one is its own file/section
  - No binary answers — output is structured-uncertainty, not "do X"
- Voice: declarative, never coaching ("you should...") or therapy ("how does that make you feel...")

## Goal-driven execution

- Each commit advances a specific lens, fixes a template, or improves the artifact format
- Frequent commits over large ones

## What this repo is for

Engineering leaders working through hard calls. Pre-decision rehearsal that produces a durable, reusable decision artifact in markdown. Not a chat thread; not an automated answer.

## What this repo is NOT for

- Real-time decision support during meetings — Kaleidoscope is for slow thinking, not live tactics
- Team-shared decision artifacts (initially) — local-first means *your* decisions, not org wiki
- Replacement for actual leadership judgment — the artifact assists; the call is the leader's

## How to ship a change

1. Branch from `main` as `<your-id>/<short-feature>`
2. Test the lens or template change manually with a real decision (eat the dogfood)
3. PR to `main`
4. Wait for human approval before merge
