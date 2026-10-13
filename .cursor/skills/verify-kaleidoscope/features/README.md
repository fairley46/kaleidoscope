# Kaleidoscope verification map

This directory is the maintained source for verifying user-facing kaleidoscope behavior. Read the index before driving the CLI, then use the matching feature file as the recipe.

## Baseline preconditions

- Repo root is the working directory.
- `PYTHONPATH=src` or an editable install is available.
- Run `.cursor/skills/verify-kaleidoscope/scripts/doctor.sh` and require exit 0.
- Every proof run uses a disposable `--reports-dir` via `scripts/run-isolated.sh`.
- Never write proof runs into the tracked `reports/` directory.

## Driving conventions

- Start every recipe from a clean reports dir.
- Prefer the stdin-pipe path over interactive typing.
- Treat every command as literal.
- Restore nothing after a run except removing the disposable reports dir with `cleanup.sh`.
- Do not remove proof artifacts during cleanup.

## Proof and skip reporting

- Capture the CLI invocation, stdout, stderr, exit code, and master report.
- Mutation proof is the written `Kaleidoscope_Report.md` and per-lens `*_Review.md` files.
- Record the feature ID and entry point used with every artifact.
- Report an unreachable path with the attempted command and the unmet precondition.
- Do not report a skipped entry point as verified through a different path.

## Feature entry contract

Each feature file starts with an H1 title and one paragraph describing the user-visible behavior. It then uses exactly four H2 sections in this order.

1. `Sub-features`
2. `How to get to it (user POV)`
3. `Driving it with verify-kaleidoscope`
4. `Gotchas`

## Features

- [Explore a problem](./explore-problem.md) covers the clarifying-question flow, multi-lens analysis, and master report.
- [Custom lens load](./custom-lens.md) covers dropping a markdown lens into `lenses/` and seeing it in the run.
- [Report files on disk](./report-files.md) covers per-lens reviews and the master report path.
