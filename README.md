# Kaleidoscope

Kaleidoscope is a local-first, markdown-driven pre-decision review tool for engineering leaders working through messy technical, organizational, and strategic calls. It is designed to help a person pressure-test judgment in gray areas before they socialize a decision, not to force binary answers or pretend to automate leadership judgment.

You can think of it as a private decision companion:

- start with a messy thought
- clarify what is actually being decided
- rotate the problem through multiple lenses
- surface blind spots, tensions, tradeoffs, and next-step ideas
- leave with a reusable decision artifact instead of a disposable chat thread

This V1 prototype is intentionally simple:

- It runs as a Python CLI.
- It starts from a rough problem statement.
- It asks a short set of clarifying questions before analyzing.
- It loads lens definitions from markdown files on disk.
- It generates one markdown review per lens plus a synthesized master report.
- It supports custom lenses by dropping a new markdown file into `lenses/`.

## Positioning

Kaleidoscope is not trying to be a general AI workspace, a knowledge base, or a planning tool.

Its wedge is narrower and more specific:

- a private pre-decision review flow for engineering leaders
- a way to pressure-test an ambiguous technical or organizational call before committing
- a way to turn fuzzy judgment into a reusable markdown artifact

That means Kaleidoscope is most valuable when the problem is sensitive, gray-area, and hard to reason through alone, such as:

- whether to centralize a platform capability
- whether to re-draw ownership boundaries
- whether to make a foundational engineering investment now or later
- whether a migration is strategically right but organizationally risky

## V1 Scope And Intent

The goal of V1 is usefulness, transparency, and editability.

Kaleidoscope is optimized for:

- local-first use in a coding environment
- inspectable markdown inputs and outputs
- structured but flexible guided questioning
- clear modular code that can be iterated on quickly
- an abstraction boundary where a real model-backed provider can be plugged in later

Kaleidoscope is not trying to solve:

- polished UI
- collaboration features
- authentication
- formal scoring
- enterprise-scale workflows
- generic brainstorming for everything
- project tracking or roadmap management

## Project Structure

```text
kaleidoscope/
  lenses/
    Culture_Lens.md
    Financial_Lens.md
    Operational_Lens.md
    Technical_Lens.md
    User_Lens.md
  reports/
  src/
    kaleidoscope/
      __init__.py
      __main__.py
      analyzer.py
      cli.py
      lens_loader.py
      models.py
      providers.py
      question_flow.py
      report_writer.py
      synthesizer.py
  templates/
    Lens_Template.md
  pyproject.toml
  README.md
```

## Install And Run

Kaleidoscope uses only the Python standard library.

```bash
cd /Users/bradfairley/Documents/Playground/kaleidoscope
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run it with a rough prompt:

```bash
kaleidoscope "We should centralize this platform capability, but I am worried about downstream effects."
```

You can also run it without installing the console script:

```bash
PYTHONPATH=src python3 -m kaleidoscope "This migration seems technically right but I am worried about downstream effects."
```

## Questioning Flow

Kaleidoscope begins with a rough problem statement and then asks a short series of clarifying questions. The goal is to gather enough context to do useful pre-decision analysis without turning the experience into a rigid survey.

The built-in question flow covers areas such as:

- what decision is actually being weighed
- who is affected
- what constraints matter
- what success looks like
- which options are already on the table
- which risks or assumptions already feel important

The flow stops once enough context is gathered or when the maximum question count is reached.

The intended feeling is closer to a thoughtful strategic check-in than a form fill.

## How Lens Files Work

Lens definitions are stored as markdown in `lenses/`. Each file is a source-of-truth artifact for a perspective Kaleidoscope should use during analysis.

The default lenses are:

- Technical
- Culture
- Operational
- Financial
- User

Each lens file includes sections for:

- Lens Name
- Purpose
- When to Use
- Key Questions
- What This Lens Looks For
- Common Risks / Failure Modes
- Signals or Evidence to Consider
- Output Expectations
- Recommendation Style

These files are meant to be readable and editable by a human. In V1, they are also used to make custom lens output more useful without requiring code changes.

## How Reports Are Generated

Each run creates:

- one report per lens, such as `reports/Technical_Review.md`
- a master synthesis report at `reports/Kaleidoscope_Report.md`

The `reports/` directory is intentionally local-only in this repo. Generated notes and diagnostic artifacts are ignored by git so a user can think in private without accidentally committing working notes.

That local-only default is part of the product stance: the working notes are for the decision-maker first. Kaleidoscope is meant to help someone get sharper before the meeting, memo, or org announcement, not turn every draft thought into a shared system artifact.

The lens-specific reports include:

- a short summary
- observations
- risks
- tradeoffs
- recommendations
- open questions
- signals or evidence to consider
- confidence / ambiguity notes

The master report includes:

- Problem Overview
- Executive Synthesis
- Lens Highlights
- Blind Spots
- Cross-Lens Tensions
- Tradeoffs
- Recommendations / Ideas
- Open Questions
- Confidence / Ambiguity Notes

The synthesis is built from the structured lens outputs rather than by simply concatenating the markdown files together.

## Adding Custom Lenses

To add a custom lens:

1. Copy `templates/Lens_Template.md`.
2. Fill in the sections with meaningful content.
3. Save the file into `lenses/` with a descriptive name such as `Security_Lens.md`.
4. Re-run Kaleidoscope.

No application code changes are required. Any new markdown file in `lenses/` is loaded automatically.

Custom lenses use the same report pipeline as the defaults. In V1, the default five lenses have specialized heuristics, while custom lenses are analyzed through a generic lens-aware heuristic that reads the markdown sections directly.

## V1 Assumptions And Simplifications

This version makes a few intentional simplifications:

- Analysis and synthesis use a heuristic provider, not a live LLM.
- The provider interface is explicit so a model-backed implementation can be added later without rewriting the CLI or report pipeline.
- Question asking is interactive but lightweight, with a fixed question bank and early stopping logic.
- Markdown parsing is intentionally simple and based on section headings rather than a heavier schema format.
- Reports are overwritten on each run in the configured `reports/` directory.

These tradeoffs keep the prototype understandable and local-first while still preserving the product intent.

## Why This Shape

Kaleidoscope is intentionally framed as a decision-support product, not a generic assistant.

The bet behind the product is that engineering leaders often need a private place to think through calls that are:

- strategically consequential
- politically sensitive
- technically ambiguous
- difficult to reason about from a single perspective

The value is not just "getting AI output." The value is producing a clearer decision artifact with explicit tradeoffs, blind spots, tensions, and follow-up questions.

## Future Improvements

Useful next steps for future versions could include:

- model-backed analysis and synthesis providers
- richer adaptive questioning based on previous answers
- saved sessions and multiple report runs
- comparison mode across options or scenarios
- evidence attachments and richer context ingestion
- confidence tuning with explicit signal quality
- a lightweight TUI or desktop wrapper while preserving markdown outputs
