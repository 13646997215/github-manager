"""Environment diagnoser for phase-2."""

from __future__ import annotations

from tools.schemas.diagnosis_schema import CandidateCause, DiagnosisFinding, DiagnosisReport, ProbeRecommendation, RiskLevel, snapshot_to_dict
from tools.schemas.runtime_schema import EnvironmentSnapshot



def diagnose_environment_snapshot(snapshot: EnvironmentSnapshot):
    findings = []
    candidate_causes = []

    if snapshot.ros_distro != snapshot.expected_ros_distro:
        findings.append(DiagnosisFinding(summary="ROS distro mismatch", severity="warning", evidence_refs=["env:ros_distro"]))
        candidate_causes.append(CandidateCause(cause="environment_mismatch", confidence="high", evidence_refs=["env:ros_distro"], risk_level=RiskLevel.READ_ONLY))
    if not snapshot.setup_bash_exists:
        findings.append(DiagnosisFinding(summary="expected ROS setup.bash missing", severity="error", evidence_refs=["env:setup_bash"]))
        candidate_causes.append(CandidateCause(cause="missing_ros_setup", confidence="high", evidence_refs=["env:setup_bash"], risk_level=RiskLevel.READ_ONLY))

    report = DiagnosisReport(
        domain="environment",
        findings=findings,
        candidate_causes=candidate_causes,
        recommended_next_probe=ProbeRecommendation(action="recheck_shell_environment", reason="environment facts are incomplete or mismatched", risk_level=RiskLevel.READ_ONLY),
    )
    return snapshot_to_dict(report)
