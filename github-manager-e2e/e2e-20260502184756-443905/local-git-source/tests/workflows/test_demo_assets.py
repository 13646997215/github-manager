import json
from pathlib import Path

from tools.ros2_workspace_inspect import inspect_workspace
from tools.ros2_launch_diagnose import diagnose_launch


REPO_ROOT = Path(__file__).resolve().parents[2]
DEMO_WS = REPO_ROOT / "examples" / "demo_workspace" / "demo_ws"
BROKEN_WS = REPO_ROOT / "examples" / "broken_cases" / "broken_ws_missing_package_xml"


def test_demo_workspace_is_detected_as_ros2_workspace():
    result = inspect_workspace(str(DEMO_WS))
    assert result["looks_like_ros2_workspace"] is True
    assert result["package_count"] == 1
    assert result["packages"][0]["name"] == "demo_nodes"
    assert result["recommended_next_step"] == "build_workspace"
    json.dumps(result)


def test_broken_workspace_missing_package_xml_is_not_ready():
    result = inspect_workspace(str(BROKEN_WS))
    assert result["looks_like_ros2_workspace"] is True
    assert result["package_count"] == 0
    assert result["recommended_next_step"] == "repair_workspace"
    assert any("no package.xml" in warning or "package.xml" in warning for warning in result["warnings"])


def test_demo_launch_diagnosis_with_missing_asset(tmp_path: Path):
    prefix = tmp_path / "install" / "demo_nodes"
    launch_dir = prefix / "share" / "demo_nodes" / "launch"
    launch_dir.mkdir(parents=True)
    (launch_dir / "demo.launch.py").write_text("# demo", encoding="utf-8")

    result = diagnose_launch(
        package_name="demo_nodes",
        launch_file="demo.launch.py",
        package_prefix=str(prefix),
        referenced_assets=[str(tmp_path / "missing.urdf")],
    )
    assert result["package_found"] is True
    assert "referenced_asset_missing" in result["root_cause_candidates"]
