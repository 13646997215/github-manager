import json

import pytest

from tools.collectors.ros2_env_collect import (
    collect_environment,
    parse_ament_prefix_path,
    should_require_command,
)


def test_parse_ament_prefix_path_splits_nonempty_entries():
    result = parse_ament_prefix_path("/opt/ros/humble:/tmp/ws/install::/overlay")
    assert result == ["/opt/ros/humble", "/tmp/ws/install", "/overlay"]


def test_should_require_command_marks_core_commands_required():
    assert should_require_command("ros2") is True
    assert should_require_command("colcon") is True
    assert should_require_command("python3") is True
    assert should_require_command("rviz2") is False


def test_collect_environment_returns_runtime_schema_snapshot(monkeypatch):
    monkeypatch.setenv("ROS_DISTRO", "humble")
    monkeypatch.setenv("RMW_IMPLEMENTATION", "rmw_fastrtps_cpp")
    monkeypatch.setenv("AMENT_PREFIX_PATH", "/opt/ros/humble:/tmp/demo_ws/install")

    result = collect_environment(
        workspace_path="/tmp/demo_ws",
        expected_ros_distro="humble",
        command_lookup={
            "ros2": "/usr/bin/ros2",
            "colcon": "/usr/bin/colcon",
            "rosdep": None,
            "python3": "/usr/bin/python3",
            "rviz2": None,
            "gazebo": None,
            "gz": None,
        },
        setup_bash_exists=True,
        os_name_override="Ubuntu",
        os_version_override="22.04",
    )

    assert result["metadata"]["source"] == "ros2_env_collect"
    assert result["ros_distro"] == "humble"
    assert result["rmw_implementation"] == "rmw_fastrtps_cpp"
    assert result["underlay_paths"] == ["/opt/ros/humble"]
    assert result["overlay_paths"] == ["/tmp/demo_ws/install"]
    assert result["metadata"]["collection_success"] is True
    json.dumps(result)


def test_collect_environment_reports_missing_required_commands(monkeypatch):
    monkeypatch.delenv("ROS_DISTRO", raising=False)
    monkeypatch.delenv("RMW_IMPLEMENTATION", raising=False)
    monkeypatch.delenv("AMENT_PREFIX_PATH", raising=False)

    result = collect_environment(
        expected_ros_distro="humble",
        command_lookup={
            "ros2": None,
            "colcon": None,
            "rosdep": None,
            "python3": "/usr/bin/python3",
            "rviz2": None,
            "gazebo": None,
            "gz": None,
        },
        setup_bash_exists=False,
        os_name_override="Ubuntu",
        os_version_override="22.04",
    )

    assert result["metadata"]["collection_success"] is False
    assert any("required command missing: ros2" == item for item in result["failures"])
    assert any("required command missing: colcon" == item for item in result["failures"])
    assert any("/opt/ros/humble/setup.bash not found" == item for item in result["failures"])
    assert "install_or_verify_ros_setup" in result["repair_hints"]
    assert "source_expected_ros_setup" in result["repair_hints"]
    json.dumps(result)
