# Bootstrap Workflow

## Goal
Provide a repository-backed path from clone -> profile install -> workspace bootstrap -> repository validation.

## 1. Install the profile
```bash
bash profile/ros2-agent/bootstrap/install_profile.sh
```

## 2. Inspect installed manifest
```bash
cat ~/.hermes/profiles/ros2-agent/INSTALL_MANIFEST.md
```

## 3. Prepare a starter workspace
```bash
bash profile/ros2-agent/bootstrap/init_workspace.sh ~/ros2_ws
```

## 4. Validate repository assets
```bash
PYTHONPATH=. python3 scripts/validation/validate_repo.py
PYTHONPATH=. python3 -m pytest tests/tools tests/workflows -q
bash scripts/validation/run_full_quality_gate.sh
```

## Purpose
This bootstrap path intentionally avoids modifying system ROS installation automatically.
It gives contributors and future users a reproducible starting point plus a clear verification path.
