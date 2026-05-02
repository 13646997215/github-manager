"""Runtime environment collector for ROS2-Agent phase-1.

Read-only collector that upgrades the older env audit logic into the shared
runtime schema used by later diagnosers and reporting layers.
"""

from __future__ import annotations

import os
import platform
import shutil
from pathlib import Path
from typing import Dict, List, Optional

from tools.schemas.runtime_schema import (
    CollectionMetadata,
    CommandAvailability,
    EnvironmentSnapshot,
    snapshot_to_dict,
)


DEFAULT_COMMANDS = ["ros2", "colcon", "rosdep", "python3", "rviz2", "gazebo", "gz"]
REQUIRED_COMMANDS = {"ros2", "colcon", "python3"}


def read_os_release() -> Dict[str, str]:
    info: Dict[str, str] = {}
    os_release = Path("/etc/os-release")
    if not os_release.exists():
        return info

    for line in os_release.read_text(encoding="utf-8").splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        info[key] = value.strip().strip('"')
    return info


def parse_ament_prefix_path(raw_value: Optional[str]) -> List[str]:
    if not raw_value:
        return []
    return [entry for entry in raw_value.split(":") if entry]


def should_require_command(name: str) -> bool:
    return name in REQUIRED_COMMANDS


def detect_command(name: str, command_lookup: Optional[Dict[str, Optional[str]]] = None) -> CommandAvailability:
    path = command_lookup[name] if command_lookup is not None and name in command_lookup else shutil.which(name)
    return CommandAvailability(name=name, available=path is not None, path=path)


def infer_repair_hints(
    *,
    ros_distro: Optional[str],
    expected_ros_distro: str,
    setup_bash_exists: bool,
    command_statuses: List[CommandAvailability],
    failures: List[str],
) -> List[str]:
    hints: List[str] = []
    availability = {command.name: command.available for command in command_statuses}

    if not setup_bash_exists:
        hints.append("install_or_verify_ros_setup")
    if ros_distro != expected_ros_distro:
        hints.append("source_expected_ros_setup")
    if not availability.get("colcon", False):
        hints.append("install_colcon")
    if not availability.get("rosdep", False):
        hints.append("install_or_init_rosdep")
    if failures:
        hints.append("resolve_environment_failures")
    if not hints:
        hints.append("proceed_to_workspace_collection")
    return hints


def classify_prefix_paths(prefix_paths: List[str]) -> tuple[List[str], List[str]]:
    underlay_paths: List[str] = []
    overlay_paths: List[str] = []
    for path in prefix_paths:
        if path.startswith("/opt/ros/"):
            underlay_paths.append(path)
        else:
            overlay_paths.append(path)
    return underlay_paths, overlay_paths


def collect_environment(
    workspace_path: Optional[str] = None,
    expected_ros_distro: str = "humble",
    command_lookup: Optional[Dict[str, Optional[str]]] = None,
    setup_bash_exists: Optional[bool] = None,
    os_name_override: Optional[str] = None,
    os_version_override: Optional[str] = None,
) -> Dict[str, object]:
    os_release = read_os_release()
    os_name = os_name_override or os_release.get("NAME", platform.system())
    os_version = os_version_override or os_release.get("VERSION_ID", platform.release())
    ros_distro = os.environ.get("ROS_DISTRO")
    rmw_implementation = os.environ.get("RMW_IMPLEMENTATION")
    prefix_paths = parse_ament_prefix_path(os.environ.get("AMENT_PREFIX_PATH"))
    underlay_paths, overlay_paths = classify_prefix_paths(prefix_paths)

    setup_path = f"/opt/ros/{expected_ros_distro}/setup.bash"
    setup_exists = Path(setup_path).exists() if setup_bash_exists is None else setup_bash_exists
    command_statuses = [detect_command(name, command_lookup=command_lookup) for name in DEFAULT_COMMANDS]

    warnings: List[str] = []
    failures: List[str] = []

    if ros_distro is None:
        warnings.append("ROS_DISTRO is not set in current shell")
    elif ros_distro != expected_ros_distro:
        warnings.append(f"ROS_DISTRO is '{ros_distro}', expected '{expected_ros_distro}'")

    if not rmw_implementation:
        warnings.append("RMW_IMPLEMENTATION is not set in current shell")

    if not setup_exists:
        failures.append(f"/opt/ros/{expected_ros_distro}/setup.bash not found")

    for command in command_statuses:
        if should_require_command(command.name) and not command.available:
            failures.append(f"required command missing: {command.name}")

    repair_hints = infer_repair_hints(
        ros_distro=ros_distro,
        expected_ros_distro=expected_ros_distro,
        setup_bash_exists=setup_exists,
        command_statuses=command_statuses,
        failures=failures,
    )

    metadata = CollectionMetadata(
        source="ros2_env_collect",
        command_used=[f"which {name}" for name in DEFAULT_COMMANDS],
        warnings=warnings,
        collection_success=len(failures) == 0,
    )
    snapshot = EnvironmentSnapshot(
        metadata=metadata,
        os_name=os_name,
        os_version=os_version,
        ros_distro=ros_distro,
        expected_ros_distro=expected_ros_distro,
        rmw_implementation=rmw_implementation,
        setup_bash_path=setup_path,
        setup_bash_exists=setup_exists,
        workspace_path=workspace_path,
        commands=command_statuses,
        underlay_paths=underlay_paths,
        overlay_paths=overlay_paths,
        failures=failures,
        repair_hints=repair_hints,
    )
    return snapshot_to_dict(snapshot)
