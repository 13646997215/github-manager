# Benchmark Task - launch_runtime_failure_hint

## Input
Fixture:
- `benchmarks/fixtures/launch_runtime_failure_hint`

## Goal
The tool/agent should:
- resolve launch path
- detect structurally valid launch assets
- when runtime_return_code is non-zero, classify runtime_probe_failed
- recommend collecting runtime logs
