#!/usr/bin/env python3
"""Render a Markdown benchmark digest from the latest JSON report."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT_JSON = ROOT / 'benchmarks' / 'reports' / 'latest_benchmark_report.json'
REPORT_MD = ROOT / 'benchmarks' / 'reports' / 'latest_benchmark_report.md'


def main() -> None:
    data = json.loads(REPORT_JSON.read_text(encoding='utf-8'))
    overall = data.get('overall', {})
    lines = [
        '# ROS2-Agent Benchmark Report',
        '',
        '## Overall',
        f"- passed: {overall.get('passed')}",
        f"- score: {overall.get('score')} / {overall.get('max_score')}",
        '',
        '## Sections',
    ]
    for key, value in data.items():
        if key == 'overall':
            continue
        lines.extend([
            '',
            f'### {key}',
            f"- passed: {value.get('passed')}",
            f"- score: {value.get('score')} / {value.get('max_score')}",
            f"- matched: {', '.join(value.get('matched', [])) or '(none)'}",
            f"- missing: {', '.join(value.get('missing', [])) or '(none)'}",
        ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding='utf-8')
    print(str(REPORT_MD))


if __name__ == '__main__':
    main()
