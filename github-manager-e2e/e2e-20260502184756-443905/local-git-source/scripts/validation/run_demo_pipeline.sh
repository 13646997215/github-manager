#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEMO_WS="$ROOT_DIR/examples/demo_workspace/demo_ws"
SUCCESS_LOG="$ROOT_DIR/benchmarks/fixtures/sample_colcon_success.log"

PYTHONPATH="$ROOT_DIR" python3 "$ROOT_DIR/scripts/audit/env_audit.py"
PYTHONPATH="$ROOT_DIR" python3 "$ROOT_DIR/scripts/audit/workspace_inspect.py" "$DEMO_WS"
PYTHONPATH="$ROOT_DIR" python3 "$ROOT_DIR/scripts/audit/build_summary.py" "$SUCCESS_LOG"

echo "ROS2-Agent demo pipeline completed."
