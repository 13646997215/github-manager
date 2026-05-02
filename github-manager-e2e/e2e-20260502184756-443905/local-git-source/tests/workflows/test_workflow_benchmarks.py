import json
from pathlib import Path


def test_workflow_benchmark_assets_exist():
    base = Path("benchmarks/workflows")
    cases = [
        "launch_runtime_graph_failure",
        "tf_controller_interaction_failure",
        "environment_overlay_conflict",
    ]
    for case in cases:
        case_dir = base / case
        assert (case_dir / "scenario.md").exists()
        assert (case_dir / "evidence.json").exists()
        assert (case_dir / "expected_diagnosis.json").exists()
        assert (case_dir / "verification.md").exists()
        json.loads((case_dir / "expected_diagnosis.json").read_text(encoding="utf-8"))
