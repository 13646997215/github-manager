"""Workspace structure collector for ROS2-Agent phase-1."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List
import xml.etree.ElementTree as ET

from tools.schemas.runtime_schema import (
    CollectionMetadata,
    WorkspacePackageSnapshot,
    WorkspaceSnapshot,
    snapshot_to_dict,
)


BUILD_FILE_PATTERNS = ("setup.py", "CMakeLists.txt")


def infer_build_type(package_dir: Path) -> str:
    if (package_dir / "setup.py").exists():
        return "ament_python"
    if (package_dir / "CMakeLists.txt").exists():
        return "ament_cmake"
    return "unknown"


def parse_package_name(package_xml: Path) -> str:
    try:
        root = ET.fromstring(package_xml.read_text(encoding="utf-8"))
        node = root.find("name")
        if node is not None and node.text:
            return node.text.strip()
    except ET.ParseError:
        return package_xml.parent.name
    return package_xml.parent.name


def collect_files(root: Path, patterns: List[str]) -> List[str]:
    results: List[str] = []
    for pattern in patterns:
        for path in root.rglob(pattern):
            if path.is_file():
                results.append(str(path))
    return sorted(set(results))


def package_has_build_file(package_dir: Path) -> bool:
    return any((package_dir / pattern).exists() for pattern in BUILD_FILE_PATTERNS)


def collect_workspace(workspace_root: str) -> Dict[str, object]:
    root = Path(workspace_root).expanduser().resolve()
    src_dir = root / "src"

    warnings: List[str] = []
    metadata_issues: List[str] = []
    looks_like_ros2_workspace = root.exists() and src_dir.exists() and src_dir.is_dir()

    if not root.exists():
        warnings.append("workspace root does not exist")
    if root.exists() and not src_dir.exists():
        warnings.append("src directory missing")

    packages: List[WorkspacePackageSnapshot] = []
    if src_dir.exists():
        for package_xml in sorted(src_dir.rglob("package.xml")):
            package_dir = package_xml.parent
            package_name = parse_package_name(package_xml)
            build_type = infer_build_type(package_dir)
            has_cmakelists = (package_dir / "CMakeLists.txt").exists()
            has_setup_py = (package_dir / "setup.py").exists()
            packages.append(
                WorkspacePackageSnapshot(
                    name=package_name,
                    path=str(package_dir),
                    build_type=build_type,
                    has_package_xml=True,
                    has_cmakelists=has_cmakelists,
                    has_setup_py=has_setup_py,
                )
            )
            if not package_has_build_file(package_dir):
                metadata_issues.append(f"package_missing_build_file:{package_name}")

    if looks_like_ros2_workspace and not packages:
        metadata_issues.append("workspace_has_src_but_no_package_xml")

    recommended_next_step = "build_workspace"
    if not looks_like_ros2_workspace or metadata_issues:
        recommended_next_step = "repair_workspace"

    metadata = CollectionMetadata(
        source="ros2_workspace_collect",
        command_used=[f"scan workspace {root}"],
        warnings=warnings,
        collection_success=root.exists(),
    )
    snapshot = WorkspaceSnapshot(
        metadata=metadata,
        workspace_root=str(root),
        looks_like_ros2_workspace=looks_like_ros2_workspace,
        package_count=len(packages),
        packages=packages,
        launch_files=collect_files(root, ["*.launch.py", "*.launch.xml"]),
        config_files=collect_files(root, ["*.yaml", "*.yml"]),
        urdf_files=collect_files(root, ["*.urdf"]),
        xacro_files=collect_files(root, ["*.xacro"]),
        install_dir_exists=(root / "install").exists(),
        build_dir_exists=(root / "build").exists(),
        log_dir_exists=(root / "log").exists(),
        metadata_issues=metadata_issues,
        recommended_next_step=recommended_next_step,
    )
    return snapshot_to_dict(snapshot)
