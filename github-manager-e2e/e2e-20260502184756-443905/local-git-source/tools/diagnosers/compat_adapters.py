"""Compatibility adapters between phase-1 runtime schema and legacy diagnoser inputs."""

from __future__ import annotations

from typing import Dict

from tools.schemas.runtime_schema import ControllerSnapshot, RuntimeEvidenceBundle, TfSnapshot



def graph_bundle_to_legacy_input(bundle: RuntimeEvidenceBundle) -> Dict[str, object]:
    return {
        "nodes": [
            {
                "name": node.name,
                "publishers": node.publishers,
                "subscribers": node.subscribers,
            }
            for node in bundle.graph_nodes
        ],
        "topics": [
            {
                "name": topic.name,
                "publisher_count": topic.publisher_count,
                "subscriber_count": topic.subscriber_count,
                "category": topic.category,
            }
            for topic in bundle.topics
        ],
    }



def tf_snapshot_to_legacy_input(snapshot: TfSnapshot) -> Dict[str, object]:
    return {
        "frame_count": snapshot.frame_count,
        "stale_frames": snapshot.stale_frames,
        "missing_chains": snapshot.missing_chains,
    }



def controller_snapshot_to_legacy_input(snapshot: ControllerSnapshot) -> Dict[str, object]:
    return {
        "controllers": [
            {
                "name": controller.name,
                "state": controller.state,
                "claimed_interfaces": controller.claimed_interfaces,
                "required_interfaces": controller.required_interfaces,
            }
            for controller in snapshot.controllers
        ]
    }
