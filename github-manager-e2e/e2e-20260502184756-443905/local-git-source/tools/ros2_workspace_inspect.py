"""Structured workspace inspection implementation for ROS2-Agent."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional
import xml.etree.ElementTree as ET


@dataclass
class PackageInfo:
    name: str
    path: str
    build_type: str
    has_package_xml: bool
    has_cmakelists: bool
    has_setup_py: bool


@dataclass
class WorkspaceInspectResult:
    success: bool
    workspace_root: str
    looks_like_ros2_workspace: bool
    package_count: int
    packages: List[Dict[str, Any]]
    launch_files: List[str]
    config_files: List[str]
    urdf_files: List[str]
    xacro_files: List[str]
    warnings: List[str]
    recommended_next_step: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def infer_build_type(package_dir: Path) -> str:
    if (package_dir / "setup.py").exists():
        return "ament_python"
    if (package_dir / "CMakeLists.txt").exists():
        return "ament_cmake"
    return "unknown"


def parse_package_name(package_xml: Path) -> str:
    try:
        root = ET.fromstring(package_xml.read_text(encoding="utf-8"))
        name_node = root.find("name")
        if name_node is not None and name_node.text:
            return name_node.text.strip()
    except ET.ParseError:
        pass
    return package_xml.parent.name


def collect_files(root: Path, patterns: List[str]) -> List[str]:
    results: List[str] = []
    for pattern in patterns:
        for path in root.rglob(pattern):
            if path.is_file():
                results.append(str(path))
    return sorted(set(results))


def build_workspace_inspect_result(
    *,
    workspace_root: str,
    looks_like_ros2_workspace: bool,
    packages: Optional[List[PackageInfo]] = None,
    launch_files: Optional[List[str]] = None,
    config_files: Optional[List[str]] = None,
    urdf_files: Optional[List[str]] = None,
    xacro_files: Optional[List[str]] = None,
    warnings: Optional[List[str]] = None,
    recommended_next_step: str = "review_workspace",
) -> Dict[str, Any]:
    package_items = [asdict(p) for p in (packages or [])]
    result = WorkspaceInspectResult(
        success=True,
        workspace_root=workspace_root,
        looks_like_ros2_workspace=looks_like_ros2_workspace,
        package_count=len(package_items),
        packages=package_items,
        launch_files=launch_files or [],
        config_files=config_files or [],
        urdf_files=urdf_files or [],
        xacro_files=xacro_files or [],
        warnings=warnings or [],
        recommended_next_step=recommended_next_step,
    )
    return result.to_dict()


def inspect_workspace(workspace_root: str) -> Dict[str, Any]:
    root = Path(workspace_root).expanduser().resolve()
    src_dir = root / "src"
    warnings: List[str] = []

    looks_like_ros2_workspace = root.exists() and src_dir.exists() and src_dir.is_dir()
    if not root.exists():
        warnings.append("workspace root does not exist")
    if root.exists() and not src_dir.exists():
        warnings.append("src directory missing")

    packages: List[PackageInfo] = []
    if src_dir.exists():
        for package_xml in sorted(src_dir.rglob("package.xml")):
            package_dir = package_xml.parent
            packages.append(
                PackageInfo(
                    name=parse_package_name(package_xml),
                    path=str(package_dir),
                    build_type=infer_build_type(package_dir),
                    has_package_xml=True,
                    has_cmakelists=(package_dir / "CMakeLists.txt").exists(),
                    has_setup_py=(package_dir / "setup.py").exists(),
                )
            )

    launch_files = collect_files(root, ["*.launch.py", "*.launch.xml"])
    config_files = collect_files(root, ["*.yaml", "*.yml"])
    urdf_files = collect_files(root, ["*.urdf"])
    xacro_files = collect_files(root, ["*.xacro"])

    if looks_like_ros2_workspace and not packages:
        warnings.append("workspace has src directory but no package.xml files were found")

    recommended_next_step = "build_workspace" if looks_like_ros2_workspace and packages else "repair_workspace"

    return build_workspace_inspect_result(
        workspace_root=str(root),
        looks_like_ros2_workspace=looks_like_ros2_workspace,
        packages=packages,
        launch_files=launch_files,
        config_files=config_files,
        urdf_files=urdf_files,
        xacro_files=xacro_files,
        warnings=warnings,
        recommended_next_step=recommended_next_step,
    )
