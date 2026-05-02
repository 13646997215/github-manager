import json

from tools.diagnosers.compat_adapters import (
    controller_snapshot_to_legacy_input,
    graph_bundle_to_legacy_input,
    tf_snapshot_to_legacy_input,
)
from tools.schemas.runtime_schema import (
    CollectionMetadata,
    ControllerSnapshot,
    ControllerStateSnapshot,
    RuntimeEvidenceBundle,
    TfSnapshot,
    TopicSnapshot,
)


def test_graph_bundle_adapter_maps_topics_for_legacy_graph_inspector():
    bundle = RuntimeEvidenceBundle(
        topics=[TopicSnapshot(name="/scan", publisher_count=1, subscriber_count=0, category="critical_sensor")]
    )
    result = graph_bundle_to_legacy_input(bundle)
    assert result["topics"][0]["name"] == "/scan"
    assert result["topics"][0]["category"] == "critical_sensor"
    json.dumps(result)


def test_tf_snapshot_adapter_maps_required_fields():
    snapshot = TfSnapshot(
        metadata=CollectionMetadata(source="test"),
        frame_count=3,
        stale_frames=["tool0"],
        missing_chains=["map->base_link"],
    )
    result = tf_snapshot_to_legacy_input(snapshot)
    assert result["frame_count"] == 3
    assert result["stale_frames"] == ["tool0"]
    assert result["missing_chains"] == ["map->base_link"]


def test_controller_snapshot_adapter_maps_controller_states():
    snapshot = ControllerSnapshot(
        metadata=CollectionMetadata(source="test"),
        controller_manager_available=True,
        controllers=[ControllerStateSnapshot(name="arm_controller", state="inactive", claimed_interfaces=4, required_interfaces=6)],
    )
    result = controller_snapshot_to_legacy_input(snapshot)
    assert result["controllers"][0]["name"] == "arm_controller"
    assert result["controllers"][0]["required_interfaces"] == 6
    json.dumps(result)
