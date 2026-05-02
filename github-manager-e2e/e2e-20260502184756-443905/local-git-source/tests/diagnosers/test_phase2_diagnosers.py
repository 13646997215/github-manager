import json

from tools.diagnosers.build_diagnoser import diagnose_build_summary
from tools.diagnosers.controller_diagnoser import diagnose_controller_snapshot
from tools.diagnosers.env_diagnoser import diagnose_environment_snapshot
from tools.diagnosers.launch_diagnoser import diagnose_launch_probe
from tools.diagnosers.runtime_graph_diagnoser import diagnose_runtime_graph_bundle
from tools.diagnosers.tf_diagnoser import diagnose_tf_snapshot
from tools.diagnosers.workspace_diagnoser import diagnose_workspace_snapshot
from tools.schemas.runtime_schema import (
    CollectionMetadata,
    ControllerSnapshot,
    ControllerStateSnapshot,
    EnvironmentSnapshot,
    LaunchProbeSnapshot,
    RuntimeEvidenceBundle,
    TfSnapshot,
    TopicSnapshot,
    WorkspaceSnapshot,
)


def test_env_diagnoser_reports_missing_setup_and_ros_distro_mismatch():
    snapshot = EnvironmentSnapshot(
        metadata=CollectionMetadata(source="env", warnings=["ROS_DISTRO is 'iron', expected 'humble'"] , collection_success=False),
        os_name="Ubuntu",
        os_version="22.04",
        ros_distro="iron",
        expected_ros_distro="humble",
        setup_bash_exists=False,
        failures=["/opt/ros/humble/setup.bash not found"],
        repair_hints=["install_or_verify_ros_setup"],
    )
    result = diagnose_environment_snapshot(snapshot)
    assert result["findings"]
    assert result["candidate_causes"]
    json.dumps(result)


def test_workspace_diagnoser_reports_metadata_issues():
    snapshot = WorkspaceSnapshot(
        metadata=CollectionMetadata(source="ws"),
        workspace_root="/tmp/ws",
        looks_like_ros2_workspace=True,
        metadata_issues=["package_missing_build_file:demo_pkg"],
        recommended_next_step="repair_workspace",
    )
    result = diagnose_workspace_snapshot(snapshot)
    assert result["findings"]
    assert result["recommended_next_probe"]["action"] == "inspect_workspace_metadata"
    json.dumps(result)


def test_build_diagnoser_reports_missing_dependencies():
    result = diagnose_build_summary(
        {
            "success": False,
            "failures": ["missing dependency: rclpy"],
            "warnings": [],
            "next_actions": ["install_missing_dependencies"],
        }
    )
    assert result["candidate_causes"][0]["cause"] == "build_dependency_failure"
    json.dumps(result)


def test_launch_diagnoser_reports_missing_assets():
    snapshot = LaunchProbeSnapshot(
        metadata=CollectionMetadata(source="launch", collection_success=False),
        launch_file="demo.launch.py",
        probe_success=False,
        missing_assets=["demo_params.yaml"],
    )
    result = diagnose_launch_probe(snapshot)
    assert result["candidate_causes"][0]["cause"] == "launch_missing_asset"
    json.dumps(result)


def test_runtime_graph_diagnoser_reports_unconsumed_sensor_topic():
    bundle = RuntimeEvidenceBundle(
        topics=[TopicSnapshot(name="/scan", publisher_count=1, subscriber_count=0, category="critical_sensor")]
    )
    result = diagnose_runtime_graph_bundle(bundle)
    assert result["candidate_causes"][0]["cause"] == "critical_sensor_not_consumed"
    json.dumps(result)


def test_tf_diagnoser_reports_missing_chain_and_stale_frames():
    snapshot = TfSnapshot(
        metadata=CollectionMetadata(source="tf"),
        frame_count=2,
        stale_frames=["tool0"],
        missing_chains=["map->odom->base_link"],
    )
    result = diagnose_tf_snapshot(snapshot)
    assert len(result["candidate_causes"]) == 2
    json.dumps(result)


def test_controller_diagnoser_reports_activation_and_interface_issues():
    snapshot = ControllerSnapshot(
        metadata=CollectionMetadata(source="controller"),
        controller_manager_available=True,
        controllers=[ControllerStateSnapshot(name="arm_controller", state="inactive", claimed_interfaces=4, required_interfaces=6)],
    )
    result = diagnose_controller_snapshot(snapshot)
    assert len(result["candidate_causes"]) == 2
    json.dumps(result)
