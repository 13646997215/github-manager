import json

from tools.schemas.runtime_schema import (
    CollectionMetadata,
    CommandAvailability,
    ControllerSnapshot,
    ControllerStateSnapshot,
    EnvironmentSnapshot,
    GraphNodeSnapshot,
    RuntimeEvidenceBundle,
    TfSnapshot,
    TopicSnapshot,
    WorkspacePackageSnapshot,
    WorkspaceSnapshot,
    snapshot_to_dict,
)


def test_runtime_schema_snapshots_are_json_serializable():
    metadata = CollectionMetadata(source="unit-test", command_used=["ros2 node list"])
    environment = EnvironmentSnapshot(
        metadata=metadata,
        os_name="Ubuntu",
        os_version="22.04",
        ros_distro="humble",
        expected_ros_distro="humble",
        commands=[CommandAvailability(name="ros2", available=True, path="/usr/bin/ros2")],
    )
    workspace = WorkspaceSnapshot(
        metadata=metadata,
        workspace_root="/tmp/ws",
        looks_like_ros2_workspace=True,
        package_count=1,
        packages=[
            WorkspacePackageSnapshot(
                name="demo_pkg",
                path="/tmp/ws/src/demo_pkg",
                build_type="ament_python",
                has_package_xml=True,
                has_cmakelists=False,
                has_setup_py=True,
            )
        ],
    )
    tf_snapshot = TfSnapshot(metadata=metadata, frame_count=3, stale_frames=["tool0"])
    controller = ControllerSnapshot(
        metadata=metadata,
        controller_manager_available=True,
        controllers=[
            ControllerStateSnapshot(
                name="arm_controller",
                state="active",
                claimed_interfaces=6,
                required_interfaces=6,
            )
        ],
    )
    bundle = RuntimeEvidenceBundle(
        environment=environment,
        workspace=workspace,
        graph_nodes=[GraphNodeSnapshot(name="/demo_node", publishers=1, subscribers=2)],
        topics=[TopicSnapshot(name="/scan", publisher_count=1, subscriber_count=1, category="critical_sensor")],
        tf=tf_snapshot,
        controller=controller,
    )

    result = bundle.to_dict()
    assert result["environment"]["os_name"] == "Ubuntu"
    assert result["workspace"]["packages"][0]["name"] == "demo_pkg"
    assert result["tf"]["stale_frames"] == ["tool0"]
    assert result["controller"]["controllers"][0]["name"] == "arm_controller"
    json.dumps(result)


def test_collection_metadata_defaults_are_present():
    metadata = CollectionMetadata(source="collector-test")
    result = snapshot_to_dict(metadata)
    assert result["source"] == "collector-test"
    assert result["collection_success"] is True
    assert isinstance(result["warnings"], list)
    assert "T" in result["collected_at"]


def test_runtime_evidence_bundle_can_hold_partial_snapshots():
    metadata = CollectionMetadata(source="partial-test", warnings=["degraded"])
    environment = EnvironmentSnapshot(
        metadata=metadata,
        os_name="Ubuntu",
        os_version="22.04",
        ros_distro=None,
        expected_ros_distro="humble",
    )
    bundle = RuntimeEvidenceBundle(environment=environment, bundle_warnings=["graph collector skipped"])
    result = bundle.to_dict()
    assert result["environment"]["metadata"]["warnings"] == ["degraded"]
    assert result["topics"] == []
    assert result["bundle_warnings"] == ["graph collector skipped"]
    json.dumps(result)
