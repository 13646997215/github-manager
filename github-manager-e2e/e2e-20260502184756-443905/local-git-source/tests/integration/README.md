# Integration-lite tests for phase-1 collectors

These tests intentionally validate only the minimum live-runtime integration path.

Principles:
- Safe to run in environments without ROS2
- Skip with explicit reasons when runtime tools are unavailable
- Do not require full simulation stacks
- Only verify that collectors execute and return structured schema output

Covered in phase-1:
- ros2_graph_collect
- ros2_tf_collect
- ros2_controller_collect

Not covered yet:
- full runtime replay
- launch probe integration
- end-to-end diagnosis workflows
