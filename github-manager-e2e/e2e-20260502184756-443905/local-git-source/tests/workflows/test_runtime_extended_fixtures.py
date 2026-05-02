import json
from pathlib import Path

from tools.ros2_controller_diagnose import ControllerState, diagnose_controllers
from tools.ros2_tf_diagnose import TfHealthInput, diagnose_tf_health

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_tf_chain_missing_fixture_maps_to_expected_root_cause():
    fixture = json.loads((REPO_ROOT / 'benchmarks' / 'fixtures' / 'tf_chain_missing.json').read_text(encoding='utf-8'))
    result = diagnose_tf_health(TfHealthInput(**fixture))
    assert 'critical_tf_chain_missing' in result['root_cause_candidates']


def test_controller_unconfigured_fixture_maps_to_expected_root_cause():
    fixture = json.loads((REPO_ROOT / 'benchmarks' / 'fixtures' / 'controller_unconfigured.json').read_text(encoding='utf-8'))
    raw = fixture['controllers'][0]
    result = diagnose_controllers([
        ControllerState(
            name=raw['name'],
            state=raw['state'],
            claimed_interfaces=raw['claimed_interfaces'],
            required_interfaces=raw['required_interfaces'],
        )
    ])
    assert 'controller_activation_failure' in result['root_cause_candidates']
