#!/usr/bin/env python3
"""Sample script placeholder for ROS2 environment audit."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.ros2_env_audit import audit_environment


def main() -> None:
    result = audit_environment()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
