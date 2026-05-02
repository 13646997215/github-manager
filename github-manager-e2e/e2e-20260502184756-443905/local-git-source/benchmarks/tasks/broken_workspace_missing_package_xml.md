# Benchmark Task - broken_workspace_missing_package_xml

## Input
Workspace:
- `examples/broken_cases/broken_ws_missing_package_xml`

## Goal
The tool/agent should:
- identify the workspace root and src directory
- detect that no valid package.xml inventory exists
- warn that the workspace needs repair
- recommend `repair_workspace`
