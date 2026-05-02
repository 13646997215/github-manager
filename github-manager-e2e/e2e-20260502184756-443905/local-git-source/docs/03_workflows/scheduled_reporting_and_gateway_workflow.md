# Scheduled Reporting and Gateway Workflow

## Goal
让 ROS2-Agent 在未来能够稳定对接 Hermes cron / gateway，自动输出实验室级、团队级、仓库级 ROS2 质量报告。

## Planned pipeline
1. 调用 validation / benchmark / demo pipeline。
2. 生成 JSON benchmark report。
3. 导出 Markdown digest，便于 GitHub README、Issue、周报、聊天推送复用。
4. 由未来的 Hermes cron job 定时执行。
5. 由 gateway / messaging target 推送到 Telegram / Feishu / Discord / Matrix 等协作渠道。

## Design rules
- 所有产物必须留在仓库工作区内。
- JSON 作为 machine-readable artifact，Markdown 作为 human-readable digest。
- 未来接入真实网关时，不让 agent 直接拼装混乱自由文本，而是优先基于结构化报告二次渲染。
- 任何自动推送前，必须先经过 full quality gate，避免把错误报告发到团队群里。

## Future hooks
- `scripts/validation/generate_benchmark_report.py`：核心结构化报告入口。
- `scripts/validation/export_latest_report.sh`：导出最新报告供外部系统消费。
- 未来可新增：
  - `scripts/integration/render_report_digest.py`
  - `scripts/integration/prepare_gateway_payload.py`
  - `cronjobs/*.yaml` 或示例 prompt 文档

## Competitive value
- 不是“能跑个 agent”就结束，而是把机器人开发团队每天都会遇到的验证、诊断、播报、协作闭环做完整。
- 对个人开发者、实验室、机器人创业团队都具有直接吸引力。
