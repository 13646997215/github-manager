import json

from tools.diagnosers.fusion_diagnoser import fuse_runtime_evidence
from tools.schemas.diagnosis_schema import CandidateCause, DiagnosisReport, ProbeRecommendation, RiskLevel
from tools.schemas.runtime_schema import (
    CollectionMetadata,
    ControllerSnapshot,
    ControllerStateSnapshot,
    RuntimeEvidenceBundle,
    TfSnapshot,
    TopicSnapshot,
)


def test_fuse_runtime_evidence_prioritizes_controller_and_tf_signals():
    bundle = RuntimeEvidenceBundle(
        topics=[TopicSnapshot(name="/scan", publisher_count=1, subscriber_count=0, category="critical_sensor")],
        tf=TfSnapshot(
            metadata=CollectionMetadata(source="tf"),
            frame_count=2,
            stale_frames=["tool0"],
            missing_chains=["map->odom->base_link"],
        ),
        controller=ControllerSnapshot(
            metadata=CollectionMetadata(source="controller"),
            controller_manager_available=True,
            controllers=[
                ControllerStateSnapshot(
                    name="arm_controller",
                    state="inactive",
                    claimed_interfaces=4,
                    required_interfaces=6,
                )
            ],
        ),
    )
    result = fuse_runtime_evidence(bundle)
    assert result["prioritized_candidates"]
    assert result["recommended_next_probe"]
    assert any(candidate["cause"] == "controller_activation_failure" for candidate in result["prioritized_candidates"])
    assert any(candidate["cause"] == "critical_tf_chain_missing" for candidate in result["prioritized_candidates"])
    json.dumps(result)


def test_fuse_runtime_evidence_from_diagnosis_reports_uses_weighted_probe_selection():
    reports = [
        DiagnosisReport(
            domain="controller",
            candidate_causes=[CandidateCause(cause="controller_activation_failure", confidence="high", evidence_refs=["controller:arm"], risk_level=RiskLevel.READ_ONLY)],
            recommended_next_probe=ProbeRecommendation(action="inspect_controller_manager_logs", reason="controller issue", risk_level=RiskLevel.READ_ONLY),
        ),
        DiagnosisReport(
            domain="tf",
            candidate_causes=[CandidateCause(cause="critical_tf_chain_missing", confidence="high", evidence_refs=["tf_chain:map->odom->base_link"], risk_level=RiskLevel.READ_ONLY)],
            recommended_next_probe=ProbeRecommendation(action="inspect_tf_publishers", reason="tf issue", risk_level=RiskLevel.READ_ONLY),
        ),
    ]
    result = fuse_runtime_evidence(None, diagnosis_reports=reports)
    assert result["prioritized_candidates"][0]["cause"] == "controller_activation_failure"
    assert result["recommended_next_probe"] == "inspect_controller_manager_logs"
    json.dumps(result)
