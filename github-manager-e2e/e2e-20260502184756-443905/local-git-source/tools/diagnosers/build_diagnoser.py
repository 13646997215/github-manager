"""Build diagnoser for phase-2."""

from __future__ import annotations

from tools.schemas.diagnosis_schema import CandidateCause, DiagnosisFinding, DiagnosisReport, ProbeRecommendation, RiskLevel, snapshot_to_dict



def diagnose_build_summary(build_summary):
    findings = []
    candidate_causes = []
    for failure in build_summary.get("failures", []):
        findings.append(DiagnosisFinding(summary=failure, severity="error", evidence_refs=[f"build:{failure}"]))
        cause = "build_dependency_failure" if "dependency" in failure else "build_failure"
        candidate_causes.append(CandidateCause(cause=cause, confidence="high", evidence_refs=[f"build:{failure}"], risk_level=RiskLevel.READ_ONLY))

    report = DiagnosisReport(
        domain="build",
        findings=findings,
        candidate_causes=candidate_causes,
        recommended_next_probe=ProbeRecommendation(action="replay_colcon_failure", reason="build failure needs direct log confirmation", risk_level=RiskLevel.READ_ONLY),
    )
    return snapshot_to_dict(report)
