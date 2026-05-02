"""Fusion diagnoser with phase-1 bundle support and phase-2 diagnosis report prioritization."""

from __future__ import annotations

from typing import Dict, List, Optional

from tools.schemas.runtime_schema import RuntimeEvidenceBundle


CAUSE_WEIGHTS = {
    "controller_activation_failure": 90,
    "hardware_interface_export_issue": 85,
    "critical_tf_chain_missing": 80,
    "tf_staleness": 70,
    "critical_sensor_not_consumed": 65,
    "orphan_topic": 50,
    "environment_mismatch": 75,
    "missing_ros_setup": 88,
    "workspace_layout_invalid": 72,
    "workspace_metadata_issue": 60,
    "build_dependency_failure": 82,
    "build_failure": 68,
    "launch_missing_asset": 78,
}



def _fuse_from_bundle(bundle: RuntimeEvidenceBundle) -> Dict[str, object]:
    candidates: List[Dict[str, object]] = []
    uncertainty_gaps: List[str] = []

    for topic in bundle.topics:
        if topic.category == "critical_sensor" and topic.subscriber_count == 0:
            candidates.append({"cause": "critical_sensor_not_consumed", "score": CAUSE_WEIGHTS["critical_sensor_not_consumed"], "evidence_refs": [f"topic:{topic.name}"]})
        elif topic.publisher_count > 0 and topic.subscriber_count == 0:
            candidates.append({"cause": "orphan_topic", "score": CAUSE_WEIGHTS["orphan_topic"], "evidence_refs": [f"topic:{topic.name}"]})

    if bundle.tf is None:
        uncertainty_gaps.append("tf snapshot missing")
    else:
        if bundle.tf.missing_chains:
            candidates.append({"cause": "critical_tf_chain_missing", "score": CAUSE_WEIGHTS["critical_tf_chain_missing"], "evidence_refs": [f"tf_chain:{chain}" for chain in bundle.tf.missing_chains]})
        if bundle.tf.stale_frames:
            candidates.append({"cause": "tf_staleness", "score": CAUSE_WEIGHTS["tf_staleness"], "evidence_refs": [f"tf_frame:{frame}" for frame in bundle.tf.stale_frames]})

    if bundle.controller is None:
        uncertainty_gaps.append("controller snapshot missing")
    else:
        for controller in bundle.controller.controllers:
            if controller.state in {"inactive", "unconfigured", "failed"}:
                candidates.append({"cause": "controller_activation_failure", "score": CAUSE_WEIGHTS["controller_activation_failure"], "evidence_refs": [f"controller:{controller.name}:{controller.state}"]})
            if controller.required_interfaces > controller.claimed_interfaces:
                candidates.append({"cause": "hardware_interface_export_issue", "score": CAUSE_WEIGHTS["hardware_interface_export_issue"], "evidence_refs": [f"controller:{controller.name}:interfaces"]})

    return _finalize_prioritization(candidates, uncertainty_gaps)



def _get_probe_action(probe: object) -> str:
    if isinstance(probe, dict):
        return str(probe.get("action", "collect_missing_runtime_evidence"))
    return str(getattr(probe, "action", "collect_missing_runtime_evidence"))



def _fuse_from_reports(diagnosis_reports: List[object]) -> Dict[str, object]:
    candidates: List[Dict[str, object]] = []
    uncertainty_gaps: List[str] = []
    probe_votes: List[tuple[int, str]] = []

    for report in diagnosis_reports:
        for candidate in getattr(report, "candidate_causes", []):
            cause = candidate.cause
            score = CAUSE_WEIGHTS.get(cause, 40)
            candidates.append({"cause": cause, "score": score, "evidence_refs": list(candidate.evidence_refs)})
        if getattr(report, "recommended_next_probe", None) is not None:
            probe_votes.append((max([CAUSE_WEIGHTS.get(c.cause, 40) for c in getattr(report, "candidate_causes", [])] or [0]), _get_probe_action(report.recommended_next_probe)))
        for finding in getattr(report, "findings", []):
            uncertainty_gaps.extend(list(getattr(finding, "uncertainty_gaps", [])))

    result = _finalize_prioritization(candidates, uncertainty_gaps)
    if probe_votes:
        result["recommended_next_probe"] = sorted(probe_votes, key=lambda item: item[0], reverse=True)[0][1]
    return result



def _finalize_prioritization(candidates: List[Dict[str, object]], uncertainty_gaps: List[str]) -> Dict[str, object]:
    prioritized_candidates = sorted(candidates, key=lambda item: item["score"], reverse=True)[:3]
    recommended_next_probe = "collect_missing_runtime_evidence"
    if prioritized_candidates:
        top_cause = prioritized_candidates[0]["cause"]
        if top_cause == "controller_activation_failure":
            recommended_next_probe = "inspect_controller_manager_logs"
        elif top_cause == "hardware_interface_export_issue":
            recommended_next_probe = "verify_hardware_interface_exports"
        elif top_cause in {"critical_tf_chain_missing", "tf_staleness"}:
            recommended_next_probe = "inspect_tf_publishers"
        elif top_cause == "critical_sensor_not_consumed":
            recommended_next_probe = "verify_sensor_pipeline"
        elif top_cause == "orphan_topic":
            recommended_next_probe = "inspect_downstream_subscribers"
        elif top_cause == "missing_ros_setup":
            recommended_next_probe = "recheck_shell_environment"
        elif top_cause == "launch_missing_asset":
            recommended_next_probe = "verify_launch_assets"

    return {
        "prioritized_candidates": prioritized_candidates,
        "evidence_refs": [ref for candidate in prioritized_candidates for ref in candidate["evidence_refs"]],
        "uncertainty_gaps": uncertainty_gaps,
        "recommended_next_probe": recommended_next_probe,
    }



def fuse_runtime_evidence(bundle: Optional[RuntimeEvidenceBundle], diagnosis_reports: Optional[List[object]] = None) -> Dict[str, object]:
    if diagnosis_reports:
        return _fuse_from_reports(diagnosis_reports)
    if bundle is None:
        return _finalize_prioritization([], ["runtime evidence bundle missing"])
    return _fuse_from_bundle(bundle)
