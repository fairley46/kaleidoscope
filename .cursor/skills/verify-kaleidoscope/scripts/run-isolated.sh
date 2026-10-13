#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run-isolated.sh <run-id> \"<problem statement>\"" >&2
  exit 2
fi

RUN_ID="$1"
PROBLEM="$2"
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
REPORTS_DIR="/tmp/ks-verify-${RUN_ID}"
ARTIFACT_ROOT="/opt/cursor/artifacts/verify-kaleidoscope/${RUN_ID}"
if [[ ! -d /opt/cursor/artifacts ]]; then
  ARTIFACT_ROOT="${ROOT}/artifacts/verify-kaleidoscope/${RUN_ID}"
fi

mkdir -p "$REPORTS_DIR" "$ARTIFACT_ROOT"
cd "$ROOT"

ANSWERS_FILE="${ARTIFACT_ROOT}/answers.txt"
cat >"$ANSWERS_FILE"

set +e
PYTHONPATH=src python3 -m kaleidoscope "$PROBLEM" \
  --max-questions 6 \
  --reports-dir "$REPORTS_DIR" \
  <"$ANSWERS_FILE" \
  >"${ARTIFACT_ROOT}/stdout.txt" \
  2>"${ARTIFACT_ROOT}/stderr.txt"
EC=$?
set -e
echo "$EC" >"${ARTIFACT_ROOT}/exit_code.txt"

if [[ -f "${REPORTS_DIR}/Kaleidoscope_Report.md" ]]; then
  cp "${REPORTS_DIR}/Kaleidoscope_Report.md" "${ARTIFACT_ROOT}/Kaleidoscope_Report.md"
fi

echo "REPORTS_DIR=${REPORTS_DIR}"
echo "ARTIFACT_ROOT=${ARTIFACT_ROOT}"
echo "exit_code=${EC}"
exit "$EC"
