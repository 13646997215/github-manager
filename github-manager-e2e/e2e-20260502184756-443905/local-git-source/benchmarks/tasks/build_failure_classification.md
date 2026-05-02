# Benchmark Task - build_failure_classification

## Input
Fixture log:
- `benchmarks/fixtures/sample_colcon_failure.log`

## Goal
The agent/tool should:
- identify `bad_pkg` as failed package
- detect compile/dependency style root cause
- recommend a sane next action such as retrying failed packages after dependency/header investigation
