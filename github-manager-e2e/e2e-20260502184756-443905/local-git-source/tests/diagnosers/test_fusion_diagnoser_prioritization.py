import json

from tools.diagnosers.fusion_diagnoser import fuse_runtime_evidence
from tools.schemas.diagnosis_schema import CandidateCause, DiagnosisReport, ProbeRecommendation, RiskLevel


def test_fusion_prioritization_prefers_higher_weight_candidates():
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
