import pytest

from tools.collectors.ros2_controller_collect import collect_controllers, ros2_control_available


@pytest.mark.skipif(not ros2_control_available(), reason="ros2 CLI not available in current environment")
def test_collect_controllers_integration_runs_when_ros_available():
    result = collect_controllers()
    assert "metadata" in result
    assert "controllers" in result
    assert isinstance(result["hardware_interfaces"], list)
