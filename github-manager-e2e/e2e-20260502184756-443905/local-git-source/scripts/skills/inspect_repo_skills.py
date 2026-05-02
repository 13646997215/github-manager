"""Inspect repo skills metadata."""

from __future__ import annotations

from pathlib import Path
from typing import List



def list_repo_skills(root: str = "skills") -> List[str]:
    base = Path(root)
    return sorted(str(path.parent) for path in base.rglob("SKILL.md"))


if __name__ == "__main__":
    for item in list_repo_skills():
        print(item)
