import json

from tools.collectors.ros2_graph_collect import collect_runtime_graph, parse_topic_info_verbose


def test_parse_topic_info_verbose_extracts_counts_and_type():
    verbose = """
Type: sensor_msgs/msg/LaserScan

Publisher count: 1
Subscription count: 2
Node name: /lidar_driver
Node namespace: /
QoS profile:
  Reliability: RELIABLE
--
Node name: /localizer
Node namespace: /
QoS profile:
  Reliability: BEST_EFFORT
--
Node name: /mapper
Node namespace: /
QoS profile:
  Reliability: BEST_EFFORT
"""
    result = parse_topic_info_verbose("/scan", verbose)
    assert result["name"] == "/scan"
    assert result["publisher_count"] == 1
    assert result["subscriber_count"] == 2
    assert result["message_type"] == "sensor_msgs/msg/LaserScan"
    assert len(result["publishers"]) == 1
    assert len(result["subscribers"]) == 2


def test_collect_runtime_graph_handles_missing_ros2_commands():
    result = collect_runtime_graph(
        cli_outputs={
            "ros2 node list": None,
            "ros2 topic list": None,
        }
    )
    assert result["metadata"]["collection_success"] is False
    assert result["metadata"]["warnings"]
    assert result["nodes"] == []
    assert result["topics"] == []
    json.dumps(result)


def test_collect_runtime_graph_builds_structured_nodes_and_topics():
    result = collect_runtime_graph(
        cli_outputs={
            "ros2 node list": "/lidar_driver\n/localizer\n",
            "ros2 topic list": "/scan\n/debug\n",
            "ros2 topic info --verbose /scan": "Type: sensor_msgs/msg/LaserScan\nPublisher count: 1\nSubscription count: 1\nNode name: /lidar_driver\nNode namespace: /\nQoS profile:\n  Reliability: RELIABLE\n--\nNode name: /localizer\nNode namespace: /\nQoS profile:\n  Reliability: BEST_EFFORT\n",
            "ros2 topic info --verbose /debug": "Type: std_msgs/msg/String\nPublisher count: 1\nSubscription count: 0\nNode name: /lidar_driver\nNode namespace: /\nQoS profile:\n  Reliability: RELIABLE\n",
        }
    )
    assert result["metadata"]["collection_success"] is True
    assert len(result["nodes"]) == 2
    assert len(result["topics"]) == 2
    assert result["topics"][0]["name"] == "/debug" or result["topics"][1]["name"] == "/debug"
    debug_topic = next(topic for topic in result["topics"] if topic["name"] == "/debug")
    assert debug_topic["publisher_count"] == 1
    assert debug_topic["subscriber_count"] == 0
    json.dumps(result)
