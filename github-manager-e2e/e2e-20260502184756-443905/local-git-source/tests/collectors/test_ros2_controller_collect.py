import json

from tools.collectors.ros2_controller_collect import collect_controllers, parse_controller_states


def test_parse_controller_states_extracts_required_fields():
    raw = "joint_state_broadcaster active 0 0\narm_controller inactive 4 6\n"
    result = parse_controller_states(raw)
    assert len(result) == 2
    assert result[1]["name"] == "arm_controller"
    assert result[1]["required_interfaces"] == 6


def test_collect_controllers_handles_missing_ros2_control_commands():
    result = collect_controllers(
        cli_outputs={
            "ros2 control list_controllers": None,
            "ros2 control list_hardware_interfaces": None,
        }
    )
    assert result["metadata"]["collection_success"] is False
    assert result["controller_manager_available"] is False
    assert result["controllers"] == []
    json.dumps(result)


def test_collect_controllers_builds_snapshot_with_hardware_interfaces():
    result = collect_controllers(
        cli_outputs={
            "ros2 control list_controllers": "joint_state_broadcaster active 0 0\narm_controller active 6 6\n",
            "ros2 control list_hardware_interfaces": "joint1/position\njoint2/position\n",
        }
    )
    assert result["metadata"]["collection_success"] is True
    assert result["controller_manager_available"] is True
    assert len(result["controllers"]) == 2
    assert result["hardware_interfaces"] == ["joint1/position", "joint2/position"]
    json.dumps(result)
