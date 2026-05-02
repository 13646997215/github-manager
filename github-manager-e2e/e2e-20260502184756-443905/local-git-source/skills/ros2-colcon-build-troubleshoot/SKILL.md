---
name: ros2-colcon-build-troubleshoot
description: 对 colcon build 失败结果做按包聚合、错误分类与修复建议。
version: 0.1.0
author: ROS2-Agent
license: MIT
metadata:
  hermes:
    tags: [ros2, colcon, build, troubleshoot, humble]
---

# ros2-colcon-build-troubleshoot

## 适用场景

- `colcon build` 失败
- 只知道构建挂了，但不知道根因
- 想把长日志转为可执行的修复步骤

## 目标

将 noisy build log 转换为：
- 失败包列表
- 每个失败包的错误类别
- 根因候选
- 修复优先级
- 最小验证动作

## 推荐工作流

1. 确认环境层和 workspace 层基本可用。
2. 收集 build 日志或执行受控 build。
3. 按失败包聚合信息。
4. 将错误分类为环境 / 依赖 / 元数据 / CMake / 编译 / Python / 接口生成 / 链接 / overlay 等类型。
5. 输出建议修复动作与重试路径。

## 推荐搭配工具

优先调用：`colcon_build_summary`

必要时回退复用：
- `ros2_env_audit`
- `ros2_workspace_inspect`

## 典型错误类型

- dependency
- package metadata
- cmake/configure
- compile/cpp
- python packaging
- interface generation
- linking
- overlay contamination
- environment

## 验证方式

- 指定包级别重新构建
- 需要时清理 build/install/log 后重试
- 检查失败包是否减少

## 风险提示

- 不要被第一条报错迷惑，优先定位第一个根因包。
- 不要无脑全清理，先判断是否真的需要清空构建残留。

## 升级条件

- 构建通过 -> 进入 `ros2-launch-debug` 或仿真启动流程
- 构建根因不清 -> 回退环境与 workspace 诊断
