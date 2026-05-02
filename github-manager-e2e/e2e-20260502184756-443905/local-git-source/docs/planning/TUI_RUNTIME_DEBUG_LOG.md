# ROS2-Agent TUI 运行调试日志

文件路径：/home/hanhan/Desktop/ROS2-Agent/docs/planning/TUI_RUNTIME_DEBUG_LOG.md
创建时间：2026-05-01
用途：持续记录 TUI 中键盘/鼠标/退出/命令执行链的真实运行行为，帮助定位“按 Enter 后只退出 TUI，不执行命令”的问题。

## 记录规范
每次调试至少记录：
- 时间
- 触发方式（Enter / 点击 / 滚轮 / CLI）
- 预期行为
- 实际行为
- 相关代码位置
- 已执行验证命令
- 结果
- 推测根因
- 下一步动作

## 当前已知问题
- 用户反馈：在 TUI 中选中任意命令后，按 Enter 只会退出 TUI，看不到对应命令真正执行。
- 用户确认：这不是 UI 样式问题，而是执行链问题。
- 最新用户反馈：点击后右侧面板只看到一些代码样式内容，依旧主观感受为“什么都没有执行”。

## 初始观察
- CLI 直跑 `--no-ui` 命令时，关键命令可正常输出。
- 问题集中在 TUI -> Enter -> 结果展示 这条链路。

## 已确认事实
1. Enter 一直都能触发执行链。
2. 关键命令能产生非空输出。
3. 用户看见“只有一些代码”说明输出确实进入面板了，但展示体验不足以让用户明确感知“命令已执行完成”。

## 最新根因收缩
- 不是“没执行”。
- 不是“没输出”。
- 是“输出展示方式与用户预期严重不匹配”：
  - 输出面板只是生硬显示原始文本/JSON
  - 缺少强提示“执行成功/失败”与结构化结果头部
  - 用户把原始输出误判为‘只是一些代码，没有执行’

## 已追加修复策略
- 为 TUI 输出区统一走 `_render_output_text()`
- 所有 catalog 命令先通过 `run_catalog_command_capture()` 保证有字符串输出或明确错误提示
- 新增自动化测试 `tests/tools/test_tui_command_capture.py`
- 当前测试已通过：
  - help 有输出
  - status 有输出
  - collect env 有输出
  - 全命令目录至少返回可见输出或指导语

## 下一步建议
- 继续把输出区做成“结果卡片式”而不是纯原始文本
- 在输出顶部加入：命令名 / 执行完成 / exit_code / 时间
- 对 JSON 结果增加更强的标题和分隔，让它不再像‘一坨代码’

## 2026-05-01T03:05:06 | select_from_index
- selected_index: 0
- command: collect env

## 2026-05-01T03:05:06 | select_from_index
- selected_index: 0
- command: collect env

## 2026-05-01T03:05:07 | action_run_selected_enter
- selected_index: 0
- title: 环境采集
- command: collect env

## 2026-05-01T03:05:07 | action_run_selected_execute
- selected_index: 0
- title: 环境采集
- command: collect env

## 2026-05-01T03:05:07 | action_run_selected_exit
- selected_index: 0
- title: 环境采集
- command: collect env
- exit_code: 0
- output_preview: {
  "metadata": {
    "source": "ros2_env_collect",
    "collected_at": "2026-04-30T19:05:07+00:00",
    "command_used": [
      "which ros2",
      "which colcon",
      "which rosdep",
      "which python3",
      "which rviz2",
      "wh

## 2026-05-01T03:05:10 | select_from_index
- selected_index: 1
- command: collect workspace

## 2026-05-01T03:05:11 | select_from_index
- selected_index: 2
- command: collect graph

## 2026-05-01T03:05:11 | action_run_selected_enter
- selected_index: 2
- title: 运行图采集
- command: collect graph

## 2026-05-01T03:05:11 | action_run_selected_execute
- selected_index: 2
- title: 运行图采集
- command: collect graph

## 2026-05-01T03:05:12 | action_run_selected_exit
- selected_index: 2
- title: 运行图采集
- command: collect graph
- exit_code: 0
- output_preview: {
  "metadata": {
    "source": "ros2_graph_collect",
    "collected_at": "2026-04-30T19:05:12+00:00",
    "command_used": [
      "ros2 node list",
      "ros2 topic list",
      "ros2 topic info --verbose <topic>"
    ],
    "warnings": [

## 2026-05-01T03:05:15 | select_from_index
- selected_index: 9
- command: diagnose controller

## 2026-05-01T03:05:16 | action_run_selected_enter
- selected_index: 9
- title: 控制器诊断
- command: diagnose controller

## 2026-05-01T03:05:16 | action_run_selected_execute
- selected_index: 9
- title: 控制器诊断
- command: diagnose controller

## 2026-05-01T03:05:16 | action_run_selected_exit
- selected_index: 9
- title: 控制器诊断
- command: diagnose controller
- exit_code: 0
- output_preview: {
  "domain": "controller",
  "findings": [],
  "candidate_causes": [],
  "recommended_next_probe": {
    "action": "inspect_controller_manager_logs",
    "reason": "controller manager state needs confirmation",
    "risk_level": "read_only

## 2026-05-01T03:05:18 | action_run_selected_enter
- selected_index: 9
- title: 控制器诊断
- command: diagnose controller

## 2026-05-01T03:05:18 | action_run_selected_execute
- selected_index: 9
- title: 控制器诊断
- command: diagnose controller

## 2026-05-01T03:05:19 | action_run_selected_exit
- selected_index: 9
- title: 控制器诊断
- command: diagnose controller
- exit_code: 0
- output_preview: {
  "domain": "controller",
  "findings": [],
  "candidate_causes": [],
  "recommended_next_probe": {
    "action": "inspect_controller_manager_logs",
    "reason": "controller manager state needs confirmation",
    "risk_level": "read_only

## 2026-05-01T03:05:19 | select_from_index
- selected_index: 10
- command: diagnose fusion

## 2026-05-01T03:05:20 | action_run_selected_enter
- selected_index: 10
- title: 融合诊断
- command: diagnose fusion

## 2026-05-01T03:05:20 | action_run_selected_execute
- selected_index: 10
- title: 融合诊断
- command: diagnose fusion

## 2026-05-01T03:05:21 | action_run_selected_exit
- selected_index: 10
- title: 融合诊断
- command: diagnose fusion
- exit_code: 0
- output_preview: {
  "prioritized_candidates": [],
  "evidence_refs": [],
  "uncertainty_gaps": [],
  "recommended_next_probe": "collect_missing_runtime_evidence"
}

## 2026-05-01T03:05:22 | select_from_index
- selected_index: 11
- command: benchmark workflow

## 2026-05-01T03:09:43 | select_from_index
- selected_index: 12
- command: benchmark recovery

## 2026-05-01T17:14:16 | select_from_index
- selected_index: 1
- command: collect workspace

## 2026-05-01T17:14:17 | select_from_index
- selected_index: 1
- command: collect workspace

## 2026-05-01T17:14:17 | select_from_index
- selected_index: 2
- command: collect graph

## 2026-05-01T17:40:02 | select_from_index
- selected_index: 0
- command: doctor

## 2026-05-01T17:40:06 | action_run_selected_enter
- selected_index: 0
- title: 平台体检
- command: doctor

## 2026-05-01T17:40:06 | action_run_selected_execute
- selected_index: 0
- title: 平台体检
- command: doctor

## 2026-05-01T17:40:06 | action_run_selected_exit
- selected_index: 0
- title: 平台体检
- command: doctor
- exit_code: 0
- output_preview: 已完成平台体检。

## 2026-05-01T17:40:09 | select_from_index
- selected_index: 1
- command: inspect

## 2026-05-01T17:40:10 | action_run_selected_enter
- selected_index: 1
- title: 平台巡检
- command: inspect

## 2026-05-01T17:40:10 | action_run_selected_execute
- selected_index: 1
- title: 平台巡检
- command: inspect

## 2026-05-01T17:40:10 | action_run_selected_exit
- selected_index: 1
- title: 平台巡检
- command: inspect
- exit_code: 0
- output_preview: 已完成平台巡检。

## 2026-05-01T17:40:11 | select_from_index
- selected_index: 2
- command: history

## 2026-05-01T17:40:12 | action_run_selected_enter
- selected_index: 2
- title: 最近历史
- command: history

## 2026-05-01T17:40:12 | action_run_selected_execute
- selected_index: 2
- title: 最近历史
- command: history

## 2026-05-01T17:40:12 | action_run_selected_exit
- selected_index: 2
- title: 最近历史
- command: history
- exit_code: 0
- output_preview: 已读取最近命令历史。

## 2026-05-01T17:40:12 | select_from_index
- selected_index: 3
- command: workflow

## 2026-05-01T17:40:12 | action_run_selected_enter
- selected_index: 3
- title: 工作流总览
- command: workflow

## 2026-05-01T17:40:12 | action_run_selected_execute
- selected_index: 3
- title: 工作流总览
- command: workflow

## 2026-05-01T17:40:12 | action_run_selected_exit
- selected_index: 3
- title: 工作流总览
- command: workflow
- exit_code: 0
- output_preview: 已列出 workflow 资产。

## 2026-05-01T17:40:12 | select_from_index
- selected_index: 3
- command: workflow

## 2026-05-01T17:40:12 | action_run_selected_enter
- selected_index: 3
- title: 工作流总览
- command: workflow

## 2026-05-01T17:40:13 | action_run_selected_execute
- selected_index: 3
- title: 工作流总览
- command: workflow

## 2026-05-01T17:40:13 | action_run_selected_exit
- selected_index: 3
- title: 工作流总览
- command: workflow
- exit_code: 0
- output_preview: 已列出 workflow 资产。

## 2026-05-01T17:40:13 | select_from_index
- selected_index: 4
- command: report

## 2026-05-01T17:40:13 | action_run_selected_enter
- selected_index: 4
- title: 报告总览
- command: report

## 2026-05-01T17:40:13 | action_run_selected_execute
- selected_index: 4
- title: 报告总览
- command: report

## 2026-05-01T17:40:13 | action_run_selected_exit
- selected_index: 4
- title: 报告总览
- command: report
- exit_code: 0
- output_preview: 已整理报告资产入口。

## 2026-05-01T17:40:14 | select_from_index
- selected_index: 5
- command: settings

## 2026-05-01T17:40:14 | action_run_selected_enter
- selected_index: 5
- title: 设置说明
- command: settings

## 2026-05-01T17:40:14 | action_run_selected_execute
- selected_index: 5
- title: 设置说明
- command: settings

## 2026-05-01T17:40:14 | action_run_selected_exit
- selected_index: 5
- title: 设置说明
- command: settings
- exit_code: 0
- output_preview: 已展示当前只读设置说明。

## 2026-05-01T17:40:15 | select_from_index
- selected_index: 8
- command: quality

## 2026-05-01T17:40:15 | action_run_selected_enter
- selected_index: 8
- title: 完整质量门
- command: quality

## 2026-05-01T17:40:15 | action_run_selected_execute
- selected_index: 8
- title: 完整质量门
- command: quality

## 2026-05-01T17:40:15 | action_run_selected_exit
- selected_index: 8
- title: 完整质量门
- command: quality
- exit_code: 2
- output_preview: quality 命令属于重量级验证流程，需在 TUI 外部运行。

## 2026-05-01T17:40:16 | select_from_index
- selected_index: 12
- command: collect tf

## 2026-05-01T17:40:17 | action_run_selected_enter
- selected_index: 12
- title: TF 采集
- command: collect tf

## 2026-05-01T17:40:17 | action_run_selected_execute
- selected_index: 12
- title: TF 采集
- command: collect tf

## 2026-05-01T17:40:17 | action_run_selected_exit
- selected_index: 12
- title: TF 采集
- command: collect tf
- exit_code: 0
- output_preview: 已完成 TF 采集。

## 2026-05-01T17:40:18 | select_from_index
- selected_index: 15
- command: diagnose workspace

## 2026-05-01T17:40:18 | action_run_selected_enter
- selected_index: 15
- title: 工作区诊断
- command: diagnose workspace

## 2026-05-01T17:40:18 | action_run_selected_execute
- selected_index: 15
- title: 工作区诊断
- command: diagnose workspace

## 2026-05-01T17:40:18 | action_run_selected_exit
- selected_index: 15
- title: 工作区诊断
- command: diagnose workspace
- exit_code: 0
- output_preview: 已完成工作区诊断。

## 2026-05-01T17:40:20 | select_from_index
- selected_index: 26
- command: doctor control

## 2026-05-01T17:40:20 | action_run_selected_enter
- selected_index: 26
- title: 控制器体检
- command: doctor control

## 2026-05-01T17:40:20 | action_run_selected_execute
- selected_index: 26
- title: 控制器体检
- command: doctor control

## 2026-05-01T17:40:20 | action_run_selected_exit
- selected_index: 26
- title: 控制器体检
- command: doctor control
- exit_code: 0
- output_preview: 已完成控制器体检。

## 2026-05-01T17:40:22 | select_from_index
- selected_index: 40
- command: profile verify

## 2026-05-01T17:40:23 | action_run_selected_enter
- selected_index: 40
- title: Profile 验证
- command: profile verify

## 2026-05-01T17:40:23 | action_run_selected_execute
- selected_index: 40
- title: Profile 验证
- command: profile verify

## 2026-05-01T17:40:23 | action_run_selected_exit
- selected_index: 40
- title: Profile 验证
- command: profile verify
- exit_code: 0
- output_preview: 已检查 profile 安装状态。

## 2026-05-01T17:40:23 | select_from_index
- selected_index: 39
- command: profile install

## 2026-05-01T17:40:24 | action_run_selected_enter
- selected_index: 39
- title: Profile 安装
- command: profile install

## 2026-05-01T17:40:24 | action_run_selected_execute
- selected_index: 39
- title: Profile 安装
- command: profile install

## 2026-05-01T17:40:24 | action_run_selected_exit
- selected_index: 39
- title: Profile 安装
- command: profile install
- exit_code: 0
- output_preview: 已完成 demo profile 安装。

## 2026-05-01T17:40:25 | select_from_index
- selected_index: 32
- command: replay workflow

## 2026-05-01T17:40:25 | action_run_selected_enter
- selected_index: 32
- title: 工作流回放
- command: replay workflow

## 2026-05-01T17:40:25 | action_run_selected_execute
- selected_index: 32
- title: 工作流回放
- command: replay workflow

## 2026-05-01T17:40:25 | action_run_selected_exit
- selected_index: 32
- title: 工作流回放
- command: replay workflow
- exit_code: 0
- output_preview: 已整理 workflow replay 入口。
