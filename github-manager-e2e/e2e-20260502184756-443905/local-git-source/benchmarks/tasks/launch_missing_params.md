# Benchmark Task - launch_missing_params

## Input
Fixture:
- `benchmarks/fixtures/launch_missing_params`

## Goal
The tool/agent should:
- resolve the launch path from the package prefix
- report package_found = true
- detect missing params file
- recommend fixing params path before deeper runtime debugging
