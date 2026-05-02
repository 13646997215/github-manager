import json
from pathlib import Path

from benchmarks.scoring import score_list_subset
from tools.colcon_build_summary import summarize_build_log_file
from tools.ros2_runtime_samples import diagnose_runtime_graph_issue, diagnose_runtime_health_issue
from tools.ros2_workspace_inspect import inspect_workspace

REPO_ROOT = Path(__file__).resolve().parents[2]
SUCCESS_LOG = REPO_ROOT / 'benchmarks' / 'fixtures' / 'sample_colcon_success.log'
DEMO_WS = REPO_ROOT / 'examples' / 'demo_workspace' / 'demo_ws'
RUNTIME_GRAPH = REPO_ROOT / 'benchmarks' / 'fixtures' / 'runtime_qos_mismatch_graph.json'
RUNTIME_HEALTH = REPO_ROOT / 'benchmarks' / 'fixtures' / 'runtime_controller_activation_failure.json'


def test_success_build_fixture_reports_success_path():
    result = summarize_build_log_file(str(SUCCESS_LOG), workspace_root=str(DEMO_WS), return_code=0)
    assert result['success'] is True
    assert result['packages_failed'] == 0
    assert 'proceed_to_launch' in result['next_actions']
    json.dumps(result)


def test_demo_workspace_inspection_still_detects_launch_assets():
    result = inspect_workspace(str(DEMO_WS))
    assert result['launch_files']
    assert result['config_files']


def test_runtime_graph_fixture_produces_expected_root_causes():
    summary = json.loads(RUNTIME_GRAPH.read_text(encoding='utf-8'))
    result = diagnose_runtime_graph_issue(summary)
    score = score_list_subset(result['root_cause_candidates'], ['qos_incompatibility', 'sensor_data_not_reaching_consumer'])
    assert score['passed'] is True


def test_runtime_health_fixture_produces_expected_root_causes():
    summary = json.loads(RUNTIME_HEALTH.read_text(encoding='utf-8'))
    result = diagnose_runtime_health_issue(summary)
    score = score_list_subset(result['root_cause_candidates'], ['controller_activation_failure', 'hardware_interface_export_issue', 'tf_staleness'])
    assert score['passed'] is True
