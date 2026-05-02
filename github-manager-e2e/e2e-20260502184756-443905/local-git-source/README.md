# ROS2-Agent

ROS2-Agent 当前是一个 repository-backed、Hermes-aligned 的 ROS2 工程平台原型。

它已经具备：
- 统一命令 runtime（CLI / TUI 共用）
- Hermes 风格基础命令族
- ROS2 专项 collect / diagnose / inspect / doctor / suggest-fix / trace / replay / compare 命令面
- workflow / recovery benchmark 与 runbook 资产
- profile / install validation / MCP readiness / gateway demo 等平台层资产
- 三栏 TUI 工作台与四种结果视图（summary / next_actions / payload / raw）

请先阅读：
- docs/00_overview/quickstart.md
- docs/00_overview/current-capability-boundaries.md
- docs/01_architecture/capability_contract.md
- docs/00_overview/final-platform-capability-summary.md
- docs/03_workflows/launcher-ui-workflow.md

## 直接体验（推荐）
如果你已经使用本仓库附带的专用部署目录，请直接运行：

```bash
/home/hanhan/Desktop/.ros2-agent/ros2-agent
```

这个入口会优先使用部署目录里的 venv 与 Textual 依赖，进入高级 TUI 工作台。

## 现在可直接体验的核心能力
- 左侧命令目录：浏览基础命令、ROS2 采集、ROS2 巡检、ROS2 诊断、Workflow/Benchmark
- 中间详情区：查看命令说明、成熟度、风险级别、实际执行方式
- 右侧结果区：执行后在 summary / next_actions / payload / raw 四种视图间切换
- `/`：聚焦搜索框并过滤命令目录
- `R`：查看最近命令历史
- `E`：查看最近错误 / blocked / not_implemented 记录
- `Enter`：执行当前命令
- `Tab`：切换结果视图
- `H`：显示帮助
- `Q`：退出

## 开发验证与依赖说明
如果你是在仓库内开发/调试，而不是只使用部署入口，推荐按下面方式验证：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
PYTHONPATH=. bash scripts/validation/run_tui_layered_validation.sh
```

分层验证说明：
- layer 1：CLI contract tests，不依赖 Textual，必须通过
- layer 2：TUI smoke fallback，验证无 Textual 时的基本入口体验
- layer 3：Textual interaction tests，只有安装 `textual` 后才会真正执行，否则会 skip

如果你希望跑真实交互测试层，建议额外安装：
- `textual`
- `pytest-asyncio`

仓库内直接运行脚本入口现在也支持：
```bash
python3 tools/cli.py --smoke-ui
python3 tools/cli.py --no-ui history
python3 tools/cli.py --no-ui quality
```

## 常用命令
```bash
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui help
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui status
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui doctor
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui inspect workspace
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui collect env
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui diagnose fusion
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui suggest-fix tf
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui trace failure
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui runbook list
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui quality
```

## 平台边界说明
不要把当前仓库误解为 production-ready 现场恢复平台；更准确的定位是：

- 它已经是一个具备统一命令系统、结构化诊断结果层、repo-backed 评测资产和终端工作台体验的 ROS2 工程平台原型
- runtime diagnosis 在真实 ROS2 环境中仍属于 implemented prototype
- recovery benchmark / MCP / gateway / cron 仍分别属于 prototype / readiness / demo 级别，不应夸大为 production automation

## 从哪里开始使用
1. 先运行 `/home/hanhan/Desktop/.ros2-agent/ros2-agent`
2. 先看 `help` / `status` / `doctor`
3. 再进入 `inspect workspace`、`collect env`、`diagnose fusion`
4. 如果你想复演案例，再看 `runbook list` 和 `replay workflow`
