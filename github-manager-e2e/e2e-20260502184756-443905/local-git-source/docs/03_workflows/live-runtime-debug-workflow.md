# Live Runtime Debug Workflow（Phase-1）

最后更新：2026-04-30
适用阶段：Phase-1 foundation

## 1. 目标

这个工作流的目标不是直接自动修复 ROS2 现场问题，而是：
1. 从真实环境采集最小可信证据
2. 把证据归一化为统一 runtime schema
3. 为 phase-2 diagnosis、phase-3 benchmark、phase-4 platform surface 提供稳定输入

## 2. Phase-1 推荐步骤

### Step 1：收集环境证据
运行 `tools/collectors/ros2_env_collect.py` 对应入口逻辑，确认：
- ROS_DISTRO
- RMW_IMPLEMENTATION
- setup.bash 可用性
- 核心命令可用性
- underlay / overlay 路径

### Step 2：收集 workspace 证据
运行 `tools/collectors/ros2_workspace_collect.py`，确认：
- workspace 是否像 ROS2 workspace
- package 数量与 build type
- launch/config/urdf/xacro 资产
- install/build/log 状态
- package metadata 问题

### Step 3：收集 runtime graph 证据
运行 `tools/collectors/ros2_graph_collect.py`，确认：
- node list
- topic list
- topic info verbose
- 关键 topic 基础分类
- 运行图采集是否 degraded

### Step 4：收集 TF 证据
运行 `tools/collectors/ros2_tf_collect.py`，确认：
- frame_count
- missing_chains
- frame_authorities
- /clock 是否存在

### Step 5：收集 ros2_control 证据
运行 `tools/collectors/ros2_controller_collect.py`，确认：
- controller manager 是否可见
- controllers 状态
- hardware interfaces

### Step 6：进入 compat/fusion 层
- `tools/diagnosers/compat_adapters.py`
- `tools/diagnosers/fusion_diagnoser.py`

注意：在 phase-1，这一步只适合做“证据组织与最小优先级尝试”，不应宣称为完整诊断结论。

## 3. 输出预期

每个 collector 应输出：
- `metadata.source`
- `metadata.collected_at`
- `metadata.command_used`
- `metadata.warnings`
- `metadata.collection_success`

这些输出统一进入 `tools/schemas/runtime_schema.py` 定义的 snapshot/bundle 结构。

## 4. Phase-1 限制
- integration-lite only
- no recovery loop
- no production automation
- no full launch/log collection yet
- no confidence/risk schema yet

## 5. 使用建议
- 先证据采集，再推理
- 先接受 degraded / skipped truth，再决定下一步
- 不把 phase-1 skeleton 当 production diagnosis engine
