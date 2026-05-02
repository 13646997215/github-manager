import json
from pathlib import Path

from tools.ros2_launch_diagnose import diagnose_launch

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_launch_fixture_missing_params_detects_missing_params():
    fixture = REPO_ROOT / "benchmarks" / "fixtures" / "launch_missing_params"
    package_prefix = fixture / "install" / "demo_nodes"
    result = diagnose_launch(
        package_name="demo_nodes",
        launch_file="demo.launch.py",
        package_prefix=str(package_prefix),
        params_files=[str(fixture / "install" / "demo_nodes" / "share" / "demo_nodes" / "config" / "demo_params.yaml")],
    )
    assert result["package_found"] is True
    assert "params_file_missing" in result["root_cause_candidates"]
    json.dumps(result)


def test_launch_fixture_missing_launch_file_detects_launch_missing():
    fixture = REPO_ROOT / "benchmarks" / "fixtures" / "launch_missing_launch_file"
    package_prefix = fixture / "install" / "demo_nodes"
    package_prefix.mkdir(parents=True, exist_ok=True)
    result = diagnose_launch(
        package_name="demo_nodes",
        launch_file="demo.launch.py",
        package_prefix=str(package_prefix),
    )
    assert result["package_found"] is True
    assert "launch_file_missing" in result["root_cause_candidates"]


def test_launch_fixture_complete_structure_is_ready_for_probe():
    fixture = REPO_ROOT / "benchmarks" / "fixtures" / "launch_complete"
    package_prefix = fixture / "install" / "demo_nodes"
    result = diagnose_launch(
        package_name="demo_nodes",
        launch_file="demo.launch.py",
        package_prefix=str(package_prefix),
        params_files=[str(fixture / "install" / "demo_nodes" / "share" / "demo_nodes" / "config" / "demo_params.yaml")],
        referenced_assets=[str(fixture / "assets" / "demo.urdf")],
    )
    assert result["package_found"] is True
    assert result["target"]["resolved_path"] is not None
    assert result["next_actions"] == ["execute_minimal_launch_probe"]
