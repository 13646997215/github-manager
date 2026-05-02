# Hermes Integration Contract

## Purpose
Clarify how ROS2-Agent should be understood and used as a repository-backed Hermes expert platform.

## Current integration model
ROS2-Agent currently uses a repository-backed integration pattern:
- a Hermes profile scaffold is installable under `profile/ros2-agent/`
- the installed profile points users back to repository assets
- skills, tools, fixtures, transcripts, and validation pipelines remain transparent and versioned inside the repository

## Why repository-backed
This project is not trying to hide expertise inside an opaque black-box profile.
It is intentionally built so users can inspect:
- profile identity and policy
- skills and workflows
- tools and structured outputs
- benchmarks and scoring
- examples and transcripts
- validation and quality gates

## Current contract boundaries
### install_profile.sh guarantees
- installs profile identity/config template files
- records repository root
- creates an install manifest
- creates a verifiable starting point for Hermes profile usage

### install_profile.sh does not yet guarantee
- automatic profile-local installation of all repo skills into Hermes global skill storage
- automatic runtime tool registration inside Hermes core
- automatic MCP server installation
- automatic gateway/cron deployment

## User-facing expectation
Users should understand ROS2-Agent today as:
- an installable Hermes profile scaffold
- a repository-native ROS2 expert platform
- a transparent toolkit and benchmarked knowledge base
- a strong base for future deeper Hermes-native packaging

## Planned future evolution
- richer profile-local skill discovery strategy
- MCP-based ROS2 diagnostic service surface
- cron/gateway-ready recurring report flows
- stronger end-to-end Hermes runtime demos
