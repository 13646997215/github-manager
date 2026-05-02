"""Launch diagnoser for phase-2."""

from __future__ import annotations

from tools.schemas.diagnosis_schema import CandidateCause, DiagnosisFinding, DiagnosisReport, ProbeRecommendation, RiskLevel, snapshot_to_dict
from tools.schemas.runtime_schema import LaunchProbeSnapshot



def diagnose_launch_probe(snapshot: LaunchProbeSnapshot):
    findings = []
    candidate_causes = []
    for asset in snapshot.missing_assets:
        findings.append(DiagnosisFinding(summary=f"missing asset: {asset}", severity="error", evidence_refs=[f"launch:{asset}"]))
        candidate_causes.append(CandidateCause(cause="launch_missing_asset", confidence="high", evidence_refs=[f"launch:{asset}"], risk_level=RiskLevel.READ_ONLY))

    if not snapshot.probe_success and snapshot.stderr_excerpt:
        findings.append(DiagnosisFinding(summary="launch probe stderr available", severity="warning", evidence_refs=["launch:stderr"]))

    report = DiagnosisReport(
        domain="launch",
        findings=findings,
        candidate_causes=candidate_causes,
        recommended_next_probe=ProbeRecommendation(action="verify_launch_assets", reason="launch references need to be validated", risk_level=RiskLevel.READ_ONLY),
    )
    return snapshot_to_dict(report)
