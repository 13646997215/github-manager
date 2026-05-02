# ROS2-Agent 架构总览

## 1. 分层架构

ROS2-Agent 采用五层结构：

1. Foundation Layer
   - Hermes Agent runtime
   - tools / sessions / memory / skills / cron / gateway / delegation / MCP

2. Domain Intelligence Layer
   - ROS2 专家 persona
   - 教学与引导策略
   - 安全边界
   - 项目上下文约束

3. Workflow Layer
   - 环境搭建
   - workspace 管理
   - build / launch / debug
   - simulation / regression / reporting

4. Structured Tools Layer
   - env audit
   - workspace inspect
   - build summary
   - graph snapshot
   - launch diagnose
   - health checks

5. Collaboration Layer
   - examples
   - benchmarks
   - gateway
   - cron
   - GitHub-facing docs and contribution workflows

## 2. 设计原则

- 先用技能沉淀专家流程，再把高频能力工具化。
- 结构化输出优于裸终端噪声。
- 仿真安全场景与真机场景必须严格分层。
- 长期迭代必须依赖持续日志与规划文档。

## 3. 目标成果

最终平台应具备：
- 可发布 profile 模板
- 可复用 skill 体系
- 可测试的工具脚本
- 可演示的示例案例
- 可度量的 benchmark 任务集
- 可持续演进的文档与贡献体系
