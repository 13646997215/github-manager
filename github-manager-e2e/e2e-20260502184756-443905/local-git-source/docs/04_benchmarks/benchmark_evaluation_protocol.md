# Benchmark Evaluation Protocol

最后更新：2026-04-30

本协议现明确分为三层：
- offline reasoning benchmark
- workflow benchmark
- recovery benchmark

关键原则：
- 不把 fixture 命中率误写成现场恢复率
- workflow benchmark 用于验证 collector + diagnoser + fusion 的多步行为
- recovery benchmark 用于验证建议动作是否帮助恢复

详见：
- docs/04_benchmarks/benchmark-taxonomy.md
- docs/04_benchmarks/recovery-benchmark-design.md


## Goal
Define how ROS2-Agent benchmark tasks should be evaluated consistently.

## Evaluation dimensions
- factual extraction
- root-cause classification
- next-action quality
- teaching clarity where applicable

## Evidence policy
Every new expert claim should ideally map to at least one of:
- fixture
- benchmark task
- transcript
- automated test
