import pytest

from tools.collectors.ros2_tf_collect import collect_tf, tf_runtime_available


@pytest.mark.skipif(not tf_runtime_available(), reason="ros2/tf2_tools CLI not available in current environment")
def test_collect_tf_integration_runs_when_tf_tools_available():
    result = collect_tf()
    assert "metadata" in result
    assert "frame_count" in result
    assert isinstance(result["missing_chains"], list)
