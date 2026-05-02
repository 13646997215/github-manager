# 核心工作流设计

## 1. 环境审计工作流
- 检查 Ubuntu 版本
- 检查 ROS2 distro
- 检查 underlay / overlay
- 检查关键命令可用性
- 生成结构化审计结果

## 2. Workspace 诊断工作流
- 识别 src / build / install / log
- 查找 package.xml / setup.py / CMakeLists.txt
- 检查依赖缺失
- 输出 workspace 健康摘要

## 3. Build 排障工作流
- 收集 colcon build 输出
- 按包聚合失败点
- 分类为依赖、编译、配置、接口、环境问题
- 输出修复建议与验证步骤

## 4. Launch / Simulation 调试工作流
- 检查 launch 文件入口
- 检查依赖节点
- 检查 Gazebo / RViz / TF / controller 状态
- 输出根因候选与建议动作

## 5. 回归与报告工作流
- 定时执行 smoke test
- 收集结果
- 汇总异常
- 输出结构化日报 / 周报
