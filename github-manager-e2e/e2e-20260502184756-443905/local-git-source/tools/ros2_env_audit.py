"""Structured environment audit implementation for ROS2-Agent.

Phase-1 implementation scope:
- gather stable Ubuntu / ROS2 command facts
- remain read-only and safe
- provide a JSON-friendly structure for higher-level skills
"""

from __future__ import annotations

import os
import platform
import shutil
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class CommandStatus:
    name: str
    available: bool
    path: Optional[str] = None


@dataclass
class EnvAuditResult:
    success: bool
    os_name: str
    os_version: str
    ros_distro: Optional[str]
    expected_ros_distro: str
    ros_distro_matches: bool
    setup_bash_exists: bool
    commands: List[Dict[str, Any]]
    workspace_path: Optional[str]
    warnings: List[str]
    failures: List[str]
    next_actions: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


DEFAULT_COMMANDS = ["ros2", "colcon", "rosdep", "python3", "rviz2", "gazebo", "gz"]


def detect_command(name: str) -> CommandStatus:
    path = shutil.which(name)
    return CommandStatus(name=name, available=path is not None, path=path)


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


def infer_next_actions(*, ros_distro: Optional[str], expected_ros_distro: str, setup_bash_exists: bool, commands: List[CommandStatus], failures: List[str]) -> List[str]:
    actions: List[str] = []
    available = {c.name: c.available for c in commands}
    if not setup_bash_exists:
        actions.append("install_or_verify_ros_setup")
    if ros_distro != expected_ros_distro:
        actions.append("source_expected_ros_setup")
    if not available.get("colcon", False):
        actions.append("install_colcon")
    if not available.get("rosdep", False):
        actions.append("install_or_init_rosdep")
    if failures:
        actions.append("resolve_environment_failures")
    if not actions:
        actions.append("proceed_to_workspace_inspection")
    return actions


def build_env_audit_result(
    *,
    os_name: str = "Ubuntu",
    os_version: str = "22.04",
    ros_distro: Optional[str] = None,
    expected_ros_distro: str = "humble",
    setup_bash_exists: bool = False,
    commands: Optional[List[CommandStatus]] = None,
    workspace_path: Optional[str] = None,
    warnings: Optional[List[str]] = None,
    failures: Optional[List[str]] = None,
    next_actions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    result = EnvAuditResult(
        success=(failures is None or len(failures) == 0),
        os_name=os_name,
        os_version=os_version,
        ros_distro=ros_distro,
        expected_ros_distro=expected_ros_distro,
        ros_distro_matches=(ros_distro == expected_ros_distro),
        setup_bash_exists=setup_bash_exists,
        commands=[asdict(c) for c in (commands or [])],
        workspace_path=workspace_path,
        warnings=warnings or [],
        failures=failures or [],
        next_actions=next_actions or [],
    )
    return result.to_dict()


def audit_environment(workspace_path: Optional[str] = None, expected_ros_distro: str = "humble") -> Dict[str, Any]:
    os_release = read_os_release()
    os_name = os_release.get("NAME", platform.system())
    os_version = os_release.get("VERSION_ID", platform.release())
    ros_distro = os.environ.get("ROS_DISTRO")
    setup_bash_exists = Path(f"/opt/ros/{expected_ros_distro}/setup.bash").exists()
    command_statuses = [detect_command(name) for name in DEFAULT_COMMANDS]

    warnings: List[str] = []
    failures: List[str] = []

    if ros_distro is None:
        warnings.append("ROS_DISTRO is not set in current shell")
    elif ros_distro != expected_ros_distro:
        warnings.append(f"ROS_DISTRO is '{ros_distro}', expected '{expected_ros_distro}'")

    if not setup_bash_exists:
        failures.append(f"/opt/ros/{expected_ros_distro}/setup.bash not found")

    for required in ["ros2", "colcon", "python3"]:
        status = next(item for item in command_statuses if item.name == required)
        if not status.available:
            failures.append(f"required command missing: {required}")

    next_actions = infer_next_actions(
        ros_distro=ros_distro,
        expected_ros_distro=expected_ros_distro,
        setup_bash_exists=setup_bash_exists,
        commands=command_statuses,
        failures=failures,
    )

    return build_env_audit_result(
        os_name=os_name,
        os_version=os_version,
        ros_distro=ros_distro,
        expected_ros_distro=expected_ros_distro,
        setup_bash_exists=setup_bash_exists,
        commands=command_statuses,
        workspace_path=workspace_path,
        warnings=warnings,
        failures=failures,
        next_actions=next_actions,
    )
