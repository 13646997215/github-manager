---
name: ros2-environment-bootstrap
description: Ubuntu 22.04 + ROS2 Humble 环境检查、source 关系确认、依赖前置审计与下一步建议。
version: 0.1.0
author: ROS2-Agent
license: MIT
metadata:
  hermes:
    tags: [ros2, humble, ubuntu22.04, environment, bootstrap, audit]
---

# ros2-environment-bootstrap

## 适用场景

- 第一次进入新的 Ubuntu 22.04 / ROS2 Humble 机器
- 不确定 ROS2 环境是否正确安装或已被正确 source
- 准备开始 workspace 构建、launch、仿真前的前置检查
- 怀疑 underlay / overlay 关系混乱

## 目标

在进行任何 ROS2 构建、启动、调试前，先建立一份清晰的环境状态结论：
- 当前系统与 ROS2 版本状态
- 关键命令与依赖是否可用
- 是否已经正确 source
- 是否存在 overlay 污染风险
- 下一步应该进行什么动作

## 推荐工作流

1. 确认 Ubuntu 版本与 ROS_DISTRO。
2. 检查 `ros2`、`colcon`、`rosdep`、`python3` 等关键命令。
3. 检查 `/opt/ros/humble` 与关键环境变量。
4. 如有 workspace，识别 underlay / overlay 关系。
5. 输出结构化审计结果。
6. 根据结果决定：
   - 继续 workspace 诊断
   - 先修复环境
   - 先 source 正确环境

## 推荐搭配工具

优先调用结构化工具：`ros2_env_audit`

若工具不可用，则退化为：
- `source /opt/ros/humble/setup.bash`
- `printenv | grep ROS`
- `which ros2 colcon rosdep`
- `ls /opt/ros/humble`

## 常见问题分类

- ROS2 未安装
- 安装了但未 source
- source 了错误的 overlay
- 缺少 colcon / rosdep
- 仿真相关工具缺失（gazebo/rviz2）
- 环境变量异常导致路径污染

## 验证方式

至少验证：
- `ros2 --help`
- `colcon --help`
- `rosdep --help`
- `echo $ROS_DISTRO`

## 风险提示

- 不要在环境状态未确认前直接进行复杂 build/launch。
- 不要混用多个未知 overlay。
- 若结果显示路径污染，优先清理 shell 环境再继续。

## 升级条件

在以下情况下应升级到后续技能：
- 环境基本正常 -> `ros2-workspace-diagnose`
- 构建失败 -> `ros2-colcon-build-troubleshoot`
- 启动失败 -> `ros2-launch-debug`
