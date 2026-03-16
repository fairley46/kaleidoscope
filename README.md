# Kaleidoscope

Kaleidoscope is a local-first, markdown-driven diagnostic thinking tool for engineering leaders working through messy technical, organizational, and strategic decisions. It is designed to help a person think better in gray areas, not to force binary answers or pretend to automate judgment.

This V1 prototype is intentionally simple:

- It runs as a Python CLI.
- It starts from a rough problem statement.
- It asks a short set of clarifying questions before analyzing.
- It loads lens definitions from markdown files on disk.
- It generates one markdown review per lens plus a synthesized master report.
- It supports custom lenses by dropping a new markdown file into `lenses/`.

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

Kaleidoscope begins with a rough problem statement and then asks a short series of clarifying questions. The goal is to gather enough context to do useful analysis without turning the experience into a rigid survey.

The built-in question flow covers areas such as:

- what decision is actually being weighed
- who is affected
- what constraints matter
- what success looks like
- which options are already on the table
- which risks or assumptions already feel important

The flow stops once enough context is gathered or when the maximum question count is reached.

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

## Future Improvements

Useful next steps for future versions could include:

- model-backed analysis and synthesis providers
- richer adaptive questioning based on previous answers
- saved sessions and multiple report runs
- comparison mode across options or scenarios
- evidence attachments and richer context ingestion
- confidence tuning with explicit signal quality
- a lightweight TUI or desktop wrapper while preserving markdown outputs
