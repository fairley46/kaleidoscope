# Explore a problem

Explore a problem takes a rough statement, asks clarifying questions, runs the default lenses, and prints a summary plus a master report that shows perspectives, tensions, and open questions.

## Sub-features

- `explore-prompt` accepts a problem string as the first CLI argument.
- `explore-questions` asks up to `--max-questions` clarifying prompts.
- `explore-summary` prints `Kaleidoscope summary` after analysis.
- `explore-master` writes `Kaleidoscope_Report.md` with the contracted section headings.

## How to get to it (user POV)

- Run `python3 -m kaleidoscope "<problem>"` from the repo with `PYTHONPATH=src`.
- Run the installed `kaleidoscope "<problem>"` console script.
- Pipe clarifying answers on stdin, or type them at the prompts.

## Driving it with verify-kaleidoscope

Preconditions:

- `scripts/doctor.sh` exits 0.
- No shared reports dir. Use `run-isolated.sh`.

- **Run explore.** Pipe six short answers into an isolated run. Run `scripts/run-isolated.sh explore-1 "We should centralize auth, but I worry about downstream ownership."` with answers on stdin. Exit code is `0`.
- **Confirm framing.** Read `stdout.txt`. It contains `Kaleidoscope framing` and `Kaleidoscope summary`.
- **Confirm master report.** Read `Kaleidoscope_Report.md` in the artifact dir. It contains `## Problem Overview`, perspective or lens highlight content, tension content, and `## Open Questions`.
- **Proof.** Keep `stdout.txt`, `exit_code.txt`, and `Kaleidoscope_Report.md` under the artifact root for this run id.

## Gotchas

- Empty answers skip a dimension. Provide non-empty lines when the recipe needs those fields in the report.
- `_has_enough_context` can stop early before all six prompts. Pass `--max-questions 6` and enough answers for the scenario.
- Do not assert on recommendation text as the primary proof. Recommendations are secondary when present.
