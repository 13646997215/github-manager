"""Live/runtime graph collector for ROS2-Agent phase-1.

CLI-first implementation with graceful degradation when ros2 runtime commands
are unavailable. This keeps the collector safe and integration-lite friendly.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from typing import Dict, List, Optional

from tools.schemas.runtime_schema import (
    CollectionMetadata,
    GraphNodeSnapshot,
    TopicEndpointSnapshot,
    TopicSnapshot,
    snapshot_to_dict,
)


TOPIC_KEYWORDS = {
    "critical_sensor": ["scan", "image", "camera", "points", "imu", "odom"],
    "tf": ["/tf", "/tf_static"],
    "command": ["cmd_vel", "command"],
    "status": ["status", "state"],
}


def ros2_runtime_available() -> bool:
    return shutil.which("ros2") is not None


def run_cli(command: str, cli_outputs: Optional[Dict[str, Optional[str]]] = None) -> Optional[str]:
    if cli_outputs is not None and command in cli_outputs:
        return cli_outputs[command]
    try:
        completed = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
        )
        return completed.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def classify_topic(name: str) -> str:
    lowered = name.lower()
    for category, keywords in TOPIC_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return category
    return "general"


def parse_node_list(raw_output: Optional[str]) -> List[GraphNodeSnapshot]:
    if not raw_output:
        return []
    nodes: List[GraphNodeSnapshot] = []
    for line in raw_output.splitlines():
        name = line.strip()
        if not name:
            continue
        namespace = "/"
        if "/" in name.strip("/"):
            namespace = "/" + name.strip("/").rsplit("/", 1)[0]
        nodes.append(GraphNodeSnapshot(name=name, namespace=namespace))
    return nodes


def parse_topic_info_verbose(topic_name: str, raw_output: Optional[str]) -> Dict[str, object]:
    publisher_count = 0
    subscriber_count = 0
    message_type: Optional[str] = None
    publishers: List[TopicEndpointSnapshot] = []
    subscribers: List[TopicEndpointSnapshot] = []
    current_reliability: Optional[str] = None

    if raw_output:
        current_endpoint: Optional[str] = None
        for raw_line in raw_output.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("Type:"):
                message_type = line.split(":", 1)[1].strip()
            elif line.startswith("Publisher count:"):
                publisher_count = int(line.split(":", 1)[1].strip())
            elif line.startswith("Subscription count:"):
                subscriber_count = int(line.split(":", 1)[1].strip())
            elif line.startswith("Node name:"):
                current_endpoint = line.split(":", 1)[1].strip()
            elif line.startswith("Reliability:"):
                current_reliability = line.split(":", 1)[1].strip()
                if current_endpoint:
                    if len(publishers) < publisher_count:
                        publishers.append(
                            TopicEndpointSnapshot(
                                node_name=current_endpoint,
                                endpoint_type="publisher",
                                qos_profile=current_reliability,
                            )
                        )
                    else:
                        subscribers.append(
                            TopicEndpointSnapshot(
                                node_name=current_endpoint,
                                endpoint_type="subscriber",
                                qos_profile=current_reliability,
                            )
                        )
                    current_endpoint = None
                    current_reliability = None

    return snapshot_to_dict(
        TopicSnapshot(
            name=topic_name,
            publisher_count=publisher_count,
            subscriber_count=subscriber_count,
            category=classify_topic(topic_name),
            message_type=message_type,
            publishers=publishers,
            subscribers=subscribers,
        )
    )


def parse_topic_list(topic_names_output: Optional[str], cli_outputs: Optional[Dict[str, Optional[str]]] = None) -> List[Dict[str, object]]:
    if not topic_names_output:
        return []
    topics: List[Dict[str, object]] = []
    for line in topic_names_output.splitlines():
        topic_name = line.strip()
        if not topic_name:
            continue
        verbose_output = run_cli(f"ros2 topic info --verbose {topic_name}", cli_outputs=cli_outputs)
        topics.append(parse_topic_info_verbose(topic_name, verbose_output))
    return topics


def collect_runtime_graph(cli_outputs: Optional[Dict[str, Optional[str]]] = None) -> Dict[str, object]:
    warnings: List[str] = []
    node_output = run_cli("ros2 node list", cli_outputs=cli_outputs)
    topic_output = run_cli("ros2 topic list", cli_outputs=cli_outputs)

    if node_output is None:
        warnings.append("ros2 node list unavailable or failed")
    if topic_output is None:
        warnings.append("ros2 topic list unavailable or failed")

    nodes = [snapshot_to_dict(node) for node in parse_node_list(node_output)]
    topics = parse_topic_list(topic_output, cli_outputs=cli_outputs)

    metadata = CollectionMetadata(
        source="ros2_graph_collect",
        command_used=["ros2 node list", "ros2 topic list", "ros2 topic info --verbose <topic>"],
        warnings=warnings,
        collection_success=len(warnings) == 0,
    )
    return {
        "metadata": snapshot_to_dict(metadata),
        "nodes": nodes,
        "topics": topics,
    }
