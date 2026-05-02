import json
from pathlib import Path

from tools.ros2_env_audit import CommandStatus, audit_environment, build_env_audit_result


def test_build_env_audit_result_basic():
    result = build_env_audit_result(
        ros_distro="humble",
        setup_bash_exists=True,
        commands=[CommandStatus(name="ros2", available=True, path="/usr/bin/ros2")],
    )
    assert result["ros_distro"] == "humble"
    assert result["ros_distro_matches"] is True
    assert result["commands"][0]["name"] == "ros2"
    json.dumps(result)


def test_audit_environment_returns_structured_fields():
    result = audit_environment()
    assert "success" in result
    assert "commands" in result
    assert any(item["name"] == "python3" for item in result["commands"])
    assert isinstance(result["next_actions"], list)
