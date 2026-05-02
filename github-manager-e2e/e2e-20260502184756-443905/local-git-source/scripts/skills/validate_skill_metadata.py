"""Validate repo skill metadata."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from scripts.skills.inspect_repo_skills import list_repo_skills



def validate_skill_metadata(root: str = "skills") -> Dict[str, object]:
    skills = list_repo_skills(root)
    missing = []
    for skill_dir in skills:
        skill_file = Path(skill_dir) / "SKILL.md"
        text = skill_file.read_text(encoding="utf-8")
        if "name:" not in text or "description:" not in text:
            missing.append(str(skill_file))
    return {"success": len(missing) == 0, "skill_count": len(skills), "missing_metadata": missing}


if __name__ == "__main__":
    print(validate_skill_metadata())
