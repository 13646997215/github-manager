import json

from tools.ros2_graph_inspect import GraphNode, GraphTopic, inspect_runtime_graph


def test_inspect_runtime_graph_detects_orphan_and_critical_sensor():
    result = inspect_runtime_graph(
        nodes=[GraphNode(name='lidar_driver', publishers=1, subscribers=0)],
        topics=[
            GraphTopic(name='/robot1/scan', publisher_count=1, subscriber_count=0, category='critical_sensor'),
            GraphTopic(name='/robot1/debug', publisher_count=1, subscriber_count=0),
        ],
    )
    assert result['success'] is False
    assert 'orphan_topic:/robot1/debug' in result['warnings']
    assert 'critical_sensor_not_consumed:/robot1/scan' in result['warnings']
    assert 'verify_sensor_pipeline' in result['next_actions']
    json.dumps(result)
