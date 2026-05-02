import json
from pathlib import Path


def test_recovery_benchmark_assets_exist():
    recovery_dir = Path("benchmarks/recovery")
    assert (recovery_dir / "README.md").exists()
    assert (recovery_dir / "recovery_scorecard_template.md").exists()
    assert (recovery_dir / "cases" / "controller_activation_failure.md").exists()


def test_replay_manifest_template_is_valid_json():
    manifest = Path("benchmarks/reports/replay_manifest_template.json")
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["case_name"] == "example_case"
