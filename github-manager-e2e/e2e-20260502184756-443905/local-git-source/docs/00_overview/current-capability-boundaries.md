# ROS2-Agent 当前能力边界（Hermes 对齐阶段）

最后更新：2026-05-01
阶段状态：阶段 F 完成，后续 TUI / validation / bootstrap / docs / requirements 补充增强已完成收口

## 1. 当前已 live / repository-validated 的能力
- unified command runtime shared by CLI and TUI
- foundation command surface:
  - help
  - status
  - doctor
  - inspect
  - history
  - workflow
  - report
  - settings
  - runbook list
  - profile install / profile verify
  - logs deployment
- ROS2 command surface:
  - collect env / workspace / graph / tf / controller
  - diagnose env / workspace / runtime / tf / controller / fusion
  - inspect workspace / graph / tf / controller
  - doctor ros2 / workspace / tf / control
  - suggest-fix runtime / tf / controller
  - trace failure
  - replay evidence / workflow
  - compare snapshots
- workflow / recovery benchmark assets
- launcher / TUI workbench with summary / next_actions / payload / raw views
- TUI command search (`/`)
- TUI recent history panel (`R`)
- TUI recent errors panel (`E`)
- repository-local script entry `python3 tools/cli.py ...`
- layered CLI/TUI validation pipeline
- post-install read-only smoke validation

## 2. 当前能做到什么
- 用户可以从 `/home/hanhan/Desktop/.ros2-agent/ros2-agent` 直接进入终端工作台
- 在 TUI 中选择命令、执行命令、搜索命令、查看最近历史/错误、查看结构化结果与下一步建议
- 在 CLI 中以统一命令面调用基础命令和 ROS2 专项命令
- 对环境、workspace、runtime graph、tf、controller 问题给出结构化诊断结果
- 用 runbook / replay / benchmark 资产做教学复演与案例回放
- 用 layered validation / phase2 validation / post-install validation 做低风险到中等强度的仓库验证

## 3. 当前仍不能宣称什么
- 不能宣称 runtime diagnosis 已是 production-grade field platform
- 不能宣称具备自动修复闭环
- 不能宣称 recovery benchmark 已证明生产环境恢复成功率
- 不能宣称 MCP / gateway / cron 已产品化托管
- 不能宣称当前 TUI 已具备完整 IDE 级长任务编排或全量交互式作业管理能力

## 4. 当前 maturity 解释
- repository-validated：仓库内测试、docs、validation pipeline 已覆盖
- implemented prototype：可在真实 ROS2 环境中提供最小到中等强度的 runtime collection / diagnosis / workbench experience
- demo：需要外部部署或人工配合验证的展示级能力，例如 gateway/cron workflow assets
- readiness：未来接口面已定义，资产已存在，但还不是生产托管服务，例如 MCP schemas/contracts
