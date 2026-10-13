---
name: verify-kaleidoscope
description: Drive the kaleidoscope CLI the way a user does. Use when proving lens exploration output, report files, or CLI changes for this repo.
---

# Verify kaleidoscope

Kaleidoscope is a short-lived local CLI. There is no server. Launch means install once, then drive each run in its own isolated reports directory.

## Launch

From the repo root:

```bash
PYTHONPATH=src python3 -m kaleidoscope --help
```

Or install editable if `python3 -m venv` works in the environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
kaleidoscope --help
```

Ready means `--help` exits 0 and prints `usage: kaleidoscope`. There is no long-lived process to keep up.

Prefer `scripts/run-isolated.sh` from this skill for every proof run. It sets a disposable `--reports-dir` under `/tmp/ks-verify-$RUN_ID`.

## Doctor

```bash
.cursor/skills/verify-kaleidoscope/scripts/doctor.sh
```

Doctor is read-only. It checks Python ≥ 3.9, that `src/kaleidoscope/cli.py` imports, that `lenses/` contains at least the default set, and that a dry `--help` works. Exit non-zero if any check fails. Run doctor first when anything looks off.

## Drive

Harness: tmux/PTY or plain stdin pipe. Prefer the pipe for non-interactive proof.

```bash
RUN_ID=$(date +%s)
.cursor/skills/verify-kaleidoscope/scripts/run-isolated.sh "$RUN_ID" \
  "We should centralize auth, but I worry about downstream ownership." \
  <<'EOF'
Whether to centralize platform auth
Platform and product engineering
Headcount and timeline
Clear ownership with no outage spike
Centralize now; stay federated; phased rollout
Auth drift and onboarding cost
EOF
```

Stable handles:

- Framing banner text `Kaleidoscope framing`
- Summary banner text `Kaleidoscope summary`
- Master report path `$REPORTS_DIR/Kaleidoscope_Report.md`
- Per-lens review files matching `*_Review.md`
- Master report headings used by CI and the feature map (see `features/`)

Do not drive by calling `HeuristicAnalysisProvider` directly in a proof. Exercise `python3 -m kaleidoscope` or the `kaleidoscope` console script.

## Evidence

Proof artifacts go under `/opt/cursor/artifacts/verify-kaleidoscope/<run-id>/` (or `artifacts/verify-kaleidoscope/<run-id>/` when `/opt/cursor` is unavailable). Keep:

- `stdout.txt` and `stderr.txt` from the CLI run
- `exit_code.txt`
- `Kaleidoscope_Report.md` copy
- a terminal screenshot of the summary when the task asks for visual proof (`docs/demo.png` in-repo, plus the artifact copy)

Proof standards:

- Exercise the real user path (CLI + clarifying answers), not internal setters.
- Capture the action (piped answers) and the resulting state (stdout + report files).
- Assert report headings and presence of perspectives, reinforcements, tensions, and open questions as mapped in `features/`.
- Mocks are not used. The heuristic provider is the real V1 path.

## Cleanup

```bash
.cursor/skills/verify-kaleidoscope/scripts/cleanup.sh "$RUN_ID"
```

Cleanup removes `/tmp/ks-verify-$RUN_ID` only. It never deletes `/opt/cursor/artifacts/verify-kaleidoscope/` or `docs/` proof images. There is no process to kill for a completed CLI run. If you started a hung interactive session in tmux, kill that session by name (`ks-verify-$RUN_ID`), not by process name.

## Helpers

| Script | Invocation |
| --- | --- |
| `scripts/doctor.sh` | `.cursor/skills/verify-kaleidoscope/scripts/doctor.sh` |
| `scripts/run-isolated.sh` | `.cursor/skills/verify-kaleidoscope/scripts/run-isolated.sh <run-id> "<problem>"` (answers on stdin) |
| `scripts/cleanup.sh` | `.cursor/skills/verify-kaleidoscope/scripts/cleanup.sh <run-id>` |

All helpers are executable and resolve the repo root from their location.
