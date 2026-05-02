# Quickstart

## 当前项目定位
ROS2-Agent 当前是 repository-backed、Hermes-aligned 的 ROS2 工程平台原型，已经具备：
- 统一命令 runtime
- 基础命令族（help / status / doctor / inspect / history / workflow / report / settings）
- ROS2 专项命令族（collect / diagnose / inspect / doctor / suggest-fix / trace / replay / compare）
- workflow / recovery benchmark assets
- validation/report pipelines
- 三栏 TUI 工作台与四种结果视图

## 推荐开始路径（直接体验版）
1. 直接运行：
   ```bash
   /home/hanhan/Desktop/.ros2-agent/ros2-agent
   ```
2. 在左侧选择命令
3. 看中间详情区确认命令用途与风险级别
4. 按 `Enter` 执行当前命令
5. 可用 `/` 搜索命令，`R` 查看最近历史，`E` 查看最近错误
6. 在右侧用 `Tab` 切换：summary / next_actions / payload / raw
7. 按 `H` 查看帮助，按 `Q` 退出

## 开发/测试快速验证
如果你是在仓库里开发，不只是使用部署入口，推荐先跑：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
PYTHONPATH=. bash scripts/validation/run_tui_layered_validation.sh
```

说明：
- 这条脚本会先跑 CLI contracts
- 再跑 TUI smoke fallback
- 如果环境里安装了 `textual`，还会自动跑真实 TUI 交互测试
- 若想完整支持异步交互测试，建议安装 `pytest-asyncio`

## 纯命令模式推荐顺序
1. `/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui help`
2. `/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui status`
3. `/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui doctor`
4. `/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui inspect workspace`
5. `/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui collect env`
6. `/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui diagnose fusion`
7. `/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui suggest-fix tf`
8. `/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui runbook list`

## 说明
- 系统 Python 里不一定有 Textual，所以直接 `python3 -m tools.cli` 不一定等价于部署体验
- 请优先使用部署入口 `/home/hanhan/Desktop/.ros2-agent/ros2-agent`
- 当前项目仍是工程平台原型，不应描述为 production-ready 恢复平台
- 重量级命令（如 quality / validate repo / benchmark workflow）仍建议在 TUI 外执行
