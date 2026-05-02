# Final Platform Capability Summary

最后更新：2026-05-01

## 当前已经 live / 可运行
- unified command runtime shared by CLI and TUI
- Hermes-style foundation commands
- ROS2-specific collect / diagnose / inspect / doctor / suggest-fix / trace / replay / compare commands
- workflow / recovery benchmark assets + runbooks + replay/evidence entry points
- registry / capability contract / skill manifest pipeline / post-install validation / MCP readiness assets / gateway demo pipeline
- `ros2-agent` launcher with three-pane TUI workbench and four result views: summary / next_actions / payload / raw
- TUI command search (`/`), recent history (`R`), recent errors (`E`)
- repository-local script entry `python3 tools/cli.py ...`
- layered CLI/TUI validation pipeline
- deployment entry `/home/hanhan/Desktop/.ros2-agent/ros2-agent`

## 当前仍是 prototype / demo / readiness
- runtime diagnosis in real ROS2 environments is still implemented prototype, not a production-grade field platform
- recovery benchmark remains protocol-first with representative cases, not a production recovery scoreboard
- MCP assets are readiness artifacts, not a production MCP server
- gateway / cron assets are demo-level workflows, not managed production automation
- Textual real interaction test layer is environment-dependent: ready when `textual` is installed, skipped otherwise
- post-install validation currently focuses on safe read-only smoke checks, not deep runtime verification

## 推荐的用户起点
1. `/home/hanhan/Desktop/.ros2-agent/ros2-agent`
2. `help`
3. `status`
4. `doctor`
5. `inspect workspace`
6. `diagnose fusion`
7. `runbook list` / `replay workflow`
8. For repository validation: `PYTHONPATH=. bash scripts/validation/run_tui_layered_validation.sh`
