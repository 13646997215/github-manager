#!/usr/bin/env python3
"""Sample script placeholder for launch diagnosis."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.ros2_launch_diagnose import diagnose_launch


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit("usage: launch_diagnose.py <package_name> <launch_file> [package_prefix]")
    package_name = sys.argv[1]
    launch_file = sys.argv[2]
    package_prefix = sys.argv[3] if len(sys.argv) > 3 else None
    result = diagnose_launch(
        package_name=package_name,
        launch_file=launch_file,
        package_prefix=package_prefix,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
