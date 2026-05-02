#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

echo "[layer 1/3] CLI contract tests (no Textual required)"
python3 -m pytest \
  tests/tools/test_cli.py \
  tests/tools/test_cli_launcher.py \
  tests/tools/test_cli_contracts.py \
  tests/tools/test_cli_script_entry.py -q

echo "[layer 2/3] TUI smoke fallback"
python3 tools/cli.py --smoke-ui

echo "[layer 3/3] Textual interaction tests (auto-skip if missing)"
python3 -m pytest \
  tests/tools/test_tui_workbench.py \
  tests/tools/test_tui_interaction.py -q || {
    status=$?
    if [ "$status" -eq 5 ]; then
      echo "No textual tests collected; continuing"
    else
      exit "$status"
    fi
  }

echo "tui layered validation passed"
