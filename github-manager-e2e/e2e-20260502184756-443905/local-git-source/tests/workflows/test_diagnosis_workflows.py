import json

from tools.collectors.ros2_controller_collect import collect_controllers
from tools.collectors.ros2_env_collect import collect_environment
from tools.collectors.ros2_graph_collect import collect_runtime_graph
from tools.collectors.ros2_tf_collect import collect_tf
from tools.collectors.ros2_workspace_collect import collect_workspace
from tools.diagnosers.controller_diagnoser import diagnose_controller_snapshot
from tools.diagnosers.env_diagnoser import diagnose_environment_snapshot
from tools.diagnosers.fusion_diagnoser import fuse_runtime_evidence
from tools.diagnosers.runtime_graph_diagnoser import diagnose_runtime_graph_bundle
from tools.diagnosers.tf_diagnoser import diagnose_tf_snapshot
from tools.diagnosers.workspace_diagnoser import diagnose_workspace_snapshot
from tools.schemas.diagnosis_schema import CandidateCause, DiagnosisReport, ProbeRecommendation, RiskLevel
from tools.schemas.runtime_schema import (
    CollectionMetadata,
    ControllerSnapshot,
    ControllerStateSnapshot,
    EnvironmentSnapshot,
    RuntimeEvidenceBundle,
    TfSnapshot,
    TopicSnapshot,
    WorkspacePackageSnapshot,
    WorkspaceSnapshot,
)


def test_diagnosis_workflow_prioritizes_runtime_issue_over_workspace_ok(tmp_path):
    ws = tmp_path / "ok_ws"
    pkg = ws / "src" / "demo_pkg"
    pkg.mkdir(parents=True)
    (pkg / "package.xml").write_text("<package><name>demo_pkg</name></package>", encoding="utf-8")
    (pkg / "setup.py").write_text("from setuptools import setup\n", encoding="utf-8")

    env_report = diagnose_environment_snapshot(
        EnvironmentSnapshot(
            metadata=CollectionMetadata(source="env", collection_success=True),
            os_name="Ubuntu",
            os_version="22.04",
            ros_distro="humble",
            expected_ros_distro="humble",
            setup_bash_exists=True,
        )
    )
    ws_report = diagnose_workspace_snapshot(
        WorkspaceSnapshot(
            metadata=CollectionMetadata(source="ws", collection_success=True),
            workspace_root=str(ws),
            looks_like_ros2_workspace=True,
            package_count=1,
            packages=[
                WorkspacePackageSnapshot(
                    name="demo_pkg",
                    path=str(pkg),
                    build_type="ament_python",
                    has_package_xml=True,
                    has_cmakelists=False,
                    has_setup_py=True,
                )
            ],
        )
    )
    bundle = RuntimeEvidenceBundle(topics=[TopicSnapshot(name="/scan", publisher_count=1, subscriber_count=0, category="critical_sensor")])
    graph_report = diagnose_runtime_graph_bundle(bundle)
    fusion = fuse_runtime_evidence(
        None,
        diagnosis_reports=[
            DiagnosisReport(**env_report),
            DiagnosisReport(**ws_report),
            DiagnosisReport(
                domain="runtime_graph",
                candidate_causes=[CandidateCause(cause="critical_sensor_not_consumed", confidence="high", evidence_refs=["topic:/scan"], risk_level=RiskLevel.READ_ONLY)],
                recommended_next_probe=ProbeRecommendation(action="verify_sensor_pipeline", reason="critical sensor topic has no subscribers", risk_level=RiskLevel.READ_ONLY),
            ),
        ],
    )

    assert fusion["prioritized_candidates"]
    assert fusion["prioritized_candidates"][0]["cause"] == "critical_sensor_not_consumed"
    json.dumps(fusion)


def test_fusion_next_probe_selection_prefers_controller_probe():
    controller_report = diagnose_controller_snapshot(
        ControllerSnapshot(
            metadata=CollectionMetadata(source="controller", collection_success=True),
            controller_manager_available=True,
            controllers=[ControllerStateSnapshot(name="arm_controller", state="inactive", claimed_interfaces=4, required_interfaces=6)],
            hardware_interfaces=["joint1/position"],
        )
    )
    tf_report = diagnose_tf_snapshot(
        TfSnapshot(
            metadata=CollectionMetadata(source="tf", collection_success=True),
            frame_count=1,
            missing_chains=["map->odom->base_link"],
        )
    )
    fusion = fuse_runtime_evidence(
        None,
        diagnosis_reports=[
            DiagnosisReport(
                domain="controller",
                candidate_causes=[CandidateCause(cause="controller_activation_failure", confidence="high", evidence_refs=["controller:arm_controller"], risk_level=RiskLevel.READ_ONLY)],
                recommended_next_probe=ProbeRecommendation(action="inspect_controller_manager_logs", reason="controller issue", risk_level=RiskLevel.READ_ONLY),
            ),
            DiagnosisReport(
                domain="tf",
                candidate_causes=[CandidateCause(cause="critical_tf_chain_missing", confidence="high", evidence_refs=["tf_chain:map->odom->base_link"], risk_level=RiskLevel.READ_ONLY)],
                recommended_next_probe=ProbeRecommendation(action="inspect_tf_publishers", reason="tf issue", risk_level=RiskLevel.READ_ONLY),
            ),
        ],
    )
    assert fusion["recommended_next_probe"] == "inspect_controller_manager_logs"
    json.dumps(fusion)
