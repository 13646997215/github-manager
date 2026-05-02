# ROS2-Agent 项目总体规划文档

> 项目工作区：`/home/hanhan/Desktop/ROS2-Agent`
> 
> 项目目标：基于 Hermes Agent 框架，打造一个专属于 ROS2 机器人仿真开发、训练测试、教学引导的垂直专家 Agent，面向 Ubuntu 22.04 + ROS2 Humble 生态，兼顾个人开发者、实验室、开源社区与小型机器人团队场景。

---

## 1. 项目愿景

ROS2-Agent 不是“会聊 ROS2 的聊天机器人”，而是一个真正可执行、可记忆、可成长、可协作、可审计的机器人研发专家系统。

它需要具备以下定位：

1. 教学型导师
   - 能面向新手进行 ROS2 概念讲解、环境搭建引导、命令解释、问题拆解。
   - 能根据用户基础水平动态调整讲解深度。

2. 工程型开发助手
   - 能处理 Ubuntu 22.04 上 ROS2 Humble 常见开发任务。
   - 能协助完成 workspace 构建、依赖修复、节点调试、launch 排障、Gazebo / RViz / TF / MoveIt / controller 调试。

3. 仿真与测试专家
   - 能为仿真开发、训练测试、回归验证提供自动化支持。
   - 能定期巡检构建状态、日志异常、性能变化，并输出结构化报告。

4. 项目级知识中枢
   - 能持续记住用户的项目约定、工作区结构、常见错误与修复策略。
   - 能对历史会话、历史问题、历史实验结果进行检索与归纳。

5. 面向 GitHub 的竞争力产品
   - 不做“泛泛而谈的 AI 壳子”，而是聚焦 ROS2 开发痛点，形成开箱即用的实战方案。
   - 项目要能让用户一眼看出：这个 Agent 真的能解决机器人开发中的历史难题。

---

## 2. 对 Hermes Agent 的整体理解

基于已调研的 Hermes Agent 文档、技能、结构与能力，可以将其理解为一个“通用 Agent 操作系统（Agent OS）”。

它的核心不是单纯聊天，而是：

- 有完整的 Agent 循环（LLM + Tool Calling + Tool Result 回灌）
- 有可扩展工具注册体系
- 有跨会话记忆与用户画像系统
- 有 Skills 机制，可积累经验与工作流
- 有 Gateway，可接入多消息平台
- 有 Cron，可做定时自动化
- 有 Profiles，可隔离不同 Agent 实例
- 有 Delegation，可做多 Agent 协同
- 有 MCP，可对接外部能力和平台
- 有审批与安全机制，适合真实工程系统

换句话说，Hermes 已经提供了一个成熟底座；ROS2-Agent 的重点不是重复造轮子，而是把机器人领域的知识、流程和工具“产品化”到 Hermes 之上。

---

## 3. Hermes Agent 的关键搭建模式

### 3.1 Profile-first 模式

Hermes 最适合做垂直专家 Agent 的方式不是直接魔改主程序，而是建立独立 profile。

对 ROS2-Agent 来说，profile 是天然的隔离单元，可以独立拥有：

- config.yaml
- .env
- sessions
- memory
- skills
- logs
- gateway 配置
- auth 信息

这意味着未来可以形成多个专业实例，例如：

- ros2-agent-sim：仿真开发专家
- ros2-agent-lab：实验室联调专家
- ros2-agent-ci：回归测试 / 自动化检查专家
- ros2-agent-train：训练任务 / 数据分析专家

优势：
- 不污染现有 workbot
- 不同场景可切不同模型、工具和安全级别
- 更容易做开源分发、复制和社区使用

### 3.2 Skill-first 模式

Hermes 的 Skills 机制非常适合机器人领域。

ROS2 的很多问题并不是“算力不够”，而是：
- 工作流繁琐
- 经验碎片化
- 排障依赖老手经验
- 输出结果容易不稳定

因此最优路线是先沉淀一套高质量 ROS2 技能，而不是一开始就做大量复杂工具。

适合优先沉淀为 skill 的内容：
- ROS2 环境搭建流程
- workspace 创建与 overlay 规范
- rosdep 诊断与修复
- colcon build 常见错误处理
- launch 失败排障
- Gazebo / RViz / TF / QoS / DDS 网络问题分析
- MoveIt / controller_manager / URDF / Xacro 相关工作流
- 真机联调的安全规范

### 3.3 Tool-layering 模式

ROS2-Agent 的能力结构建议分三层：

第一层：Hermes 通用原生工具
- terminal
- file / read_file / search_files / patch / write_file
- todo
- session_search
- memory
- cronjob
- send_message
- delegate_task

第二层：领域工作流 Skills
- 将高频 SOP 组织为可调用经验
- 提升稳定性和可重复性

第三层：ROS2 专用工具 / MCP 工具
- 结构化提取系统信息
- 隐藏复杂 shell 细节
- 输出 JSON 化结果，方便模型稳定推理

例如后续可以规划：
- ros2_env_audit
- ros2_workspace_inspect
- colcon_build_summary
- ros2_graph_snapshot
- ros2_launch_diagnose
- gazebo_health_check
- tf_tree_snapshot
- rosbag_inspect
- controller_status_report

### 3.4 Context + Memory 模式

Hermes 的系统提示、技能、用户记忆、项目上下文是分层注入的，而且很多内容会在会话开始时冻结，这一点对长期工程项目非常重要。

ROS2-Agent 应利用这套机制，把下面这些内容进行合理分层：

1. SOUL / persona / profile 级内容
   - Agent 角色定位
   - 教学风格
   - 安全边界
   - 输出标准

2. 项目上下文文件（如 AGENTS.md / HERMES.md）
   - 当前 ROS2 工作区约定
   - 编译命令规范
   - 仿真入口规范
   - 目录组织规则
   - 测试与验证标准

3. Memory
   - 高稳定事实，如用户偏好的 distro、工作方式、已有机器人平台信息
   - 长期有价值的环境习惯、常见坑点

4. Session Search
   - 处理高变动历史信息
   - 查询过去调试记录、仿真异常、构建失败原因

### 3.5 Gateway + Cron 模式

这是 Hermes 特别强的一点，也是 ROS2-Agent 非常值得继承的差异化能力。

未来可以做到：

- 夜间自动 colcon build + 测试
- 定时运行仿真 smoke test
- 自动分析日志并发送摘要
- 定期生成回归报告
- 训练任务结束后自动推送结果
- 远程通过消息平台向 Agent 请求分析和状态查询

这会让 ROS2-Agent 从“桌面问答助手”升级成“机器人研发协作系统”。

### 3.6 Delegation / Multi-Agent 模式

Hermes 本身支持子 Agent 协作；本地你也已有自建的多 Agent 架构经验。

在 ROS2-Agent 中，多 Agent 最适合用于以下高价值场景：

- Agent A：分析 colcon 编译日志
- Agent B：检查 package.xml / CMakeLists / setup.py 配置
- Agent C：检查 launch / URDF / controller 配置
- Agent D：汇总根因并提出修复路线

但必须注意：
- 多 Agent 不适合过早全面铺开
- 优先单 Agent 打稳工作流，再逐步引入协作
- 所有并发修改文件的操作必须严格隔离

---

## 4. ROS2-Agent 的目标用户与典型使用场景

### 4.1 目标用户

1. ROS2 初学者
   - 需要教学、引导、术语解释、分步骤操作帮助

2. 机器人开发者
   - 需要环境搭建、仿真排障、节点调试、测试自动化

3. 实验室成员 / 参赛队员
   - 需要共享工作流、快速定位问题、减少新人上手成本

4. 小型机器人团队
   - 需要 Agent 化知识库、日报、巡检、回归验证、远程消息接入

### 4.2 典型场景

1. 从零搭建 ROS2 Humble 开发环境
2. 新建 workspace、导入包、配置依赖、构建与 source
3. 调试 launch 报错、TF 异常、controller 失联、Gazebo 不启动
4. 分析 build / runtime 日志
5. 自动生成排障报告与测试报告
6. 夜间回归仿真与消息通知
7. 教学式解释某个 ROS2 机制的原理与实践
8. 为 GitHub 项目贡献者提供统一工程规范和上手入口

---

## 5. 这个项目必须攻克的“历史性难题”

这是整个项目最关键的竞争力设计部分。很多 Agent 项目最终失败，不是模型不够强，而是没有真的解决领域内长期痛点。

### 5.1 难题一：ROS2 环境脆弱、前提依赖复杂

典型表现：
- source 顺序混乱
- overlay 污染
- apt / pip / rosdep / colcon 依赖冲突
- 多工作区互相干扰
- 图形环境、Gazebo、RViz 启动条件复杂

解决思路：
- 建立“环境发现优先”的强制流程
- 所有执行前先做 audit
- 所有技能都要包含 prerequisite check
- 将环境诊断结果结构化输出
- 尽量把工作区、脚本、文档、配置都约束在项目内

### 5.2 难题二：ROS2 问题排障高度依赖老手经验

典型表现：
- 错误信息长而杂
- launch 报错只是表象
- 真正原因可能在 URDF、依赖、controller、QoS、DDS、时间源

解决思路：
- 将老手经验沉淀为 Skills
- 将高频问题的分析链条固化为 SOP
- 逐步把高频终端分析提炼成结构化工具
- 用 session_search + memory 形成项目级经验库

### 5.3 难题三：机器人开发链路太长，单轮对话没意义

典型表现：
- 今天处理环境问题，明天处理仿真，后天分析训练日志
- 问题跨会话、跨天、跨设备

解决思路：
- 借助 Hermes 的 memory / sessions / session_search
- 借助 Cron 做自动化检测与汇报
- 借助 Gateway 做远程交互
- 将 Agent 从“即时问答”升级成“长期协作者”

### 5.4 难题四：危险操作多，Agent 容易不可信

机器人开发会碰到：
- 安装/卸载依赖
- 修改系统服务
- 改网络配置
- 影响真实机器人控制节点

解决思路：
- 明确区分只读诊断模式与执行模式
- 仿真环境和真机环境使用不同 profile
- 高风险操作必须有审批与确认
- 尽量使用受控工具而不是直接开放任意命令

### 5.5 难题五：大多数开源 Agent 项目“看起来强，实际上难落地”

典型表现：
- README 很强，demo 很弱
- 功能列表很多，工作流不闭环
- 没有 benchmark，没有真实复现案例

解决思路：
- 用“可复现实战案例”构建信任
- 做一套公开 benchmark
- 设计坏案例工作区（故障注入）
- 输出对比明确、结果可验证的演示流程

---

## 6. ROS2-Agent 的产品定位与核心卖点

建议项目对外宣传时，不要说：
- “又一个通用 AI Agent”
- “支持 ROS2 问答”

应该强调：

1. 面向 Ubuntu 22.04 + ROS2 Humble 的专用专家 Agent
2. 真的能执行仿真开发流程，而不是只会解释概念
3. 真的能做环境搭建、依赖修复、构建排障、launch 诊断
4. 真的能记住你的项目背景和历史问题
5. 真的能做夜间回归、定时巡检、远程消息协作
6. 基于 Hermes 的 profile、skills、gateway、cron、memory、delegation 打造，具备长期成长能力

一句话卖点建议：

“ROS2-Agent is an executable ROS2 expert built on Hermes: it teaches, debugs, remembers, automates, and continuously improves your robot simulation and development workflow on Ubuntu 22.04.”

---

## 7. 总体架构规划

### 7.1 顶层架构

建议采用以下逻辑层：

1. Foundation Layer（Hermes 原生底座）
   - Agent loop
   - tools
   - memory
   - skills
   - sessions
   - gateway
   - cron
   - delegation
   - MCP

2. Domain Intelligence Layer（ROS2 领域智能层）
   - ROS2 专家 persona
   - 教学引导策略
   - 排障方法论
   - 安全规范
   - 项目上下文模板

3. Workflow Layer（工作流层）
   - 环境搭建
   - workspace 管理
   - build / launch / debug
   - 仿真回归
   - 日志分析
   - 测试总结

4. Structured Tool Layer（结构化工具层）
   - ROS2 状态采集工具
   - 图谱采集工具
   - 构建摘要工具
   - 仿真健康检查工具
   - 测试结果聚合工具

5. Collaboration Layer（协作层）
   - GitHub 项目文档
   - Gateway 消息通知
   - 多 Agent 协作
   - CI / cron / webhook 集成

### 7.2 推荐目录规划

由于你明确要求项目目录不能乱放、并且未来要上 GitHub，因此建议整个项目保持非常清晰的层次。

推荐在 `/home/hanhan/Desktop/ROS2-Agent` 内采用如下结构：

```text
ROS2-Agent/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── 00_overview/
│   ├── 01_architecture/
│   ├── 02_product/
│   ├── 03_workflows/
│   ├── 04_benchmarks/
│   ├── 05_roadmap/
│   └── planning/
├── profile/
│   ├── ros2-agent/
│   │   ├── config.template.yaml
│   │   ├── env.template
│   │   ├── SOUL.md
│   │   ├── AGENTS.md
│   │   └── bootstrap/
├── skills/
│   ├── ros2-environment-bootstrap/
│   ├── ros2-workspace-diagnose/
│   ├── ros2-colcon-build-troubleshoot/
│   ├── ros2-launch-debug/
│   ├── ros2-gazebo-debug/
│   ├── ros2-controller-debug/
│   └── ros2-regression-report/
├── tools/
│   ├── ros2_env_audit.py
│   ├── ros2_workspace_inspect.py
│   ├── ros2_graph_snapshot.py
│   ├── colcon_build_summary.py
│   └── gazebo_health_check.py
├── mcp/
│   ├── servers/
│   └── connectors/
├── examples/
│   ├── demo_workspace/
│   ├── broken_cases/
│   └── transcripts/
├── benchmarks/
│   ├── tasks/
│   ├── fixtures/
│   └── reports/
├── scripts/
│   ├── setup/
│   ├── audit/
│   ├── cron/
│   └── validation/
├── tests/
│   ├── skills/
│   ├── tools/
│   ├── workflows/
│   └── benchmarks/
└── assets/
    ├── diagrams/
    └── images/
```

说明：
- profile/：用于存放你的 ROS2-Agent 专属 profile 模板
- skills/：存放这个项目自己的 ROS2 专业技能
- tools/：未来放结构化工具
- docs/：对外最重要的资产之一
- examples/：演示与复现实例，会极大增强项目吸引力
- benchmarks/：衡量竞争力的核心资产
- scripts/：自动化入口
- tests/：让项目显得可靠、可维护、可扩展

---

## 8. 分阶段实施路线图

### Phase 0：研究与规划阶段（当前阶段）

目标：
- 吃透 Hermes Agent 的搭建模式
- 明确 ROS2-Agent 的产品定位、架构与路线图
- 输出正式规划文档

交付：
- 本规划文档
- 后续的 README / 架构图 / 任务分解文档

### Phase 1：最小可用版本 MVP

目标：
打造一个“ROS2 仿真开发专家 Agent”。

MVP 能力建议：
- Ubuntu 22.04 + ROS2 Humble 环境发现
- workspace 结构检查
- rosdep / colcon 问题诊断
- launch 问题分析
- Gazebo / RViz / TF 常见问题排查
- 教学式解释能力
- 基础消息通知 / 基础 cron 回归能力

MVP 交付建议：
- 1 个 profile 模板
- 6~10 个核心 skills
- 3~5 个结构化工具（或脚本封装）
- 3 个可复现 demo
- 1 套基础 benchmark
- 1 套清晰上手文档

### Phase 2：工程增强版

目标：
从“个人助手”升级到“项目协作者”。

能力扩展：
- GitHub 项目集成
- 更完整的 regression report
- Gateway 远程通知
- 工作流级日志归档
- 更细粒度的安全策略
- 更强的 session knowledge recall

### Phase 3：团队协作版

目标：
面向实验室 / 小团队使用。

能力扩展：
- 多 profile 场景分工
- 团队共享技能库
- 标准故障案例库
- benchmark 排行/统计
- PR / CI / nightly build 集成

### Phase 4：高级平台化版本

目标：
把 ROS2-Agent 升级为机器人研发工作台入口。

能力扩展：
- MCP 对接仿真平台/训练平台/实验管理系统
- 多 Agent 并行分析
- 更强的结构化诊断工具
- 实验结果自动摘要与归档
- 面向真实机器人系统的受控执行体系

---

## 9. MVP 的优先级建议

为了避免一开始做得太散，建议优先级严格如下：

### P0：必须先做
- 独立项目结构与文档骨架
- Hermes-based ROS2-Agent 整体说明
- profile 模板设计
- ROS2 领域 persona 设计
- 核心 skills 列表与规范
- 环境发现与 workspace 诊断流程

### P1：高价值早做
- colcon build 诊断能力
- launch / Gazebo 调试技能
- README 对外包装
- demo workspace / broken cases
- benchmark 设计

### P2：增强体验
- cron 自动回归
- gateway 消息通知
- GitHub 集成
- 部分结构化工具

### P3：后续强化
- MCP 连接器
- 多 Agent 编排
- 真机联调模式
- 更复杂的训练/评估闭环

---

## 10. 技术架构建议

### 10.1 Agent 角色设计

建议你的 ROS2-Agent 人设不是“冷冰冰执行器”，而是“资深 ROS2 导师 + 研发专家”。

能力要求：
- 教学：解释概念、补基础、引导思路
- 引导：一步步拆任务，不让用户迷路
- 拓展：主动给出进阶方向
- 提升：帮助形成更专业的开发习惯
- 优化：发现工作流低效点，提出改进建议

但在工程层面，要非常克制：
- 危险操作先确认
- 每次行动要能解释前提与验证方式
- 优先稳定而不是炫技

### 10.2 Profile 配置原则

未来 ros2-agent profile 建议具备以下特征：

- 默认 workdir 指向用户 ROS2 工作区
- 默认启用 terminal/file/memory/session_search/todo/skills/cronjob/delegation
- 根据需要启用 messaging
- 安全模式默认 manual 或 smart
- 默认启用项目上下文加载
- 单独维护 memory 与 sessions

### 10.3 技能体系设计原则

每个技能都建议包含：
- 适用场景
- 前提检查
- 分步骤操作
- 常见错误与分支处理
- 验证方式
- 风险提示
- 何时应停止并询问用户

这会极大提升 Agent 的稳定性与可信度。

### 10.4 结构化工具设计原则

未来的工具不要只是简单包装 shell，而要追求：
- 固定输入
- 结构化输出（JSON）
- 明确错误类型
- 可复用
- 可测试
- 可审计

例如 `ros2_env_audit` 工具输出不应只是原始命令文本，而应输出类似：

```json
{
  "ros_distro": "humble",
  "ubuntu_version": "22.04",
  "workspace_detected": true,
  "underlays": ["/opt/ros/humble"],
  "overlays": ["/home/user/ws/install"],
  "missing_dependencies": [],
  "warnings": ["gazebo not found"],
  "ready": false
}
```

这种输出才适合长期做稳定 Agent。

---

## 11. 开源竞争力设计

如果这个项目想在 GitHub 上真正吸引人，必须不止“功能全”，还要“可信、可演示、可复现、可参与”。

### 11.1 README 竞争力

README 必须让人一眼看到：
- 这是做什么的
- 为什么不是普通聊天机器人
- 它解决了哪些真实 ROS2 痛点
- 它和其他 Agent / Copilot / 通用 LLM 的差别是什么
- 5 分钟如何开始
- 有哪些可复现实战案例

### 11.2 Demo 竞争力

建议准备三类 demo：

1. 环境搭建 demo
2. 故障诊断 demo
3. 夜间回归与推送 demo

每个 demo 都要有：
- 输入条件
- 触发命令
- Agent 行为
- 输出结果
- 成功标准

### 11.3 Benchmark 竞争力

建议构建一套公开 benchmark，至少包含：

1. 环境搭建任务集
2. 编译错误定位任务集
3. launch / Gazebo 报错任务集
4. TF / QoS / 网络问题任务集
5. 日志总结与回归报告任务集

评估指标可以包括：
- 任务完成率
- 根因命中率
- 修复建议有效率
- 首次响应有效信息比例
- 回归报告可读性

### 11.4 社区竞争力

项目要能支持社区共同成长：
- 欢迎大家贡献 skills
- 欢迎提交 broken cases
- 欢迎提交 benchmark case
- 欢迎贡献不同机器人平台支持

这样项目就不是一次性作品，而是“ROS2 Agent 生态”。

---

## 12. 风险分析与应对策略

### 风险 1：范围过大，前期失焦
应对：
- 先聚焦 Ubuntu 22.04 + ROS2 Humble
- 先聚焦仿真开发，不急着支持真机自治控制
- 先把高频工作流做扎实

### 风险 2：只靠 terminal，稳定性不足
应对：
- 先用 terminal 快速验证需求
- 高频场景逐步升级为结构化工具

### 风险 3：技能库质量不高，导致体验不稳定
应对：
- 为 skill 设定统一规范
- 每个 skill 必须包含验证步骤和分支处理
- 随着实践持续修订

### 风险 4：项目“看起来很强”，但 demo 不足
应对：
- 尽早准备 broken case 和 benchmark
- 所有卖点都要能演示

### 风险 5：真实机器人控制安全问题
应对：
- 明确 MVP 不做危险自治
- 真机场景严格分层审批
- 优先只做分析、建议、脚本生成和受控执行

---

## 13. 项目文档体系建议

为了保证这个项目上 GitHub 后足够专业，建议文档体系至少包含：

1. README.md
   - 项目介绍
   - 亮点
   - 快速开始
   - demo 展示
   - roadmap

2. docs/01_architecture/
   - Hermes 底座理解
   - ROS2-Agent 总体架构
   - 模块关系图

3. docs/02_product/
   - 用户画像
   - 核心场景
   - 竞品思路
   - 核心卖点

4. docs/03_workflows/
   - 环境搭建工作流
   - build 工作流
   - launch 调试工作流
   - 仿真回归工作流

5. docs/04_benchmarks/
   - 任务集设计
   - 指标定义
   - 示例结果

6. docs/05_roadmap/
   - 版本规划
   - 里程碑
   - 功能优先级

7. docs/planning/
   - 详细实施计划
   - 任务拆分
   - 阶段交付说明

---

## 14. 当前建议的下一步执行顺序

建议接下来按下面顺序推进：

1. 完成项目基础文档骨架
2. 产出 README 初稿
3. 产出 ROS2-Agent persona / SOUL 设计稿
4. 设计 profile 模板结构
5. 设计首批 skills 列表与每个 skill 的目标
6. 设计 benchmark 任务集
7. 设计 demo / broken cases 目录
8. 再进入具体实现阶段

这样能保证项目先有“战略骨架”和“展示能力”，后续实现不容易跑偏。

---

## 15. 结论

基于 Hermes Agent 来构建 ROS2-Agent，是一个非常强、非常合理、非常有潜力的方向。

真正的关键不在于“让模型更会说 ROS2”，而在于：

- 把 ROS2 的经验系统化
- 把排障路径标准化
- 把长期协作能力建立起来
- 把仿真开发、测试回归、知识沉淀做成可执行系统
- 把安全边界和可审计性做好

如果按本规划推进，ROS2-Agent 完全有机会成为一个真正让 ROS2 开发者愿意 star、愿意用、愿意贡献、愿意长期依赖的开源项目。

它的目标应该不是“一个能聊天的机器人助手”，而是：

“一个真正懂 Ubuntu 22.04 + ROS2 仿真开发生态的、会教学、会执行、会记忆、会排障、会自动化、会持续进化的专家 Agent 平台。”
