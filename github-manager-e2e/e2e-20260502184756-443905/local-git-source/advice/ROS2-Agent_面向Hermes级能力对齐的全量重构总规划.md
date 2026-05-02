# ROS2-Agent 向 Hermes 级能力对齐的全量重构总规划

生成时间：2026-05-01
项目路径：/home/hanhan/Desktop/ROS2-Agent
规划性质：只规划，不在本文件中执行实现
目标级别：尽可能接近 Hermes 的“能力型命令系统 + 统一工作台 + 持续执行闭环”，但保持 ROS2 专项定位，不盲目复制与 ROS2 无关的 Hermes 通用生态能力。

> 这份规划是给“新的执行对话”使用的总蓝图。新的执行对话必须严格按本文档执行，不得把本文档降级理解为普通的 UI 修修补补任务。

--------------------------------------------------
一、最终目标（必须对齐的产品形态）
--------------------------------------------------

ROS2-Agent 的最终目标不是“带 TUI 的 ROS2 工具列表”，而是：

一个 ROS2 专属、Hermes 风格的 agent 工作台，具备：
1. Hermes 风格命令体系
2. 可持续执行的命令工作流
3. 面向用户可理解的执行摘要与结果视图
4. 多阶段诊断 / 采集 / 推理 / 建议 / 验证闭环
5. 统一的 CLI + TUI + profile + validation + workflow + runbook + history 能力面
6. 用户打开后即可“选命令、执行、看到结果、继续下一步”，而不是只看到原始 JSON 或几行代码

换句话说，最终交付物必须尽量接近“ROS2 版 Hermes”，而不是“原型型 launcher”。

--------------------------------------------------
二、必须明确的产品边界
--------------------------------------------------

### 1. 要尽量对齐 Hermes 的部分
- 命令系统的组织方式
- 执行反馈体验
- 统一入口
- 带状态的命令结果展示
- 命令闭环与下一步建议
- profile / install / validation / doctor / inspect / logs / history / runbook / workflow 这些能力层概念
- 用户不需要懂底层脚本也能直接用

### 2. 不必硬复制 Hermes 的部分
- 与 ROS2 无关的通用社交/消息平台能力
- 与 ROS2 无关的通用媒体/内容工作流
- 与 ROS2 无关的跨平台协作生态

### 3. ROS2-Agent 应保留的专属定位
- 面向 ROS2 / 机器人 / workspace / graph / tf / ros2_control / launch / build / bench / recovery
- 面向现场问题诊断、运行时证据采集、教学复演、故障回放、恢复建议
- 面向工程工作流，而不是做成泛用聊天工具

--------------------------------------------------
三、当前差距诊断（为什么现在“不像 Hermes”）
--------------------------------------------------

当前项目与目标相比存在这些差距：

1. 命令还是“脚本调用型”，不是“能力命令型”
2. TUI 仍偏 launcher，不是工作台
3. 结果展示过于原始，用户无法感知“已执行 / 已成功 / 下一步是什么”
4. 命令分类虽然有了，但缺少 Hermes 风格的高级能力族
5. 长任务、重量级任务、只读任务、危险任务的策略没有完全分层
6. 执行历史、结果复用、最近任务、错误追踪还不完整
7. profile/install/validation 虽有资产，但还没有达到用户视角的统一使用体验
8. docs 仍偏工程文档，不够用户导向
9. TUI / CLI / docs / validation / runbook / workflow 还没有完全统一成一个产品叙事

--------------------------------------------------
四、最终能力地图（目标能力清单）
--------------------------------------------------

新的执行对话必须以这张“目标能力地图”为实现终点。

### A. 核心入口层
1. ros2-agent
2. ros2-agent --text-ui
3. ros2-agent --no-ui <command>
4. 部署入口 /home/hanhan/Desktop/.ros2-agent/ros2-agent

### B. Hermes 风格基础命令族
1. help
2. status
3. doctor
4. inspect
5. logs
6. history
7. profile
8. quality
9. validate
10. runbook
11. workflow
12. benchmark
13. report
14. settings / config（至少是只读展示与解释级别）

### C. ROS2 专项能力命令族
1. collect env
2. collect workspace
3. collect graph
4. collect tf
5. collect controller
6. diagnose env
7. diagnose workspace
8. diagnose runtime
9. diagnose tf
10. diagnose controller
11. diagnose fusion
12. inspect workspace
13. inspect launch
14. inspect graph
15. inspect tf
16. inspect controller
17. doctor ros2
18. doctor workspace
19. doctor launch
20. doctor tf
21. doctor control
22. suggest-fix <domain>
23. replay evidence
24. replay workflow
25. compare snapshots
26. trace failure

### D. 工作流 / 教学 / 复演能力
1. runbook list
2. runbook show
3. workflow list
4. workflow run
5. broken workflow walkthrough
6. evidence pack export
7. replay manifest export
8. benchmark recovery view
9. benchmark workflow run
10. report summary

### E. 平台化能力
1. registry
2. capability contract
3. post-install validation
4. profile install/verify/show
5. MCP readiness docs/assets
6. gateway demo assets
7. cron demo assets
8. skill manifest / validation pipeline

### F. TUI 工作台能力
1. 左侧命令目录
2. 中间命令详情面板
3. 右侧执行结果 / 日志面板
4. 状态栏
5. 命令搜索
6. 最近运行历史
7. 最近错误
8. 下一步建议面板
9. 命令分类与子命令浏览
10. 长任务状态提示
11. 重量级命令外部执行指引

--------------------------------------------------
五、总体架构重构原则
--------------------------------------------------

新的执行对话必须严格遵守：

1. 先能力层，后 UI 包装
2. 先统一命令模型，后逐个命令接入
3. 先轻量命令闭环，后重量级命令分层
4. 先 TUI 内可见结果，后优化交互细节
5. 先用户可理解摘要，后保留原始 JSON/日志
6. 先稳定、再花哨
7. 先真实可用，再模仿 Hermes 外观

--------------------------------------------------
六、六大阶段总路线（新版本）
--------------------------------------------------

这次不是旧的四阶段 collector/diagnoser 重构，而是在其基础上做 Hermes 风格产品化重构。

### 阶段 A：统一命令模型与执行引擎
目标：让所有命令先拥有统一的内部表示与统一执行返回结构。

必须完成：
- CommandSpec / CommandResult / CommandStatus / NextAction schema
- 命令注册元数据统一化
- CLI 与 TUI 共用同一执行引擎
- 所有轻量命令能返回结构化结果（summary / raw_output / next_actions / risk / exit_code）
- 把当前“函数直接 print JSON”的方式重构为“返回结构化结果对象”

阶段完成后用户应感知到：
- 不同命令结果展示风格一致
- 不再是某些命令一坨 JSON、某些命令一句话

Gate A：
- 核心轻量命令全部返回统一结构化结果
- TUI 与 CLI 共用执行引擎
- tests/tools 新增统一执行结果测试通过

### 阶段 B：Hermes 风格基础命令族落地
目标：补齐像 Hermes 一样“可管理、可检查、可追踪”的基础能力。

必须完成：
- help / status / doctor / inspect / logs / history / profile / validate / quality / runbook / workflow / report 命令族
- history 最低要求：记录最近运行过的命令、时间、exit_code、摘要
- logs 最低要求：查看最近执行日志与错误
- inspect / doctor 命令族对 ROS2 各域给出用户可理解摘要
- 所有命令都能给 next_actions

Gate B：
- 基础命令族在 TUI / CLI 中都能跑通
- history/logs 至少具备最小闭环
- 新增命令测试通过

### 阶段 C：ROS2 专项能力命令升维
目标：把 collect/diagnose 从脚本封装升级成真正的 ROS2 专项 agent 能力命令。

必须完成：
- collect/diagnose/inspect/doctor/suggest-fix/trace/replay/compare 体系
- 结果不只给原始数据，还给：
  - 摘要
  - 重点问题
  - 风险级别
  - 下一步建议
- fusion diagnosis 成为更高层入口而不是孤立命令
- 对 graph/tf/controller/workspace/launch 的用户导向展示完善

Gate C：
- 关键 ROS2 命令在 TUI 内一眼能看懂结果
- 用户不需要看原始 JSON 才能理解命令结果
- workflow diagnosis / integration tests / domain tests 通过

### 阶段 D：TUI 从 launcher 升级为工作台
目标：把 UI 从菜单系统升级成“真正可用的 Hermes 风格工作台”。

必须完成：
- 左中右三栏工作台稳定
- 输出面板升级为结果卡片 + 原始输出区
- 命令搜索
- 最近运行历史
- 最近错误
- 下一步建议区
- 状态栏完整显示执行态
- 重量级命令给清晰外部执行指引
- 键鼠交互完全统一

Gate D：
- 用户在 TUI 内能完成一次完整工作流，不需要“猜”命令有没有执行
- TUI 体验验证通过
- 部署环境 smoke + 关键人工体验路径通过

### 阶段 E：平台层与安装体验收口
目标：把 profile/install/validation/MCP/gateway/cron/readme 等平台面统一成真正可交付的产品入口。

必须完成：
- profile install/verify/show
- post-install validation
- README / quickstart / developer-setup / capability boundaries / final summary 全部改成新产品叙事
- MCP readiness assets / gateway demo / cron demo 明确“可用级别”
- 不夸大 demo 为 production-ready

Gate E：
- 全套文档与入口路径一致
- 用户从 README 可以一路进入部署与体验
- full quality gate 通过

### 阶段 F：最终体验闭环与交付
目标：确保“用户真的可以体验所有已承诺能力”。

必须完成：
- 全量验证链
- 关键命令人工体验清单
- 执行日志最终收口
- 最终交付报告
- 剩余 open questions
- 明确哪些能力 live / prototype / demo / readiness

Gate F：
- 用户能够在 /home/hanhan/Desktop/.ros2-agent/ros2-agent 中稳定体验承诺范围内的全部能力
- 最终文档与执行日志收口完成

--------------------------------------------------
七、必须重构的关键技术件
--------------------------------------------------

### 1. 命令执行模型
新增/重构：
- tools/command_runtime.py
- tools/command_result.py
- tools/command_dispatch.py

统一结果结构建议至少包含：
- command_id
- title
- status
- exit_code
- summary
- highlights
- next_actions
- raw_output
- error_text
- risk_level
- execution_mode (inline / external / long_running)

### 2. TUI 展示模型
新增/重构：
- tools/tui_models.py
- tools/tui_presenters.py
- tools/tui_history_store.py

### 3. 历史与日志
新增：
- .artifacts/history/*.jsonl 或 docs/runtime_logs/ 结构化日志
- 最近执行记录索引
- 最近错误索引

### 4. 命令族组织
重构 registry，使其支持：
- category
- subcategory
- execution_mode
- maturity
- risk_level
- supports_tui_inline
- supports_external_only
- summary_builder

--------------------------------------------------
八、文档交付清单（新的执行对话必须产出）
--------------------------------------------------

必须新增或重写这些文档：
1. docs/planning/EXECUTION_LOG_HERMES_ALIGNMENT.md
2. docs/00_overview/quickstart.md
3. docs/00_overview/developer-setup.md
4. docs/00_overview/current-capability-boundaries.md
5. docs/00_overview/final-platform-capability-summary.md
6. docs/02_product/capability_matrix.md
7. README.md
8. README_EN.md
9. /home/hanhan/Desktop/.ros2-agent/DEPLOYMENT_README.md
10. docs/03_workflows/hermes-style-command-workflows.md

--------------------------------------------------
九、必须创建的执行日志
--------------------------------------------------

新的执行对话一开始必须创建：
- /home/hanhan/Desktop/ROS2-Agent/docs/planning/EXECUTION_LOG_HERMES_ALIGNMENT.md

日志必须持续记录：
- 当前阶段
- 当前 in_progress 任务
- 已完成任务
- 修改文件
- 测试结果
- 人工体验结果
- Gate 状态
- 当前系统可体验能力
- 剩余问题
- 下一步任务

--------------------------------------------------
十、测试与验证要求
--------------------------------------------------

至少必须覆盖：
1. tests/tools
2. tests/collectors
3. tests/diagnosers
4. tests/workflows
5. tests/recovery
6. tests/integration
7. TUI 交互测试
8. TUI 结果展示测试
9. command capture / command result schema 测试
10. deployment smoke tests

必须新增的测试方向：
- 全命令目录至少返回结构化结果或明确指导语
- Enter 后 TUI 结果面板非空
- 关键命令在 TUI 中显示 summary + raw_output
- history/logs 至少写入最小记录
- heavyweight commands 的 TUI 提示正确

--------------------------------------------------
十一、风险控制要求
--------------------------------------------------

新的执行对话必须遵守：
1. 不可把未完成的 demo 说成 Hermes 级完整产品
2. 不可把 readiness 资产说成 production-ready
3. 不可跳过测试和人工体验链
4. 不可只做 UI，不做命令能力重构
5. 不可只做命令能力，不做最终收口
6. 不可频繁停下问“要不要继续”
7. 只有涉及高风险系统修改时才允许停下确认

--------------------------------------------------
十二、新对话必须遵守的执行纪律
--------------------------------------------------

1. 先读现有 advice 文档与本规划文档
2. 建立覆盖全部阶段的 todo list
3. 同一时间只允许一个任务 in_progress
4. 每完成一个任务必须：
   - 更新 todo
   - 跑测试/验证
   - 更新执行日志
5. 每个阶段结束必须检查 gate
6. gate 不通过不得进入下一阶段
7. 最终必须完成完整收尾，不能停在“功能大概有了”

--------------------------------------------------
十三、最终完成定义（Definition of Done）
--------------------------------------------------

只有同时满足以下条件，才算“用户可以体验所有承诺范围内内容”：

1. /home/hanhan/Desktop/.ros2-agent/ros2-agent 可以稳定启动
2. TUI 内可选择、执行、查看结果、查看建议
3. 基础命令族与 ROS2 专项命令族都能闭环
4. 关键命令不再只显示几行原始代码而无解释
5. 文档、部署说明、能力边界、最终总结一致
6. 全量测试与质量门通过
7. 执行日志最终收口

--------------------------------------------------
十四、给新的执行对话的核心提醒
--------------------------------------------------

这不是“继续修一点 TUI 交互细节”的任务。
这是：
把 ROS2-Agent 从“原型型 ROS2 launcher”升级为“尽量接近 Hermes 级能力的 ROS2 专属 agent 工作台”的完整平台重构任务。

新的执行对话必须像项目负责人一样连续工作，长时间不停止，直到所有规划完成并完成最终收尾。
