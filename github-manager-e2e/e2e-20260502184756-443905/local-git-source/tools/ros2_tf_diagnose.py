"""Structured TF health diagnosis helpers for ROS2-Agent."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class TfHealthInput:
    frame_count: int
    stale_frames: List[str]
    missing_chains: List[str]


@dataclass
class TfDiagnosisResult:
    success: bool
    frame_count: int
    stale_frames: List[str]
    missing_chains: List[str]
    root_cause_candidates: List[str]
    next_actions: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def diagnose_tf_health(tf: TfHealthInput) -> Dict[str, Any]:
    root_causes: List[str] = []
    next_actions: List[str] = []

    if tf.stale_frames:
        root_causes.append("tf_staleness")
        next_actions.append("inspect_tf_publishers")
    if tf.missing_chains:
        root_causes.append("critical_tf_chain_missing")
        next_actions.append("verify_frame_chain_configuration")

    success = not root_causes
    if success:
        next_actions.append("continue_navigation_runtime_checks")

    return TfDiagnosisResult(
        success=success,
        frame_count=tf.frame_count,
        stale_frames=tf.stale_frames,
        missing_chains=tf.missing_chains,
        root_cause_candidates=sorted(set(root_causes)),
        next_actions=next_actions,
    ).to_dict()
