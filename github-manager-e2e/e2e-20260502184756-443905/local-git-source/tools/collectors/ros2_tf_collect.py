"""TF collector for ROS2-Agent phase-1.

Phase-1 keeps this CLI-first and tolerant of partial runtime evidence.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from typing import Dict, List, Optional

from tools.schemas.runtime_schema import CollectionMetadata, TfSnapshot, snapshot_to_dict


DEFAULT_EXPECTED_CHAINS = ["map->odom->base_link"]


def tf_runtime_available() -> bool:
    return shutil.which("ros2") is not None and shutil.which("timeout") is not None


def run_cli(command: str, cli_outputs: Optional[Dict[str, Optional[str]]] = None) -> Optional[str]:
    if cli_outputs is not None and command in cli_outputs:
        return cli_outputs[command]
    try:
        completed = subprocess.run(
            f"timeout 15s {command}",
            shell=True,
            check=True,
            text=True,
            capture_output=True,
        )
        return completed.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def parse_tf_frames_json(raw_output: Optional[str], expected_chains: Optional[List[str]] = None) -> Dict[str, object]:
    if not raw_output:
        return snapshot_to_dict(TfSnapshot(metadata=CollectionMetadata(source="ros2_tf_collect", collection_success=False), frame_count=0))

    data = json.loads(raw_output)
    frames = data.get("frames", {})
    frame_authorities = {
        frame_name: frame_info.get("broadcaster", "unknown")
        for frame_name, frame_info in frames.items()
        if isinstance(frame_info, dict)
    }
    frame_names = set(frames.keys())

    missing_chains: List[str] = []
    for chain in expected_chains or DEFAULT_EXPECTED_CHAINS:
        segments = [segment.strip() for segment in chain.split("->") if segment.strip()]
        if not all(segment in frame_names for segment in segments):
            missing_chains.append(chain)

    snapshot = TfSnapshot(
        metadata=CollectionMetadata(source="ros2_tf_collect"),
        frame_count=len(frames),
        missing_chains=missing_chains,
        frame_authorities=frame_authorities,
    )
    return snapshot_to_dict(snapshot)


def collect_tf(
    cli_outputs: Optional[Dict[str, Optional[str]]] = None,
    expected_chains: Optional[List[str]] = None,
) -> Dict[str, object]:
    warnings: List[str] = []
    frames_output = run_cli("ros2 run tf2_tools view_frames", cli_outputs=cli_outputs)
    topic_output = run_cli("ros2 topic list", cli_outputs=cli_outputs)

    if frames_output is None:
        warnings.append("tf frame export unavailable or failed")
        metadata = CollectionMetadata(
            source="ros2_tf_collect",
            command_used=["ros2 run tf2_tools view_frames", "ros2 topic list"],
            warnings=warnings,
            collection_success=False,
        )
        snapshot = TfSnapshot(metadata=metadata, frame_count=0)
        return snapshot_to_dict(snapshot)

    parsed = parse_tf_frames_json(frames_output, expected_chains=expected_chains)
    clock_topic_present = "/clock" in topic_output.splitlines() if topic_output else None
    metadata = CollectionMetadata(
        source="ros2_tf_collect",
        command_used=["ros2 run tf2_tools view_frames", "ros2 topic list"],
        warnings=warnings,
        collection_success=True,
    )
    snapshot = TfSnapshot(
        metadata=metadata,
        frame_count=parsed["frame_count"],
        stale_frames=parsed.get("stale_frames", []),
        missing_chains=parsed.get("missing_chains", []),
        frame_authorities=parsed.get("frame_authorities", {}),
        clock_topic_present=clock_topic_present,
    )
    return snapshot_to_dict(snapshot)
