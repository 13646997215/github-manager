# Benchmark Task - build_dependency_failure

## Input
Fixture log:
- `benchmarks/fixtures/sample_colcon_dependency_failure.log`

## Goal
The tool/agent should:
- identify the failed package
- classify the issue as dependency or cmake/configure related
- recommend dependency/configuration repair actions
