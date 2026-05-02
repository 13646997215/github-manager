# AGENTS Context Template for ROS2-Agent Projects

This file defines the local project conventions ROS2-Agent should follow when working inside a ROS2 workspace.

## Workspace Assumptions

- Primary target OS: Ubuntu 22.04
- Primary ROS distro: Humble
- Prefer simulation-safe operations by default
- Verify environment before build / launch / test actions

## Working Rules

1. Detect workspace structure before acting.
2. Identify underlay / overlay sourcing order.
3. Prefer read-only diagnosis before modification.
4. After any modification, define a verification step.
5. Record durable conventions into docs or reusable assets.

## Debugging Rules

- Classify failures into environment / dependency / build / launch / runtime / graph / QoS / TF / controller categories.
- Avoid claiming success without validation.
- When output is too noisy, summarize root causes and next steps structurally.

## Safety Rules

- Do not assume access to real hardware is safe.
- Treat controller / actuator / network / system-level changes as high-risk.
- For risky steps, require explicit operator awareness and validation.

## Documentation Rules

- Save important artifacts inside the project repository.
- Keep examples, benchmarks, and scripts organized under their dedicated folders.
- Update the running development log after major platform changes.
