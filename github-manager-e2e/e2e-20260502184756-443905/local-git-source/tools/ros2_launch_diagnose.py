"""Structured launch diagnosis implementation for ROS2-Agent."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class LaunchTarget:
    package_name: Optional[str]
    launch_file: Optional[str]
    resolved_path: Optional[str]


@dataclass
class LaunchDiagnosisResult:
    success: bool
    target: Dict[str, Any]
    package_found: bool
    package_prefix: Optional[str]
    missing_executables: List[str]
    params_files_status: List[Dict[str, Any]]
    referenced_assets_status: List[Dict[str, Any]]
    runtime_probe_executed: bool
    runtime_return_code: Optional[int]
    root_cause_candidates: List[str]
    escalation_hints: List[str]
    next_actions: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def build_launch_diagnosis_result(
    *,
    package_name: Optional[str],
    launch_file: Optional[str],
    resolved_path: Optional[str],
    package_found: bool,
    package_prefix: Optional[str],
    missing_executables: Optional[List[str]] = None,
    params_files_status: Optional[List[Dict[str, Any]]] = None,
    referenced_assets_status: Optional[List[Dict[str, Any]]] = None,
    runtime_probe_executed: bool = False,
    runtime_return_code: Optional[int] = None,
    root_cause_candidates: Optional[List[str]] = None,
    escalation_hints: Optional[List[str]] = None,
    next_actions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    result = LaunchDiagnosisResult(
        success=(package_found and (runtime_return_code in (None, 0))),
        target=asdict(LaunchTarget(package_name, launch_file, resolved_path)),
        package_found=package_found,
        package_prefix=package_prefix,
        missing_executables=missing_executables or [],
        params_files_status=params_files_status or [],
        referenced_assets_status=referenced_assets_status or [],
        runtime_probe_executed=runtime_probe_executed,
        runtime_return_code=runtime_return_code,
        root_cause_candidates=root_cause_candidates or [],
        escalation_hints=escalation_hints or [],
        next_actions=next_actions or [],
    )
    return result.to_dict()


def _status_for_paths(paths: List[str]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for raw in paths:
        path = Path(raw).expanduser().resolve()
        items.append({"path": str(path), "exists": path.exists()})
    return items


def diagnose_launch(
    *,
    package_name: Optional[str],
    launch_file: Optional[str],
    package_prefix: Optional[str] = None,
    params_files: Optional[List[str]] = None,
    referenced_assets: Optional[List[str]] = None,
    expected_executables: Optional[List[str]] = None,
    runtime_return_code: Optional[int] = None,
) -> Dict[str, Any]:
    resolved_path: Optional[str] = None
    launch_path_exists = False
    package_found = False
    root_cause_candidates: List[str] = []
    escalation_hints: List[str] = []
    next_actions: List[str] = []

    if package_prefix:
        prefix_path = Path(package_prefix).expanduser().resolve()
        package_found = prefix_path.exists()
    else:
        prefix_path = None

    if package_prefix and launch_file and package_name:
        candidate = prefix_path / "share" / package_name / "launch" / launch_file if prefix_path else None
        if candidate and candidate.exists():
            resolved_path = str(candidate)
            launch_path_exists = True
        else:
            root_cause_candidates.append("launch_file_missing")
            next_actions.append("verify_launch_file_path")
    elif launch_file:
        candidate = Path(launch_file).expanduser().resolve()
        if candidate.exists():
            resolved_path = str(candidate)
            launch_path_exists = True
        else:
            root_cause_candidates.append("launch_file_missing")
            next_actions.append("verify_launch_file_path")

    params_status = _status_for_paths(params_files or [])
    asset_status = _status_for_paths(referenced_assets or [])

    if any(not item["exists"] for item in params_status):
        root_cause_candidates.append("params_file_missing")
        next_actions.append("fix_params_path")

    if any(not item["exists"] for item in asset_status):
        root_cause_candidates.append("referenced_asset_missing")
        escalation_hints.append("maybe_gazebo_or_urdf")
        next_actions.append("verify_referenced_assets")

    missing_executables = expected_executables or []
    if missing_executables:
        root_cause_candidates.append("executable_missing")
        next_actions.append("verify_install_targets")

    if package_prefix and not package_found:
        root_cause_candidates.append("package_not_found")
        next_actions.append("verify_package_installation")

    if runtime_return_code not in (None, 0):
        root_cause_candidates.append("runtime_probe_failed")
        escalation_hints.append("inspect_runtime_logs")
        next_actions.append("collect_runtime_logs")

    if not next_actions and package_found and launch_path_exists:
        next_actions.append("execute_minimal_launch_probe")

    return build_launch_diagnosis_result(
        package_name=package_name,
        launch_file=launch_file,
        resolved_path=resolved_path,
        package_found=package_found,
        package_prefix=package_prefix,
        missing_executables=missing_executables,
        params_files_status=params_status,
        referenced_assets_status=asset_status,
        runtime_probe_executed=(runtime_return_code is not None),
        runtime_return_code=runtime_return_code,
        root_cause_candidates=root_cause_candidates,
        escalation_hints=escalation_hints,
        next_actions=next_actions,
    )
