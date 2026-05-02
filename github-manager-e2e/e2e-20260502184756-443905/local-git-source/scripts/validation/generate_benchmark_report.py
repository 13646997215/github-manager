#!/usr/bin/env python3
"""Generate a lightweight benchmark demonstration report for repository fixtures."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from benchmarks.scoring import (
    score_expected_value,
    score_list_subset,
    score_next_actions,
    score_required_strings,
    score_weighted_sections,
)
from tools.colcon_build_summary import summarize_build_log_file
from tools.ros2_runtime_samples import diagnose_runtime_graph_issue, diagnose_runtime_health_issue
from tools.ros2_workspace_inspect import inspect_workspace


def _load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def _section_passed(*sections):
    return all(section.get('passed', False) for section in sections)


def main() -> None:
    demo_ws = ROOT / 'examples' / 'demo_workspace' / 'demo_ws'
    build_log = ROOT / 'benchmarks' / 'fixtures' / 'sample_colcon_failure.log'
    runtime_graph_fixture = ROOT / 'benchmarks' / 'fixtures' / 'runtime_qos_mismatch_graph.json'
    runtime_health_fixture = ROOT / 'benchmarks' / 'fixtures' / 'runtime_controller_activation_failure.json'

    workspace_result = inspect_workspace(str(demo_ws))
    workspace_text = json.dumps(workspace_result, ensure_ascii=False)
    workspace_score = score_required_strings(workspace_text, ['demo_nodes', 'ament_python', 'build_workspace'])
    workspace_value_score = score_expected_value(workspace_result, 'recommended_next_step', 'build_workspace')

    build_result = summarize_build_log_file(str(build_log))
    build_text = json.dumps(build_result, ensure_ascii=False)
    build_score = score_required_strings(build_text, ['bad_pkg', 'compile/cpp', 'retry_failed_packages'])
    build_action_score = score_next_actions(build_result.get('next_actions', []), ['retry_failed_packages'])

    runtime_graph_result = _load_json(runtime_graph_fixture)
    runtime_graph_diag = diagnose_runtime_graph_issue(runtime_graph_result)
    runtime_graph_warning_score = score_required_strings(
        json.dumps(runtime_graph_diag, ensure_ascii=False),
        ['qos_incompatibility', 'sensor_data_not_reaching_consumer']
    )
    runtime_graph_action_score = score_next_actions(
        runtime_graph_diag.get('next_actions', []),
        ['align_qos_profiles', 'verify_scan_subscriber_runtime']
    )

    runtime_health_result = _load_json(runtime_health_fixture)
    runtime_health_diag = diagnose_runtime_health_issue(runtime_health_result)
    runtime_health_root_score = score_list_subset(
        runtime_health_diag.get('root_cause_candidates', []),
        ['controller_activation_failure', 'hardware_interface_export_issue', 'tf_staleness']
    )
    runtime_health_action_score = score_next_actions(
        runtime_health_diag.get('next_actions', []),
        ['inspect_controller_manager_logs', 'verify_hardware_interface_exports', 'inspect_tf_publishers']
    )

    overall = score_weighted_sections([
        ('workspace_demo', 1.0, _section_passed(workspace_score, workspace_value_score)),
        ('build_failure_demo', 1.0, _section_passed(build_score, build_action_score)),
        ('runtime_graph_demo', 1.0, _section_passed(runtime_graph_warning_score, runtime_graph_action_score)),
        ('runtime_health_demo', 1.0, _section_passed(runtime_health_root_score, runtime_health_action_score)),
    ])

    report = {
        'workspace_demo': workspace_score,
        'workspace_next_step': workspace_value_score,
        'build_failure_demo': build_score,
        'build_failure_next_actions': build_action_score,
        'runtime_graph_demo': runtime_graph_warning_score,
        'runtime_graph_next_actions': runtime_graph_action_score,
        'runtime_health_demo': runtime_health_root_score,
        'runtime_health_next_actions': runtime_health_action_score,
        'overall': overall,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
