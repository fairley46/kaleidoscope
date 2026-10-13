#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"

python3 - <<'PY'
import sys
from pathlib import Path

if sys.version_info < (3, 9):
    raise SystemExit(f"Python >= 3.9 required, found {sys.version}")

root = Path(".").resolve()
cli = root / "src" / "kaleidoscope" / "cli.py"
if not cli.is_file():
    raise SystemExit(f"missing {cli}")

lenses = sorted((root / "lenses").glob("*.md"))
if len(lenses) < 9:
    raise SystemExit(f"expected >=9 lens files, found {len(lenses)}")

sys.path.insert(0, str(root / "src"))
import kaleidoscope.cli  # noqa: F401
print(f"doctor ok: python={sys.version.split()[0]} lenses={len(lenses)}")
PY

PYTHONPATH=src python3 -m kaleidoscope --help >/dev/null
echo "doctor ok: --help exits 0"
