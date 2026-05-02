#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

python3 "$ROOT_DIR/scripts/validation/generate_benchmark_report.py" > "$ROOT_DIR/benchmarks/reports/latest_benchmark_report.json"
python3 "$ROOT_DIR/scripts/validation/render_markdown_report.py"
echo "Wrote benchmark reports to: $ROOT_DIR/benchmarks/reports/latest_benchmark_report.json and latest_benchmark_report.md"
