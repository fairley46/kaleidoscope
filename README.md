# Kaleidoscope

[![CI](https://github.com/fairley46/kaleidoscope/actions/workflows/ci.yml/badge.svg)](https://github.com/fairley46/kaleidoscope/actions/workflows/ci.yml)

Local-first CLI that pressure-tests an ambiguous engineering decision through markdown lenses, then writes a reusable decision artifact.

![Kaleidoscope CLI demo](docs/demo.png)

## Pitch

You start with a messy thought. Kaleidoscope asks a short clarifying set, rotates the problem through Technical, Culture, Operational, Financial, and User lenses, and leaves lens reviews plus a master synthesis under `reports/`.

It is a private pre-decision companion for engineering leaders, not a general AI workspace and not a substitute for judgment.

## Why

Gray-area calls are hard to reason through alone. A single chat thread is disposable. Kaleidoscope turns the same rough prompt into inspectable markdown you can edit, keep local, and reuse before you socialize a decision.

V1 uses a heuristic analysis provider (stdlib only) behind an explicit provider boundary so a model-backed implementation can plug in later without rewriting the CLI or report pipeline.

## Quickstart

Requires Python 3.9+.

```bash
git clone https://github.com/fairley46/kaleidoscope.git
cd kaleidoscope
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run with a rough prompt (answers can be typed interactively, or piped):

```bash
kaleidoscope "We should centralize this platform capability, but I am worried about downstream effects."
```

Without installing the console script:

```bash
PYTHONPATH=src python3 -m kaleidoscope "This migration seems technically right but organizationally risky."
```

Each run writes one `*_Review.md` per lens and `reports/Kaleidoscope_Report.md`. Generated reports stay gitignored so working notes remain local.

## Architecture

```text
kaleidoscope/
  lenses/                 # editable markdown lens definitions
  templates/              # Lens_Template.md for custom lenses
  reports/                # local-only generated reviews (gitignored)
  src/kaleidoscope/
    cli.py                # argparse entry
    question_flow.py      # clarifying questions
    lens_loader.py        # markdown lens parser
    providers.py          # AnalysisProvider + heuristic implementation
    analyzer.py           # per-lens analysis
    synthesizer.py        # cross-lens synthesis
    report_writer.py      # markdown report output
  tests/                  # unittest smoke pin
```

Add a custom lens by copying `templates/Lens_Template.md` into `lenses/` and re-running. No code change required.

## Status

V1 prototype. Useful locally for private pre-decision reviews. Heuristic provider only. No UI, auth, collaboration, or live model calls yet.

## License

MIT. See [LICENSE](LICENSE).
