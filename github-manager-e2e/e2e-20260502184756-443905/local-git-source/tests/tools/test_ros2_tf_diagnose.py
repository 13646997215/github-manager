import json

from tools.ros2_tf_diagnose import TfHealthInput, diagnose_tf_health


def test_diagnose_tf_health_detects_missing_chain_and_staleness():
    result = diagnose_tf_health(TfHealthInput(frame_count=10, stale_frames=['tool0'], missing_chains=['map->odom->base_link']))
    assert result['success'] is False
    assert 'tf_staleness' in result['root_cause_candidates']
    assert 'critical_tf_chain_missing' in result['root_cause_candidates']
    assert 'inspect_tf_publishers' in result['next_actions']
    json.dumps(result)
