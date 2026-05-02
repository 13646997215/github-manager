---
name: ros2-launch-reasoning-coach
description: Teach users how to reason from ROS2 launch symptoms to missing assets, params, executables, and runtime probes.
version: 1.0.0
---

# ROS2 Launch Reasoning Coach

## Core idea
A successful `ros2 launch` command is not the same as a healthy runtime.

## Teaching checklist
1. Is the package actually installed?
2. Is the launch file resolved from the expected prefix?
3. Are params files present?
4. Are referenced assets present?
5. Did the runtime probe still fail after static checks passed?
6. What is the smallest next check that narrows uncertainty?
