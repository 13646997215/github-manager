# Weighted Benchmark Scoring Plan

## Current weighted direction
The repository now includes `score_weighted_sections(...)` so multiple checks can be aggregated into a single weighted score.

## Intended use
- combine fact extraction checks
- combine next-action checks
- combine structural and semantic checks

## Example pattern
- fixture identification: 0.4
- root-cause classification: 0.3
- next-action quality: 0.3

This gives ROS2-Agent a path toward more serious benchmark grading.
