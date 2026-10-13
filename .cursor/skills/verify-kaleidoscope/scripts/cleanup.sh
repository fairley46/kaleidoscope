#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: cleanup.sh <run-id>" >&2
  exit 2
fi

RUN_ID="$1"
REPORTS_DIR="/tmp/ks-verify-${RUN_ID}"

if [[ -d "$REPORTS_DIR" ]]; then
  rm -rf "$REPORTS_DIR"
  echo "removed ${REPORTS_DIR}"
else
  echo "nothing to remove at ${REPORTS_DIR}"
fi

# Evidence under /opt/cursor/artifacts/verify-kaleidoscope/ or artifacts/ is kept.
SESSION="ks-verify-${RUN_ID}"
if command -v tmux >/dev/null 2>&1; then
  if tmux has-session -t "=$SESSION" 2>/dev/null; then
    tmux kill-session -t "=$SESSION"
    echo "killed tmux session ${SESSION}"
  fi
fi
