# Benchmark Scoring Guide

## Why add scoring helpers

Benchmark tasks should gradually move from informal human judgment toward transparent, repeatable scoring.

## Current scoring direction

The repository now includes a lightweight scoring helper module:
- `benchmarks/scoring.py`

It currently supports:
- required-string matching
- required-key presence checks

## Intended use

These helpers are not final benchmark science.
They are the first step toward repeatable grading for:
- tool structured outputs
- transcript quality gates
- benchmark fixture expectations

## Future expansion
- weighted category scoring
- root-cause class scoring
- next-action scoring
- report completeness scoring
