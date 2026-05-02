"""Structured ros2_control/controller-manager style diagnosis helpers."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class ControllerState:
    name: str
    state: str
    claimed_interfaces: int
    required_interfaces: int = 0


@dataclass
class ControllerDiagnosisResult:
    success: bool
    controllers: List[Dict[str, Any]]
    root_cause_candidates: List[str]
    warnings: List[str]
    next_actions: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def diagnose_controllers(controllers: List[ControllerState]) -> Dict[str, Any]:
    root_causes: List[str] = []
    warnings: List[str] = []
    next_actions: List[str] = []

    for controller in controllers:
        if controller.state in {"inactive", "unconfigured", "failed"}:
            warnings.append(f"controller_not_active:{controller.name}")
            root_causes.append("controller_activation_failure")
            if "inspect_controller_manager_logs" not in next_actions:
                next_actions.append("inspect_controller_manager_logs")
        if controller.required_interfaces > controller.claimed_interfaces:
            warnings.append(f"interfaces_not_fully_claimed:{controller.name}")
            root_causes.append("hardware_interface_export_issue")
            if "verify_hardware_interface_exports" not in next_actions:
                next_actions.append("verify_hardware_interface_exports")

    success = len(warnings) == 0
    if success:
        next_actions.append("continue_motion_validation")

    return ControllerDiagnosisResult(
        success=success,
        controllers=[asdict(c) for c in controllers],
        root_cause_candidates=sorted(set(root_causes)),
        warnings=warnings,
        next_actions=next_actions,
    ).to_dict()
