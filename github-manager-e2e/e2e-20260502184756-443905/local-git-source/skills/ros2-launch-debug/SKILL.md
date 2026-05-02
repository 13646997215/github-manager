---
name: ros2-launch-debug
description: 对 ros2 launch 失败或启动异常进行入口、资源、节点与日志级诊断。
version: 0.1.0
author: ROS2-Agent
license: MIT
metadata:
  hermes:
    tags: [ros2, launch, debug, simulation, runtime]
---

# ros2-launch-debug

## 适用场景

- `ros2 launch` 直接报错
- launch 能启动但关键节点崩溃或退出
- 找不到 package、launch 文件、参数文件、资源文件或可执行节点

## 目标

把 launch 层故障分解为：
- launch 入口问题
- package / executable 定位问题
- 参数与资源文件问题
- 运行初期失败信号
- 是否需要升级到 Gazebo / TF / controller 专题调试

## 推荐工作流

1. 确认环境与 workspace、build 状态基本正常。
2. 确认 launch 文件路径与 package 解析状态。
3. 检查参数文件、URDF/Xacro 与资源引用。
4. 检查关键 executable 是否存在。
5. 结合最小化 runtime probe 生成根因候选。
6. 输出下一步建议与升级方向。

## 推荐搭配工具

优先调用：`ros2_launch_diagnose`

必要时复用：
- `ros2_workspace_inspect`
- `ros2_env_audit`

## 常见问题分类

- package not found
- launch file not found
- executable not installed
- params yaml invalid or missing
- xacro / urdf generation failure
- runtime early exit
- simulation dependency not ready

## 验证方式

- 最小化 launch 复现
- 单节点验证
- 资源路径验证
- package prefix / executable 枚举检查

## 风险提示

- launch 失败不等于 Gazebo/TF/controller 深层问题，先检查入口层。
- 若是运行时长链路问题，升级到后续专题技能，不要在总入口 skill 中硬撑所有子问题。

## 升级条件

- 若显示仿真后端问题 -> 后续进入 gazebo 专项 skill
- 若显示图谱/坐标问题 -> 后续进入 tf/qos/network 专项 skill
- 若显示控制器问题 -> 后续进入 controller 专项 skill
