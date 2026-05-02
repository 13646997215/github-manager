#!/usr/bin/env python3
"""Sample script placeholder for ROS2 workspace inspection."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.ros2_workspace_inspect import inspect_workspace


def main() -> None:
    workspace = sys.argv[1] if len(sys.argv) > 1 else str(ROOT)
    result = inspect_workspace(workspace)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
