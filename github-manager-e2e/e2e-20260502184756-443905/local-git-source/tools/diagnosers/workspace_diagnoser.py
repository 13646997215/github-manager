"""Workspace diagnoser for phase-2."""

from __future__ import annotations

from tools.schemas.diagnosis_schema import CandidateCause, DiagnosisFinding, DiagnosisReport, ProbeRecommendation, RiskLevel, snapshot_to_dict
from tools.schemas.runtime_schema import WorkspaceSnapshot



def diagnose_workspace_snapshot(snapshot: WorkspaceSnapshot):
    findings = []
    candidate_causes = []

    if not snapshot.looks_like_ros2_workspace:
        findings.append(DiagnosisFinding(summary="workspace structure incomplete", severity="error", evidence_refs=["workspace:layout"]))
        candidate_causes.append(CandidateCause(cause="workspace_layout_invalid", confidence="high", evidence_refs=["workspace:layout"], risk_level=RiskLevel.READ_ONLY))
    for issue in snapshot.metadata_issues:
        findings.append(DiagnosisFinding(summary=issue, severity="warning", evidence_refs=[f"workspace:{issue}"]))
        candidate_causes.append(CandidateCause(cause="workspace_metadata_issue", confidence="medium", evidence_refs=[f"workspace:{issue}"], risk_level=RiskLevel.READ_ONLY))

    report = DiagnosisReport(
        domain="workspace",
        findings=findings,
        candidate_causes=candidate_causes,
        recommended_next_probe=ProbeRecommendation(action="inspect_workspace_metadata", reason="workspace metadata issues need confirmation", risk_level=RiskLevel.READ_ONLY),
    )
    return snapshot_to_dict(report)
