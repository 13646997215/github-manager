# Profile Bootstrap Guide

## What this bootstrap currently does

The bootstrap layer is designed to install a repository-backed ROS2-Agent Hermes profile without modifying the system ROS installation.

It provides:
- a ROS2-specialized Hermes profile scaffold
- profile-local docs and templates
- a starter workspace bootstrap path
- a verification path for repository-backed usage

## Available scripts

- `bootstrap/install_profile.sh`
  - installs the repository profile into a target Hermes profile directory
  - copies profile identity/config files
  - creates pointers to repository docs and reusable assets
  - creates an install manifest for verification
- `bootstrap/init_workspace.sh`
  - creates a minimal ROS2 workspace root with `src/`
  - adds a workspace README and `.gitignore`
  - prints recommended next-step validation commands

## Suggested usage

```bash
bash profile/ros2-agent/bootstrap/install_profile.sh
bash profile/ros2-agent/bootstrap/init_workspace.sh ~/ros2_ws
```

## Post-install verification

```bash
ls ~/.hermes/profiles/ros2-agent
cat ~/.hermes/profiles/ros2-agent/INSTALL_MANIFEST.md
```

Then validate the repository itself:

```bash
PYTHONPATH=. python3 scripts/validation/validate_repo.py
PYTHONPATH=. python3 -m pytest tests/tools tests/workflows -q
bash scripts/validation/run_full_quality_gate.sh
```

## Important note

This repository currently ships a repository-backed ROS2-Agent platform.
That means the installed Hermes profile is intentionally linked to repository assets and docs, so GitHub users can inspect, validate, and extend the platform rather than receiving an opaque black-box profile.
