---
name: ros2-workspace-diagnose
description: 识别 ROS2 workspace 结构、包清单、关键资源与基础健康状态。
version: 0.1.0
author: ROS2-Agent
license: MIT
metadata:
  hermes:
    tags: [ros2, workspace, diagnose, package, structure]
---

# ros2-workspace-diagnose

## 适用场景

- 刚接手一个新的 ROS2 workspace
- 不确定 src/build/install/log 是否健康
- 不知道 workspace 中有哪些包、资源、launch 文件
- 构建前需要先做结构化检查

## 目标

快速回答这些问题：
- 这是不是一个标准 ROS2 workspace？
- 有多少包？它们属于什么构建类型？
- 是否存在明显结构异常？
- 是否已经具备进入 colcon build 的前提？

## 推荐工作流

1. 确认环境层已基本正常。
2. 扫描 workspace 根目录。
3. 识别 `src/`、`build/`、`install/`、`log/`。
4. 扫描 `package.xml`、`CMakeLists.txt`、`setup.py`。
5. 统计 launch / config / urdf / xacro / msg / srv / action 资产。
6. 生成 workspace 健康摘要与下一步建议。

## 推荐搭配工具

优先调用：`ros2_workspace_inspect`

## 常见问题分类

- 非标准 workspace 目录
- 包清单不完整
- package.xml 与构建系统文件不匹配
- 资源目录缺失
- build/install/log 残留污染
- 缺少进入 build 的前置条件

## 验证方式

至少验证：
- `find src -name package.xml`
- `colcon list`（若可用）
- 检查关键目录是否存在

## 风险提示

- 发现结构异常时，不要立刻进入大规模 build。
- 若 workspace 与环境不匹配，应先回退到环境检查。

## 升级条件

- 结构正常 -> 进入 `ros2-colcon-build-troubleshoot` 或 launch 流程
- 结构异常严重 -> 先修复 workspace 布局或依赖声明
