# Gateway Cron Demo Workflow

## 目标
展示如何周期性导出 benchmark/report 资产，而不是宣称已具备生产自动化。

## Demo 范围
- 运行 benchmark/report pipeline
- 导出 markdown digest
- 说明哪些部分仍依赖 Hermes 外部 cron/gateway 配置

## 非目标
- 不保证消息投递
- 不保证 secrets 管理
- 不保证生产级告警重试
