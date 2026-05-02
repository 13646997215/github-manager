import pytest

from tools.collectors.ros2_graph_collect import collect_runtime_graph, ros2_runtime_available


@pytest.mark.skipif(not ros2_runtime_available(), reason="ros2 CLI not available in current environment")
def test_collect_runtime_graph_integration_runs_when_ros_available():
    result = collect_runtime_graph()
    assert "metadata" in result
    assert "nodes" in result
    assert "topics" in result
    assert isinstance(result["metadata"]["warnings"], list)
