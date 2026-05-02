import json
from pathlib import Path


def test_replay_manifest_template_contains_required_fields():
    manifest = Path("benchmarks/reports/replay_manifest_template.json")
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    for key in ["case_name", "evidence_path", "diagnosis_path", "verification"]:
        assert key in payload
