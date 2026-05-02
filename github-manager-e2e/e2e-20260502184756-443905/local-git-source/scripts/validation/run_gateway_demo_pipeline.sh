#!/usr/bin/env bash
set -euo pipefail

python3 scripts/validation/generate_benchmark_report.py
python3 scripts/validation/render_markdown_report.py
python3 scripts/validation/export_evidence_pack.py >/dev/null

echo "gateway demo pipeline completed"
