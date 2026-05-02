# EXECUTION_LOG - HERMES ALIGNMENT (SUPPLEMENTAL SUMMARY)

最后更新：2026-05-01
状态：TUI / validation / bootstrap / docs / requirements 多轮增强已完成补充收口

## 这份补充总结的目的
用于在后续新对话或上下文压缩后，快速恢复本轮后续增强工作的真实完成状态，避免重复扫描与重复修补。

## 已完成的补充增强总览

### 1. TUI 产品化增强
已完成：
- 命令搜索：`/` 聚焦搜索框并过滤命令目录
- 最近历史：`R` 显示 recent history
- 最近错误：`E` 显示 recent error / blocked / not_implemented 记录
- 长任务 / 重量级提示：状态栏显示 lightweight / heavyweight 提示
- 仓库内脚本入口体验修复：`python3 tools/cli.py ...` 不再要求手工设置 `PYTHONPATH`

核心文件：
- `tools/cli.py`
- `tests/tools/test_tui_workbench.py`
- `tests/tools/test_tui_interaction.py`
- `tests/tools/test_cli_script_entry.py`
- `tests/tools/test_cli_contracts.py`

### 2. CLI / TUI 分层验证体系
已完成：
- 新增 `scripts/validation/run_tui_layered_validation.sh`
- layer 1：CLI contract tests（无 Textual 必跑）
- layer 2：TUI smoke fallback
- layer 3：Textual interaction tests（有 `textual` 时执行，无则 skip）
- heavyweight 命令单独按契约验证，不与轻量 happy-path 混淆

核心文件：
- `scripts/validation/run_tui_layered_validation.sh`
- `scripts/validation/run_full_quality_gate.sh`
- `scripts/validation/run_phase2_validation.sh`

### 3. pytest 兼容层收口
已完成：
- 在 `pyproject.toml` 中注册 `asyncio` mark
- 新增 `pytest.ini` 兼容旧版 pytest / ROS launch_testing hooks
- 消除 layered validation 中的 `unknown pytest.mark.asyncio` warning
- 避免在 `pytest.ini` 中使用当前环境不兼容的 `pythonpath = .`

核心文件：
- `pyproject.toml`
- `pytest.ini`

### 4. 开发依赖与文档对齐
已完成：
- `requirements-dev.txt` 新增：
  - `pytest-asyncio>=0.23`
  - `textual>=0.58`
- README / README_EN / quickstart / developer-setup 全部同步到 layered validation、新快捷键与依赖说明

核心文件：
- `requirements-dev.txt`
- `README.md`
- `README_EN.md`
- `docs/00_overview/quickstart.md`
- `docs/00_overview/developer-setup.md`
- `docs/03_workflows/launcher-ui-workflow.md`

### 5. bootstrap / post-install 收口
已完成：
- `install_profile.sh` 的推荐验证命令已纳入 layered validation
- `post_install_validate.sh` 已从“仅检查文件存在”升级为：
  - 必需文件检查
  - repository root record 检查
  - repo root 存在性检查
  - CLI entrypoint 存在性检查
  - 只读 smoke checks：
    - `python3 tools/cli.py --smoke-ui`
    - `python3 tools/cli.py --no-ui help`
    - `python3 tools/cli.py --no-ui status`

核心文件：
- `profile/ros2-agent/bootstrap/install_profile.sh`
- `profile/ros2-agent/bootstrap/post_install_validate.sh`

## 关键验证结果

### TUI layered validation
命令：
`PYTHONPATH=. bash scripts/validation/run_tui_layered_validation.sh`

结果：
- layer 1: 15 passed
- layer 2: smoke fallback passed
- layer 3: 6 skipped（当前环境无 textual，符合预期）
- 总体：passed

### phase2 validation
命令：
`bash scripts/validation/run_phase2_validation.sh`

结果：
- repo validation passed
- layered validation passed
- 原有 pytest slices: 93 passed, 6 skipped
- 总体：passed

### post-install validation
命令：
`bash profile/ros2-agent/bootstrap/install_profile.sh /tmp/ros2-agent-profile-test`
`bash profile/ros2-agent/bootstrap/post_install_validate.sh /tmp/ros2-agent-profile-test`

结果：
- install passed
- read-only smoke checks passed
- post-install validation passed

## 当前真实能力边界

### 已可直接体验 / live
- 三栏 TUI 工作台
- summary / next_actions / payload / raw 四视图
- `/` 搜索命令
- `R` 查看最近历史
- `E` 查看最近错误
- `python3 tools/cli.py` 仓库内直接入口
- layered validation 三层验证
- install / post-install 的只读 smoke 验证

### prototype / environment-dependent
- Textual 真实交互测试层：测试代码已就绪，但当前机器未安装 textual，因此表现为 skip
- 更深层 post-install 扩展验证（如 inspect/collect/runbook 的只读集）尚未建立，当前保持最小安全集合

## 推荐后续起点
如果继续推进，优先顺序建议：
1. 如需要真实交互测试，在开发环境执行：
   `pip install -r requirements-dev.txt`
2. 复跑：
   `PYTHONPATH=. bash scripts/validation/run_tui_layered_validation.sh`
3. 如需扩展安装后验证，可新增一个可选的 `extended post-install validation` 脚本，覆盖更深层但仍低风险的只读命令

## 本轮补充增强涉及的关键文件清单
- `tools/cli.py`
- `tests/tools/test_tui_workbench.py`
- `tests/tools/test_tui_interaction.py`
- `tests/tools/test_cli_script_entry.py`
- `tests/tools/test_cli_contracts.py`
- `scripts/validation/run_tui_layered_validation.sh`
- `scripts/validation/run_full_quality_gate.sh`
- `scripts/validation/run_phase2_validation.sh`
- `profile/ros2-agent/bootstrap/install_profile.sh`
- `profile/ros2-agent/bootstrap/post_install_validate.sh`
- `requirements-dev.txt`
- `pyproject.toml`
- `pytest.ini`
- `README.md`
- `README_EN.md`
- `docs/00_overview/quickstart.md`
- `docs/00_overview/developer-setup.md`
- `docs/03_workflows/launcher-ui-workflow.md`
- `docs/planning/EXECUTION_LOG_HERMES_ALIGNMENT.md`

## 结论
本轮补充增强已经把：
- 功能
- 测试
- 依赖
- 文档
- bootstrap
- post-install validation
这六层基本对齐。

后续若新开对话，优先读取：
1. `docs/planning/EXECUTION_LOG_HERMES_ALIGNMENT.md`
2. `docs/planning/EXECUTION_LOG_HERMES_ALIGNMENT_SUPPLEMENTAL_SUMMARY.md`
