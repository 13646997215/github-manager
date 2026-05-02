import json
from pathlib import Path

from scripts.skills.export_skill_manifest import export_skill_manifest
from scripts.skills.validate_skill_metadata import validate_skill_metadata


def test_skill_manifest_pipeline(tmp_path: Path):
    output = tmp_path / "skill_manifest.json"
    manifest_path = export_skill_manifest(str(output))
    assert Path(manifest_path).exists()
    payload = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    assert "skills" in payload


def test_skill_metadata_validation_runs():
    result = validate_skill_metadata()
    assert "success" in result
    assert "skill_count" in result
