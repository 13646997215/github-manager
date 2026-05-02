"""Export repo skill manifest."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from scripts.skills.inspect_repo_skills import list_repo_skills



def export_skill_manifest(output_path: str = "profile/ros2-agent/skill_manifest.json") -> str:
    payload: Dict[str, List[str]] = {"skills": list_repo_skills()}
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return str(path)


if __name__ == "__main__":
    print(export_skill_manifest())
