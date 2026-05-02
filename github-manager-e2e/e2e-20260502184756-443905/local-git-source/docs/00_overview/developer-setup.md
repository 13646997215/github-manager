# Developer Setup

## 建议验证顺序
1. python3 -m venv .venv && source .venv/bin/activate
2. pip install -r requirements-dev.txt
3. 如果要跑真实 TUI 交互测试，额外安装：
   ```bash
   pip install textual pytest-asyncio
   ```
4. PYTHONPATH=. python3 scripts/validation/validate_repo.py
5. PYTHONPATH=. bash scripts/validation/run_tui_layered_validation.sh
6. python3 -m pytest tests/tools tests/collectors tests/diagnosers tests/workflows tests/recovery tests/integration -q

## TUI 分层验证说明
`run_tui_layered_validation.sh` 分三层：
1. CLI contract tests：不依赖 Textual，验证脚本入口、命令契约、heavyweight blocked 行为
2. TUI smoke fallback：验证无 Textual 时仍可正常给出 fallback 体验
3. Textual interaction tests：安装 `textual` 后自动运行真实交互测试；若环境不满足会 skip

## 针对高级 TUI 工作台的额外验证
1. 准备部署目录 `/home/hanhan/Desktop/.ros2-agent`
2. 确认 `/home/hanhan/Desktop/.ros2-agent/venv/bin/python` 存在
3. 运行：
   ```bash
   /home/hanhan/Desktop/.ros2-agent/ros2-agent --smoke-ui
   /home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui help
   /home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui status
   /home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui diagnose fusion
   /home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui inspect workspace
   ```
4. 若要人工体验，直接运行：
   ```bash
   /home/hanhan/Desktop/.ros2-agent/ros2-agent
   ```
5. 在 TUI 中验证：
   - 左侧命令目录可浏览
   - `/` 可搜索命令
   - `R` 可查看最近 history
   - `E` 可查看最近错误
   - Enter 可以执行
   - Tab 可切换 summary / next_actions / payload / raw
   - 右侧结果区会更新

## 说明
- 无 ROS2 环境时，integration-lite tests 会合理 skip 或 degraded
- workflow / recovery 资产优先用于仓库内验证与教学复演
- 高级 TUI 依赖部署 venv；不要假设系统 Python 一定具备 Textual
- tests/tools/test_tui_workbench.py 与 test_tui_interaction.py 可能因 Textual 环境缺失而 skip，这属于环境边界，不等于功能失败
