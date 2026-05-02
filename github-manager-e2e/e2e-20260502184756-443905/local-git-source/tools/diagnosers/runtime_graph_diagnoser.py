"""Runtime graph diagnoser for phase-2."""

from __future__ import annotations

from tools.schemas.diagnosis_schema import CandidateCause, DiagnosisFinding, DiagnosisReport, ProbeRecommendation, RiskLevel, snapshot_to_dict
from tools.schemas.runtime_schema import RuntimeEvidenceBundle



def diagnose_runtime_graph_bundle(bundle: RuntimeEvidenceBundle):
    findings = []
    candidate_causes = []
    for topic in bundle.topics:
        if topic.category == "critical_sensor" and topic.subscriber_count == 0:
            findings.append(DiagnosisFinding(summary=f"critical sensor topic not consumed: {topic.name}", severity="warning", evidence_refs=[f"topic:{topic.name}"]))
            candidate_causes.append(CandidateCause(cause="critical_sensor_not_consumed", confidence="high", evidence_refs=[f"topic:{topic.name}"], risk_level=RiskLevel.READ_ONLY))
        elif topic.publisher_count > 0 and topic.subscriber_count == 0:
            findings.append(DiagnosisFinding(summary=f"orphan topic: {topic.name}", severity="warning", evidence_refs=[f"topic:{topic.name}"]))
            candidate_causes.append(CandidateCause(cause="orphan_topic", confidence="medium", evidence_refs=[f"topic:{topic.name}"], risk_level=RiskLevel.READ_ONLY))

    report = DiagnosisReport(
        domain="runtime_graph",
        findings=findings,
        candidate_causes=candidate_causes,
        recommended_next_probe=ProbeRecommendation(action="inspect_runtime_topic_consumers", reason="runtime graph shows unconsumed topics", risk_level=RiskLevel.READ_ONLY),
    )
    return snapshot_to_dict(report)
