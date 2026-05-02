# ROS2-Agent CAPABILITIES

当前 profile 绑定的 repo-backed、Hermes-aligned 能力：
- 统一 command runtime（CLI / TUI 共用）
- 基础命令族：help / status / doctor / inspect / history / workflow / report / settings
- ROS2 专项命令族：collect / diagnose / inspect / doctor / suggest-fix / trace / replay / compare
- workflow / recovery benchmark assets
- validation / reporting pipelines
- 三栏 TUI 工作台与四种结果视图（summary / next_actions / payload / raw）

重要提醒：
- 当前仍是 repository-backed platform surface
- 并非所有能力都已 production-ready
- runtime diagnosis in real ROS2 environments 仍属于 implemented prototype
- gateway / cron / MCP 资产仍应按 demo/readiness 边界理解
- 请结合 docs/01_architecture/capability_contract.md 与 docs/00_overview/current-capability-boundaries.md 一起阅读
