# Tools Contribution Guide

Structured tools in this repository should:
- expose stable JSON-friendly outputs
- prefer explicit field names
- encode errors and warnings clearly
- avoid dangerous side effects by default
- remain testable with small pytest cases

Phase-1 priority tools:
- ros2_env_audit
- ros2_workspace_inspect
- colcon_build_summary
- ros2_launch_diagnose
