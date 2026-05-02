#!/usr/bin/env python3
"""Sample script placeholder for colcon build summary."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.colcon_build_summary import summarize_build_log_file


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: build_summary.py <log_path>")
    result = summarize_build_log_file(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
