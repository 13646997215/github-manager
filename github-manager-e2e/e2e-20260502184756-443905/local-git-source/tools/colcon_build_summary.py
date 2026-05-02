"""Structured colcon build summary implementation for ROS2-Agent."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional
import re


@dataclass
class FailedPackage:
    package: str
    stage: str
    error_category: str
    headline: str
    evidence_lines: List[str]
    suggested_fix: str


@dataclass
class BuildSummaryResult:
    success: bool
    workspace_root: str
    build_executed: bool
    command: str
    return_code: int
    packages_total: int
    packages_succeeded: int
    packages_failed: int
    failed_packages: List[Dict[str, Any]]
    global_findings: List[str]
    should_retry_after_clean: bool
    should_run_rosdep: bool
    should_recheck_environment: bool
    next_actions: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


ERROR_RULES = [
    (re.compile(r"rosdep|dependency", re.IGNORECASE), "dependency", "run rosdep install and verify dependency declarations"),
    (re.compile(r"CMake Error|find_package|ament_", re.IGNORECASE), "cmake/configure", "check find_package, ament dependencies, and CMake configuration"),
    (re.compile(r"fatal error:|undefined reference|linker", re.IGNORECASE), "compile/cpp", "inspect compiler errors, include paths, and link dependencies"),
    (re.compile(r"setup.py|entry_points|ModuleNotFoundError|ImportError", re.IGNORECASE), "python packaging", "verify setup.py, package layout, and Python dependencies"),
    (re.compile(r"msg|srv|action|rosidl", re.IGNORECASE), "interface generation", "check interface files and rosidl dependency declarations"),
    (re.compile(r"overlay|AMENT_PREFIX_PATH|CMAKE_PREFIX_PATH", re.IGNORECASE), "overlay contamination", "clean overlays and verify underlay/overlay sourcing order"),
]

FAIL_RE = re.compile(r"Failed\s+<<\s+([^\s]+)")
FINISHED_RE = re.compile(r"Finished\s+<<<\s+([^\s]+)")
SUMMARY_RE = re.compile(r"Summary:\s*(\d+) packages finished")


def classify_error(text: str) -> tuple[str, str]:
    for pattern, category, suggested_fix in ERROR_RULES:
        if pattern.search(text):
            return category, suggested_fix
    return "unknown", "inspect the first failing package log and refine the root cause"


def build_colcon_summary_result(
    *,
    workspace_root: str,
    command: str,
    return_code: int,
    packages_total: int,
    packages_succeeded: int,
    failed_packages: Optional[List[FailedPackage]] = None,
    global_findings: Optional[List[str]] = None,
    should_retry_after_clean: bool = False,
    should_run_rosdep: bool = False,
    should_recheck_environment: bool = False,
    next_actions: Optional[List[str]] = None,
    build_executed: bool = True,
) -> Dict[str, Any]:
    failed_items = [asdict(p) for p in (failed_packages or [])]
    result = BuildSummaryResult(
        success=(return_code == 0 and len(failed_items) == 0),
        workspace_root=workspace_root,
        build_executed=build_executed,
        command=command,
        return_code=return_code,
        packages_total=packages_total,
        packages_succeeded=packages_succeeded,
        packages_failed=len(failed_items),
        failed_packages=failed_items,
        global_findings=global_findings or [],
        should_retry_after_clean=should_retry_after_clean,
        should_run_rosdep=should_run_rosdep,
        should_recheck_environment=should_recheck_environment,
        next_actions=next_actions or [],
    )
    return result.to_dict()


def summarize_build_log(log_text: str, workspace_root: str = ".", command: str = "colcon build", return_code: int = 1) -> Dict[str, Any]:
    lines = log_text.splitlines()
    failed_packages: List[FailedPackage] = []
    finished = FINISHED_RE.findall(log_text)
    failed = FAIL_RE.findall(log_text)

    for pkg in failed:
        evidence = [line.strip() for line in lines if pkg in line or "error" in line.lower() or "fatal" in line.lower()]
        evidence = evidence[:5] if evidence else [f"build failed for package {pkg}"]
        combined = "\n".join(evidence)
        category, suggested_fix = classify_error(combined)
        headline = evidence[0]
        failed_packages.append(
            FailedPackage(
                package=pkg,
                stage="build",
                error_category=category,
                headline=headline,
                evidence_lines=evidence,
                suggested_fix=suggested_fix,
            )
        )

    packages_total = len(set(finished + failed))
    if packages_total == 0:
        match = SUMMARY_RE.search(log_text)
        if match:
            packages_total = int(match.group(1))

    packages_succeeded = len(set(finished))
    global_findings: List[str] = []
    should_run_rosdep = any(pkg.error_category == "dependency" for pkg in failed_packages)
    should_recheck_environment = any(pkg.error_category == "overlay contamination" for pkg in failed_packages)
    should_retry_after_clean = any(pkg.error_category in {"compile/cpp", "cmake/configure", "overlay contamination"} for pkg in failed_packages)

    if failed_packages:
        global_findings.append(f"detected {len(failed_packages)} failed package(s)")
    if should_run_rosdep:
        global_findings.append("dependency-related errors detected")
    if should_recheck_environment:
        global_findings.append("environment/overlay issues may be contributing")

    next_actions: List[str] = []
    if should_run_rosdep:
        next_actions.append("run_rosdep")
    if should_recheck_environment:
        next_actions.append("recheck_environment")
    if failed_packages:
        next_actions.append("retry_failed_packages")
    elif return_code == 0:
        next_actions.append("proceed_to_launch")

    return build_colcon_summary_result(
        workspace_root=workspace_root,
        command=command,
        return_code=return_code,
        packages_total=packages_total,
        packages_succeeded=packages_succeeded,
        failed_packages=failed_packages,
        global_findings=global_findings,
        should_retry_after_clean=should_retry_after_clean,
        should_run_rosdep=should_run_rosdep,
        should_recheck_environment=should_recheck_environment,
        next_actions=next_actions,
        build_executed=False,
    )


def summarize_build_log_file(log_path: str, workspace_root: str = ".", command: str = "colcon build", return_code: int = 1) -> Dict[str, Any]:
    text = Path(log_path).read_text(encoding="utf-8")
    return summarize_build_log(text, workspace_root=workspace_root, command=command, return_code=return_code)
