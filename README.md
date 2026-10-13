# Kaleidoscope

[![CI](https://github.com/fairley46/kaleidoscope/actions/workflows/ci.yml/badge.svg)](https://github.com/fairley46/kaleidoscope/actions/workflows/ci.yml)

Local CLI that runs a problem through markdown lenses and writes the notes to disk.

![Kaleidoscope CLI demo](docs/demo.png)

## What it does

You give it a rough problem statement. It asks a few clarifying questions, then runs the loaded lenses. Each lens gets a review file. The run also writes a master report under `reports/`.

Default lenses: Company, Team, Culture, Strategy, Roadmap, Technical, Operational, Financial, and User.

The master report includes an overview, each perspective, where perspectives reinforce each other, tensions between them, open questions, and optional next steps.

## Local files

Output is markdown on your machine. Edit and reread it as needed.

V1 analysis is `HeuristicAnalysisProvider` in `providers.py`. It uses the Python standard library only. `cli.py` constructs it. Another provider can implement `AnalysisProvider`.

## Quickstart

Python 3.9 or newer.

```bash
git clone https://github.com/fairley46/kaleidoscope.git
cd kaleidoscope
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run with a prompt. Type answers at the prompts, or pipe them on stdin:

```bash
kaleidoscope "We should centralize this platform capability, but I am worried about downstream effects."
```

Without the console script:

```bash
PYTHONPATH=src python3 -m kaleidoscope "This migration seems technically right but organizationally risky."
```

Each run writes one `*_Review.md` per lens and `reports/Kaleidoscope_Report.md`. Git ignores generated files in `reports/`.

## Custom lenses

Copy `templates/Lens_Template.md` into `lenses/` and run again. The loader reads every `.md` file in that directory.

## Layout

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

V1 prototype. `HeuristicAnalysisProvider` does not call a model. No web UI, auth, or shared editing.

## License

MIT. See [LICENSE](LICENSE).
