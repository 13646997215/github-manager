import json

from tools.schemas.diagnosis_schema import DiagnosisReport, CandidateCause, DiagnosisFinding, ProbeRecommendation, RiskLevel, snapshot_to_dict


def test_diagnosis_schema_serializes_report():
    report = DiagnosisReport(
        domain="runtime_graph",
        findings=[DiagnosisFinding(summary="critical topic not consumed", severity="warning", evidence_refs=["topic:/scan"])],
        candidate_causes=[CandidateCause(cause="critical_sensor_not_consumed", confidence="high", evidence_refs=["topic:/scan"], risk_level=RiskLevel.READ_ONLY)],
        recommended_next_probe=ProbeRecommendation(action="verify_sensor_pipeline", reason="critical sensor has no subscribers", risk_level=RiskLevel.READ_ONLY),
    )
    result = snapshot_to_dict(report)
    assert result["domain"] == "runtime_graph"
    assert result["candidate_causes"][0]["risk_level"] == "read_only"
    json.dumps(result)
