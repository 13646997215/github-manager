# Runtime Tooling Direction

ROS2-Agent should eventually extend beyond environment/workspace/build/launch into runtime-aware tooling.

## Planned runtime directions
- graph snapshot summaries
- topic inventory summaries
- node health summaries
- TF / QoS / controller-oriented structured outputs

## Current repository step
The repository now includes `tools/ros2_runtime_samples.py` as a structured output prototype for future runtime tools.

## Why this matters
A serious ROS2 platform must eventually help users reason about what is running, not only what failed before runtime.


## Newly implemented prototype runtime tools
- `tools/ros2_graph_inspect.py`
- `tools/ros2_controller_diagnose.py`
- `tools/ros2_tf_diagnose.py`

These tools keep the repository on a path from runtime samples toward real structured runtime diagnostics.
