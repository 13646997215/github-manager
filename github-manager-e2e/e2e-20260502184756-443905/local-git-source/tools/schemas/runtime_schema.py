"""Unified runtime evidence schema for ROS2-Agent phase-1 collectors.

This module defines JSON-friendly dataclasses shared by collectors,
compatibility adapters, diagnosers, benchmarks, and reporting layers.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


CommandList = List[str]
WarningList = List[str]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class CollectionMetadata:
    source: str
    collected_at: str = field(default_factory=utc_now_iso)
    command_used: CommandList = field(default_factory=list)
    warnings: WarningList = field(default_factory=list)
    collection_success: bool = True


@dataclass
class CommandAvailability:
    name: str
    available: bool
    path: Optional[str] = None


@dataclass
class EnvironmentSnapshot:
    metadata: CollectionMetadata
    os_name: str
    os_version: str
    ros_distro: Optional[str]
    expected_ros_distro: str
    rmw_implementation: Optional[str] = None
    setup_bash_path: Optional[str] = None
    setup_bash_exists: bool = False
    workspace_path: Optional[str] = None
    commands: List[CommandAvailability] = field(default_factory=list)
    underlay_paths: List[str] = field(default_factory=list)
    overlay_paths: List[str] = field(default_factory=list)
    failures: List[str] = field(default_factory=list)
    repair_hints: List[str] = field(default_factory=list)


@dataclass
class WorkspacePackageSnapshot:
    name: str
    path: str
    build_type: str
    has_package_xml: bool
    has_cmakelists: bool
    has_setup_py: bool


@dataclass
class WorkspaceSnapshot:
    metadata: CollectionMetadata
    workspace_root: str
    looks_like_ros2_workspace: bool
    package_count: int = 0
    packages: List[WorkspacePackageSnapshot] = field(default_factory=list)
    launch_files: List[str] = field(default_factory=list)
    config_files: List[str] = field(default_factory=list)
    urdf_files: List[str] = field(default_factory=list)
    xacro_files: List[str] = field(default_factory=list)
    install_dir_exists: bool = False
    build_dir_exists: bool = False
    log_dir_exists: bool = False
    metadata_issues: List[str] = field(default_factory=list)
    recommended_next_step: str = "review_workspace"


@dataclass
class GraphNodeSnapshot:
    name: str
    publishers: int = 0
    subscribers: int = 0
    services: int = 0
    actions: int = 0
    namespace: Optional[str] = None


@dataclass
class TopicEndpointSnapshot:
    node_name: str
    endpoint_type: str
    qos_profile: Optional[str] = None


@dataclass
class TopicSnapshot:
    name: str
    publisher_count: int
    subscriber_count: int
    category: str = "general"
    message_type: Optional[str] = None
    qos_profile: Optional[str] = None
    sample_rate_hz: Optional[float] = None
    publishers: List[TopicEndpointSnapshot] = field(default_factory=list)
    subscribers: List[TopicEndpointSnapshot] = field(default_factory=list)


@dataclass
class TfSnapshot:
    metadata: CollectionMetadata
    frame_count: int
    stale_frames: List[str] = field(default_factory=list)
    missing_chains: List[str] = field(default_factory=list)
    frame_authorities: Dict[str, str] = field(default_factory=dict)
    sim_time_enabled: Optional[bool] = None
    clock_topic_present: Optional[bool] = None


@dataclass
class ControllerStateSnapshot:
    name: str
    state: str
    claimed_interfaces: int
    required_interfaces: int = 0


@dataclass
class ControllerSnapshot:
    metadata: CollectionMetadata
    controller_manager_available: bool
    controllers: List[ControllerStateSnapshot] = field(default_factory=list)
    hardware_interfaces: List[str] = field(default_factory=list)
    manager_namespace: Optional[str] = None


@dataclass
class LaunchProbeSnapshot:
    metadata: CollectionMetadata
    launch_file: Optional[str] = None
    package_name: Optional[str] = None
    probe_success: bool = False
    missing_assets: List[str] = field(default_factory=list)
    stderr_excerpt: Optional[str] = None


@dataclass
class LogEvidence:
    metadata: CollectionMetadata
    source_path: Optional[str] = None
    severity: str = "info"
    excerpt: str = ""
    evidence_blocks: List[str] = field(default_factory=list)


@dataclass
class RuntimeEvidenceBundle:
    environment: Optional[EnvironmentSnapshot] = None
    workspace: Optional[WorkspaceSnapshot] = None
    graph_nodes: List[GraphNodeSnapshot] = field(default_factory=list)
    topics: List[TopicSnapshot] = field(default_factory=list)
    tf: Optional[TfSnapshot] = None
    controller: Optional[ControllerSnapshot] = None
    launch: Optional[LaunchProbeSnapshot] = None
    logs: List[LogEvidence] = field(default_factory=list)
    bundle_warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def snapshot_to_dict(snapshot: Any) -> Dict[str, Any]:
    return asdict(snapshot)
