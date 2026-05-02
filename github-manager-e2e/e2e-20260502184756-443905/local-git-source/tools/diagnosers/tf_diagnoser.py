"""TF diagnoser for phase-2."""

from __future__ import annotations

from tools.schemas.diagnosis_schema import CandidateCause, DiagnosisFinding, DiagnosisReport, ProbeRecommendation, RiskLevel, snapshot_to_dict
from tools.schemas.runtime_schema import TfSnapshot



def diagnose_tf_snapshot(snapshot: TfSnapshot):
    findings = []
    candidate_causes = []
    for frame in snapshot.stale_frames:
        findings.append(DiagnosisFinding(summary=f"stale TF frame: {frame}", severity="warning", evidence_refs=[f"tf:{frame}"]))
        candidate_causes.append(CandidateCause(cause="tf_staleness", confidence="medium", evidence_refs=[f"tf:{frame}"], risk_level=RiskLevel.READ_ONLY))
    for chain in snapshot.missing_chains:
        findings.append(DiagnosisFinding(summary=f"missing TF chain: {chain}", severity="error", evidence_refs=[f"tf_chain:{chain}"]))
        candidate_causes.append(CandidateCause(cause="critical_tf_chain_missing", confidence="high", evidence_refs=[f"tf_chain:{chain}"], risk_level=RiskLevel.READ_ONLY))

    report = DiagnosisReport(
        domain="tf",
        findings=findings,
        candidate_causes=candidate_causes,
        recommended_next_probe=ProbeRecommendation(action="inspect_tf_publishers", reason="TF chain health is incomplete", risk_level=RiskLevel.READ_ONLY),
    )
    return snapshot_to_dict(report)
