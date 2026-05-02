"""Structured ROS2 runtime graph inspection helpers for repository-backed diagnostics."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class GraphNode:
    name: str
    publishers: int
    subscribers: int


@dataclass
class GraphTopic:
    name: str
    publisher_count: int
    subscriber_count: int
    category: str = "general"


@dataclass
class GraphInspectionResult:
    success: bool
    nodes: List[Dict[str, Any]]
    topics: List[Dict[str, Any]]
    warnings: List[str]
    next_actions: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def inspect_runtime_graph(nodes: List[GraphNode], topics: List[GraphTopic]) -> Dict[str, Any]:
    warnings: List[str] = []
    next_actions: List[str] = []

    for topic in topics:
        if topic.publisher_count > 0 and topic.subscriber_count == 0:
            warnings.append(f"orphan_topic:{topic.name}")
            if "inspect_downstream_subscribers" not in next_actions:
                next_actions.append("inspect_downstream_subscribers")
        if topic.category == "critical_sensor" and topic.subscriber_count == 0:
            warnings.append(f"critical_sensor_not_consumed:{topic.name}")
            if "verify_sensor_pipeline" not in next_actions:
                next_actions.append("verify_sensor_pipeline")

    success = len(warnings) == 0
    if success:
        next_actions.append("continue_runtime_validation")

    return GraphInspectionResult(
        success=success,
        nodes=[asdict(node) for node in nodes],
        topics=[asdict(topic) for topic in topics],
        warnings=warnings,
        next_actions=next_actions,
    ).to_dict()
