import json
from pathlib import Path

from tools.ros2_workspace_inspect import PackageInfo, build_workspace_inspect_result, inspect_workspace


def test_build_workspace_inspect_result_basic():
    result = build_workspace_inspect_result(
        workspace_root="/tmp/ws",
        looks_like_ros2_workspace=True,
        packages=[
            PackageInfo(
                name="demo_pkg",
                path="/tmp/ws/src/demo_pkg",
                build_type="ament_python",
                has_package_xml=True,
                has_cmakelists=False,
                has_setup_py=True,
            )
        ],
    )
    assert result["workspace_root"] == "/tmp/ws"
    assert result["package_count"] == 1
    assert result["packages"][0]["name"] == "demo_pkg"
    json.dumps(result)


def test_inspect_workspace_detects_simple_package(tmp_path: Path):
    ws = tmp_path / "ws"
    pkg = ws / "src" / "demo_pkg"
    pkg.mkdir(parents=True)
    (pkg / "package.xml").write_text("<package><name>demo_pkg</name></package>", encoding="utf-8")
    (pkg / "setup.py").write_text("from setuptools import setup\n", encoding="utf-8")
    result = inspect_workspace(str(ws))
    assert result["looks_like_ros2_workspace"] is True
    assert result["package_count"] == 1
    assert result["packages"][0]["name"] == "demo_pkg"
    assert result["recommended_next_step"] == "build_workspace"
