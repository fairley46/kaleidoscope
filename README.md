# Kaleidoscope

[![CI](https://github.com/fairley46/kaleidoscope/actions/workflows/ci.yml/badge.svg)](https://github.com/fairley46/kaleidoscope/actions/workflows/ci.yml)

Local-first CLI that reviews an ambiguous engineering decision with markdown lenses and writes the reviews to disk.

![Kaleidoscope CLI demo](docs/demo.png)

## Pitch

You start with a rough problem statement. Kaleidoscope asks a short set of clarifying questions, then reviews the problem with the Technical, Culture, Operational, Financial, and User lenses. It writes one review per lens and a master report under `reports/`.

It is a private pre-decision review for engineering leaders.

## Why

Kaleidoscope writes the rough problem statement to markdown on your machine. You can edit the files and reread them before you share the decision.

V1 analysis is `HeuristicAnalysisProvider` in `providers.py`. That class uses only the Python standard library. `cli.py` constructs it. A model-backed provider can implement `AnalysisProvider`.

## Quickstart

You need Python 3.9 or newer.

```bash
git clone https://github.com/fairley46/kaleidoscope.git
cd kaleidoscope
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run a rough prompt. Type the answers at the prompts, or pipe them on stdin:

```bash
kaleidoscope "We should centralize this platform capability, but I am worried about downstream effects."
```

Without installing the console script:

```bash
PYTHONPATH=src python3 -m kaleidoscope "This migration seems technically right but organizationally risky."
```

Each run writes one `*_Review.md` per lens and `reports/Kaleidoscope_Report.md`. Git ignores generated files in `reports/`.

## Architecture

```text
kaleidoscope/
  lenses/                 # editable markdown lens definitions
  templates/              # Lens_Template.md for custom lenses
  reports/                # generated reviews, gitignored
  src/kaleidoscope/
    cli.py                # argparse entry
    question_flow.py      # clarifying questions
    lens_loader.py        # markdown lens parser
    providers.py          # AnalysisProvider and HeuristicAnalysisProvider
    analyzer.py           # per-lens analysis
    synthesizer.py        # cross-lens synthesis
    report_writer.py      # markdown report output
  tests/                  # unittest smoke test
```

Copy `templates/Lens_Template.md` into `lenses/` and run Kaleidoscope again. The loader reads every `.md` file in that directory.

## Status

This is a V1 prototype. `HeuristicAnalysisProvider` does not call a model. There is no user interface, authentication, or collaboration.

## License

MIT. See [LICENSE](LICENSE).
