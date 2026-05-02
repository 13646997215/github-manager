#!/usr/bin/env bash
set -euo pipefail

PYTHONPATH=. python3 scripts/validation/validate_repo.py
bash scripts/validation/run_tui_layered_validation.sh
python3 -m pytest tests/tools tests/collectors tests/diagnosers tests/workflows tests/recovery tests/integration -q
python3 scripts/validation/generate_benchmark_report.py
python3 scripts/validation/render_markdown_report.py
bash scripts/validation/run_gateway_demo_pipeline.sh

echo "full quality gate passed"
