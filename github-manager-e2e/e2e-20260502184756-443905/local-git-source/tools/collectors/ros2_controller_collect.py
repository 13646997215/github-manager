"""ros2_control collector for ROS2-Agent phase-1."""

from __future__ import annotations

import shutil
import subprocess
from typing import Dict, List, Optional

from tools.schemas.runtime_schema import (
    CollectionMetadata,
    ControllerSnapshot,
    ControllerStateSnapshot,
    snapshot_to_dict,
)


def ros2_control_available() -> bool:
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


def parse_controller_states(raw_output: Optional[str]) -> List[Dict[str, object]]:
    if not raw_output:
        return []
    results: List[Dict[str, object]] = []
    for line in raw_output.splitlines():
        parts = line.split()
        if len(parts) < 4:
            continue
        name, state, claimed_interfaces, required_interfaces = parts[:4]
        results.append(
            snapshot_to_dict(
                ControllerStateSnapshot(
                    name=name,
                    state=state,
                    claimed_interfaces=int(claimed_interfaces),
                    required_interfaces=int(required_interfaces),
                )
            )
        )
    return results


def parse_hardware_interfaces(raw_output: Optional[str]) -> List[str]:
    if not raw_output:
        return []
    return [line.strip() for line in raw_output.splitlines() if line.strip()]


def collect_controllers(cli_outputs: Optional[Dict[str, Optional[str]]] = None) -> Dict[str, object]:
    warnings: List[str] = []
    controllers_output = run_cli("ros2 control list_controllers", cli_outputs=cli_outputs)
    interfaces_output = run_cli("ros2 control list_hardware_interfaces", cli_outputs=cli_outputs)

    if controllers_output is None:
        warnings.append("ros2 control list_controllers unavailable or failed")
    if interfaces_output is None:
        warnings.append("ros2 control list_hardware_interfaces unavailable or failed")

    metadata = CollectionMetadata(
        source="ros2_controller_collect",
        command_used=["ros2 control list_controllers", "ros2 control list_hardware_interfaces"],
        warnings=warnings,
        collection_success=len(warnings) == 0,
    )
    snapshot = ControllerSnapshot(
        metadata=metadata,
        controller_manager_available=controllers_output is not None,
        controllers=[ControllerStateSnapshot(**item) for item in parse_controller_states(controllers_output)],
        hardware_interfaces=parse_hardware_interfaces(interfaces_output),
    )
    return snapshot_to_dict(snapshot)
