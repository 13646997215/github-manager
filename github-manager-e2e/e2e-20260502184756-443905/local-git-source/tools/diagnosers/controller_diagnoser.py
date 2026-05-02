"""Controller diagnoser for phase-2."""

from __future__ import annotations

from tools.schemas.diagnosis_schema import CandidateCause, DiagnosisFinding, DiagnosisReport, ProbeRecommendation, RiskLevel, snapshot_to_dict
from tools.schemas.runtime_schema import ControllerSnapshot



def diagnose_controller_snapshot(snapshot: ControllerSnapshot):
    findings = []
    candidate_causes = []
    for controller in snapshot.controllers:
        if controller.state in {"inactive", "unconfigured", "failed"}:
            findings.append(DiagnosisFinding(summary=f"controller not active: {controller.name}", severity="warning", evidence_refs=[f"controller:{controller.name}"]))
            candidate_causes.append(CandidateCause(cause="controller_activation_failure", confidence="high", evidence_refs=[f"controller:{controller.name}"], risk_level=RiskLevel.READ_ONLY))
        if controller.required_interfaces > controller.claimed_interfaces:
            findings.append(DiagnosisFinding(summary=f"controller interfaces incomplete: {controller.name}", severity="warning", evidence_refs=[f"controller:{controller.name}:interfaces"]))
            candidate_causes.append(CandidateCause(cause="hardware_interface_export_issue", confidence="high", evidence_refs=[f"controller:{controller.name}:interfaces"], risk_level=RiskLevel.READ_ONLY))

    report = DiagnosisReport(
        domain="controller",
        findings=findings,
        candidate_causes=candidate_causes,
        recommended_next_probe=ProbeRecommendation(action="inspect_controller_manager_logs", reason="controller manager state needs confirmation", risk_level=RiskLevel.READ_ONLY),
    )
    return snapshot_to_dict(report)
