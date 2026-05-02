import json
from pathlib import Path

from tools.collectors.ros2_workspace_collect import collect_workspace


def test_collect_workspace_detects_ros2_layout(tmp_path: Path):
    ws = tmp_path / "demo_ws"
    pkg = ws / "src" / "demo_pkg"
    pkg.mkdir(parents=True)
    (pkg / "package.xml").write_text("<package><name>demo_pkg</name></package>", encoding="utf-8")
    (pkg / "setup.py").write_text("from setuptools import setup\n", encoding="utf-8")
    (pkg / "launch").mkdir()
    (pkg / "launch" / "demo.launch.py").write_text("# launch\n", encoding="utf-8")
    (pkg / "config").mkdir()
    (pkg / "config" / "demo.yaml").write_text("demo: true\n", encoding="utf-8")
    (ws / "install").mkdir()
    (ws / "build").mkdir()
    (ws / "log").mkdir()

    result = collect_workspace(str(ws))
    assert result["metadata"]["source"] == "ros2_workspace_collect"
    assert result["looks_like_ros2_workspace"] is True
    assert result["package_count"] == 1
    assert result["packages"][0]["build_type"] == "ament_python"
    assert result["install_dir_exists"] is True
    assert result["build_dir_exists"] is True
    assert result["log_dir_exists"] is True
    assert result["recommended_next_step"] == "build_workspace"
    json.dumps(result)


def test_collect_workspace_reports_metadata_issues(tmp_path: Path):
    ws = tmp_path / "broken_ws"
    pkg = ws / "src" / "broken_pkg"
    pkg.mkdir(parents=True)
    (pkg / "package.xml").write_text("<package><name>broken_pkg</name></package>", encoding="utf-8")

    result = collect_workspace(str(ws))
    assert result["package_count"] == 1
    assert "package_missing_build_file:broken_pkg" in result["metadata_issues"]
    assert result["recommended_next_step"] == "repair_workspace"
    json.dumps(result)


def test_collect_workspace_handles_missing_src(tmp_path: Path):
    ws = tmp_path / "empty_ws"
    ws.mkdir()

    result = collect_workspace(str(ws))
    assert result["looks_like_ros2_workspace"] is False
    assert "src directory missing" in result["metadata"]["warnings"]
    assert result["recommended_next_step"] == "repair_workspace"
    json.dumps(result)
