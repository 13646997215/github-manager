#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

PYTHONPATH="$ROOT_DIR" python3 "$ROOT_DIR/scripts/validation/validate_repo.py"
PYTHONPATH="$ROOT_DIR" bash "$ROOT_DIR/scripts/validation/run_tui_layered_validation.sh"
PYTHONPATH="$ROOT_DIR" python3 -m pytest "$ROOT_DIR/tests/tools" "$ROOT_DIR/tests/workflows" -q

echo "ROS2-Agent Phase-2 validation skeleton passed."
