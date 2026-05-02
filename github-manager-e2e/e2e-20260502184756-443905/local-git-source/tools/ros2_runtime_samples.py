"""Runtime-oriented structured sample outputs for ROS2-Agent Phase-2 planning.

These repository-contained helpers define how future runtime tools should return
graph/topic/node/controller-style summaries and how common runtime failure logs
can be structured into actionable diagnoses.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class NodeSummary:
    name: str
    namespace: str
    publishers: int
    subscribers: int


@dataclass
class TopicSummary:
    name: str
    msg_type: str
    publisher_count: int
    subscriber_count: int


@dataclass
class ControllerSummary:
    name: str
    state: str
    claimed_interfaces: int


@dataclass
class TfSummary:
    frame_count: int
    stale_frames: List[str]


@dataclass
class RuntimeGraphSummary:
    nodes: List[Dict[str, Any]]
    topics: List[Dict[str, Any]]
    warnings: List[str]
    next_actions: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RuntimeHealthSummary:
    controllers: List[Dict[str, Any]]
    tf: Dict[str, Any]
    warnings: List[str]
    next_actions: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def build_runtime_graph_summary(
    *,
    nodes: List[NodeSummary],
    topics: List[TopicSummary],
    warnings: List[str] | None = None,
    next_actions: List[str] | None = None,
) -> Dict[str, Any]:
    summary = RuntimeGraphSummary(
        nodes=[asdict(node) for node in nodes],
        topics=[asdict(topic) for topic in topics],
        warnings=warnings or [],
        next_actions=next_actions or [],
    )
    return summary.to_dict()


def build_runtime_health_summary(
    *,
    controllers: List[ControllerSummary],
    tf: TfSummary,
    warnings: List[str] | None = None,
    next_actions: List[str] | None = None,
) -> Dict[str, Any]:
    summary = RuntimeHealthSummary(
        controllers=[asdict(controller) for controller in controllers],
        tf=asdict(tf),
        warnings=warnings or [],
        next_actions=next_actions or [],
    )
    return summary.to_dict()


def diagnose_runtime_graph_issue(summary: Dict[str, Any]) -> Dict[str, Any]:
    warnings = list(summary.get('warnings', []))
    next_actions = list(summary.get('next_actions', []))
    root_causes: List[str] = []

    for warning in warnings:
        if 'qos_mismatch' in warning:
            root_causes.append('qos_incompatibility')
            if 'align_qos_profiles' not in next_actions:
                next_actions.append('align_qos_profiles')
        if 'starved' in warning or 'timeout' in warning:
            root_causes.append('sensor_data_not_reaching_consumer')
            if 'verify_scan_subscriber_runtime' not in next_actions:
                next_actions.append('verify_scan_subscriber_runtime')

    return {
        'category': 'runtime_graph',
        'passed': len(root_causes) == 0,
        'root_cause_candidates': sorted(set(root_causes)),
        'next_actions': next_actions,
        'warnings': warnings,
    }


def diagnose_runtime_health_issue(summary: Dict[str, Any]) -> Dict[str, Any]:
    warnings = list(summary.get('warnings', []))
    next_actions = list(summary.get('next_actions', []))
    root_causes: List[str] = []

    for warning in warnings:
        if 'controller_activation_failed' in warning:
            root_causes.append('controller_activation_failure')
            if 'inspect_controller_manager_logs' not in next_actions:
                next_actions.append('inspect_controller_manager_logs')
        if 'hardware_interface' in warning:
            root_causes.append('hardware_interface_export_issue')
            if 'verify_hardware_interface_exports' not in next_actions:
                next_actions.append('verify_hardware_interface_exports')

    tf = summary.get('tf', {})
    stale_frames = tf.get('stale_frames', [])
    if stale_frames:
        root_causes.append('tf_staleness')
        if 'inspect_tf_publishers' not in next_actions:
            next_actions.append('inspect_tf_publishers')

    return {
        'category': 'runtime_health',
        'passed': len(root_causes) == 0,
        'root_cause_candidates': sorted(set(root_causes)),
        'next_actions': next_actions,
        'warnings': warnings,
        'stale_frames': stale_frames,
    }
