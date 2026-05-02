# Capability Contract

最后更新：2026-04-30

## 核心能力

### ros2_env_collect
- maturity: implemented prototype
- inputs: current shell / env vars / command availability
- outputs: EnvironmentSnapshot
- risk_level: read_only
- validation: tests/collectors/test_ros2_env_collect.py

### ros2_workspace_collect
- maturity: implemented prototype
- inputs: workspace path
- outputs: WorkspaceSnapshot
- risk_level: read_only
- validation: tests/collectors/test_ros2_workspace_collect.py

### ros2_graph_collect
- maturity: implemented prototype
- inputs: ros2 CLI runtime
- outputs: nodes/topics structured snapshot
- risk_level: read_only
- validation: tests/collectors/test_ros2_graph_collect.py + tests/integration/test_ros2_graph_collect_integration.py

### ros2_tf_collect
- maturity: implemented prototype
- inputs: tf2_tools / ros2 topic list
- outputs: TfSnapshot
- risk_level: read_only
- validation: tests/collectors/test_ros2_tf_collect.py

### ros2_controller_collect
- maturity: implemented prototype
- inputs: ros2 control CLI
- outputs: ControllerSnapshot
- risk_level: read_only
- validation: tests/collectors/test_ros2_controller_collect.py

### diagnosis layer
- maturity: implemented prototype
- inputs: runtime schema / legacy build-launch summaries
- outputs: DiagnosisReport / prioritized fusion output
- risk_level: read_only to low_risk_local
- validation: tests/diagnosers/* + tests/workflows/test_diagnosis_workflows.py
