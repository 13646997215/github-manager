---
name: ros2-runtime-debug-teaching
description: Teach users how to reason about ROS2 runtime graph, controller, TF, and QoS failures step by step.
version: 1.0.0
---

# ROS2 Runtime Debug Teaching

## When to use
Use this skill when the system launches but still does not behave correctly.

## Teaching goals
- distinguish build-time, launch-time, and runtime failures
- identify whether data flow, TF, controller, or QoS is the main bottleneck
- teach how to move from symptoms to structured root-cause candidates

## Core teaching flow
1. Ask what is running versus what is merely built.
2. Check graph facts: nodes, topics, publishers, subscribers.
3. Check controllers and claimed interfaces.
4. Check TF freshness and critical chains.
5. Explain why the observed symptom follows from the missing runtime condition.
6. Give next actions in the smallest safe order.
