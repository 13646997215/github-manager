import json

from tools.ros2_runtime_samples import (
    ControllerSummary,
    NodeSummary,
    TfSummary,
    TopicSummary,
    build_runtime_graph_summary,
    build_runtime_health_summary,
    diagnose_runtime_graph_issue,
    diagnose_runtime_health_issue,
)


def test_build_runtime_graph_summary_serializable():
    result = build_runtime_graph_summary(
        nodes=[NodeSummary(name='mapper', namespace='/robot1', publishers=2, subscribers=3)],
        topics=[TopicSummary(name='/map', msg_type='nav_msgs/msg/OccupancyGrid', publisher_count=1, subscriber_count=2)],
        warnings=['graph_ok'],
        next_actions=['continue_runtime_checks'],
    )
    assert result['nodes'][0]['name'] == 'mapper'
    json.dumps(result)


def test_build_runtime_health_summary_serializable():
    result = build_runtime_health_summary(
        controllers=[ControllerSummary(name='arm_controller', state='active', claimed_interfaces=6)],
        tf=TfSummary(frame_count=12, stale_frames=[]),
        warnings=[],
        next_actions=['continue_motion_validation'],
    )
    assert result['controllers'][0]['state'] == 'active'
    json.dumps(result)


def test_diagnose_runtime_graph_issue_detects_qos_mismatch():
    result = diagnose_runtime_graph_issue({
        'warnings': ['qos_mismatch:/robot1/scan', 'downstream_localization_starved'],
        'next_actions': [],
    })
    assert result['passed'] is False
    assert 'qos_incompatibility' in result['root_cause_candidates']
    assert 'sensor_data_not_reaching_consumer' in result['root_cause_candidates']
    assert 'align_qos_profiles' in result['next_actions']


def test_diagnose_runtime_health_issue_detects_controller_tf_problems():
    result = diagnose_runtime_health_issue({
        'warnings': ['controller_activation_failed:arm_controller', 'hardware_interface_not_claimed'],
        'next_actions': [],
        'tf': {'stale_frames': ['tool0']},
    })
    assert result['passed'] is False
    assert 'controller_activation_failure' in result['root_cause_candidates']
    assert 'hardware_interface_export_issue' in result['root_cause_candidates']
    assert 'tf_staleness' in result['root_cause_candidates']
    assert 'inspect_tf_publishers' in result['next_actions']
