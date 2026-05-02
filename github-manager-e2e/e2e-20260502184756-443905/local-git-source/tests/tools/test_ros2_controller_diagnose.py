import json

from tools.ros2_controller_diagnose import ControllerState, diagnose_controllers


def test_diagnose_controllers_detects_activation_and_interface_issues():
    result = diagnose_controllers([
        ControllerState(name='arm_controller', state='inactive', claimed_interfaces=2, required_interfaces=6)
    ])
    assert result['success'] is False
    assert 'controller_activation_failure' in result['root_cause_candidates']
    assert 'hardware_interface_export_issue' in result['root_cause_candidates']
    assert 'inspect_controller_manager_logs' in result['next_actions']
    json.dumps(result)
