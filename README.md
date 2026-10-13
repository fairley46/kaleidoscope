# Kaleidoscope

[![CI](https://github.com/fairley46/kaleidoscope/actions/workflows/ci.yml/badge.svg)](https://github.com/fairley46/kaleidoscope/actions/workflows/ci.yml)

Kaleidoscope helps you think about a problem from multiple angles. It gathers perspectives from the company, team, culture, strategy, and roadmap, alongside technical, operational, financial, and user views, and shows how those perspectives fit together.

It is not mainly a decision tool. People do better work when they have the reasoning, not just the conclusion.

![Kaleidoscope CLI demo](docs/demo.png)

## What it does

You start with a rough problem statement. Kaleidoscope asks a short set of clarifying questions, then explores the problem through markdown lenses. It writes one review per lens and a master report under `reports/`.

The master report shows:

- each perspective
- where perspectives reinforce each other
- tensions between them
- open questions

Optional next steps stay secondary. The point is the path through the problem, not a verdict.

## Why local files

Kaleidoscope writes markdown on your machine. You can edit the files, reread them, and share the reasoning when you are ready.

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

## Lenses

Default lenses:

- Company, Team, Culture, Strategy, Roadmap
- Technical, Operational, Financial, User

Copy `templates/Lens_Template.md` into `lenses/` and run Kaleidoscope again. The loader reads every `.md` file in that directory.

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
  tests/                  # unittest smoke tests
```

## Status

This is a V1 prototype. `HeuristicAnalysisProvider` does not call a model. There is no user interface, authentication, or collaboration.

## License

MIT. See [LICENSE](LICENSE).
