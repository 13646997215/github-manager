import json

from tools.collectors.ros2_tf_collect import collect_tf, parse_tf_frames_json


def test_parse_tf_frames_json_extracts_frame_authorities_and_count():
    raw = '{"frames": {"map": {"parent": "world", "broadcaster": "static_pub"}, "odom": {"parent": "map", "broadcaster": "localizer"}, "base_link": {"parent": "odom", "broadcaster": "robot_state_publisher"}}}'
    result = parse_tf_frames_json(raw, expected_chains=["map->odom->base_link"])
    assert result["frame_count"] == 3
    assert result["frame_authorities"]["map"] == "static_pub"
    assert result["missing_chains"] == []


def test_collect_tf_handles_missing_runtime_tools():
    result = collect_tf(cli_outputs={"ros2 run tf2_tools view_frames": None})
    assert result["metadata"]["collection_success"] is False
    assert result["frame_count"] == 0
    assert result["metadata"]["warnings"]
    json.dumps(result)


def test_collect_tf_detects_missing_chain_and_clock_presence():
    result = collect_tf(
        cli_outputs={
            "ros2 run tf2_tools view_frames": '{"frames": {"odom": {"parent": "map", "broadcaster": "localizer"}, "base_link": {"parent": "odom", "broadcaster": "rsp"}}}',
            "ros2 topic list": "/tf\n/tf_static\n/clock\n",
        },
        expected_chains=["map->odom->base_link", "map->camera_link"],
    )
    assert result["metadata"]["collection_success"] is True
    assert result["clock_topic_present"] is True
    assert "map->camera_link" in result["missing_chains"]
    json.dumps(result)
