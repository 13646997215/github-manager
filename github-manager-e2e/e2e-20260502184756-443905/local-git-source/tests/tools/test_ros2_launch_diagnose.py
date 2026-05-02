import json
from pathlib import Path

from tools.ros2_launch_diagnose import build_launch_diagnosis_result, diagnose_launch


def test_build_launch_diagnosis_result_basic():
    result = build_launch_diagnosis_result(
        package_name="demo_pkg",
        launch_file="demo.launch.py",
        resolved_path="/tmp/ws/src/demo_pkg/launch/demo.launch.py",
        package_found=True,
        package_prefix="/tmp/ws/install/demo_pkg",
    )
    assert result["package_found"] is True
    assert result["target"]["package_name"] == "demo_pkg"
    json.dumps(result)


def test_diagnose_launch_detects_missing_assets(tmp_path: Path):
    pkg_prefix = tmp_path / "install" / "demo_pkg"
    launch_dir = pkg_prefix / "share" / "demo_pkg" / "launch"
    launch_dir.mkdir(parents=True)
    (launch_dir / "demo.launch.py").write_text("# demo", encoding="utf-8")

    result = diagnose_launch(
        package_name="demo_pkg",
        launch_file="demo.launch.py",
        package_prefix=str(pkg_prefix),
        params_files=[str(tmp_path / "missing.yaml")],
        referenced_assets=[str(tmp_path / "missing.urdf")],
    )
    assert result["package_found"] is True
    assert result["target"]["resolved_path"].endswith("demo.launch.py")
    assert "params_file_missing" in result["root_cause_candidates"]
    assert "referenced_asset_missing" in result["root_cause_candidates"]


def test_diagnose_launch_marks_missing_prefix_as_package_not_found(tmp_path: Path):
    result = diagnose_launch(
        package_name="demo_pkg",
        launch_file="demo.launch.py",
        package_prefix=str(tmp_path / "does_not_exist"),
    )
    assert result["package_found"] is False
    assert "package_not_found" in result["root_cause_candidates"]
