# ROS2-Agent Profile Design

## 1. 目标

将 ROS2-Agent 作为 Hermes 的独立 profile 模板交付，使用户可以快速创建专属 ROS2 专家实例。

## 2. profile 组成

- `SOUL.md`：定义 ROS2-Agent 身份、教学风格、工程纪律与安全边界
- `AGENTS.md`：定义工作区级上下文规则
- `config.template.yaml`：提供建议的 Hermes 配置模板
- `env.template`：列出常见 provider/integration 所需变量
- `bootstrap/`：后续放置 profile 初始化脚本与安装流程

## 3. 设计原则

1. simulation-first
2. smart approvals by default
3. memory enabled
4. long-session friendly
5. future-ready for gateway / cron / delegation / MCP

## 4. 未来扩展

后续可以衍生：
- ros2-agent-sim
- ros2-agent-ci
- ros2-agent-lab
- ros2-agent-train
