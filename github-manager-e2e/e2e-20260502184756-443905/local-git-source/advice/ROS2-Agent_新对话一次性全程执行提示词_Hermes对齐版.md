# ROS2-Agent 新对话一次性全程执行提示词（Hermes 对齐版）

下面这段提示词，是为“新开一个对话框后，让新的 agent 严格读取现有规划资产，然后一次性连续完成 ROS2-Agent 向 Hermes 级能力对齐重构，长时间工作不停止，直到用户可以体验承诺范围内的全部功能”而写的。可直接复制使用。

--------------------------------------------------
你现在开始对 `/home/hanhan/Desktop/ROS2-Agent` 项目进行一次完整、连续、不中途停下的系统性重构执行。

你的任务不是重新规划，而是严格读取现有规划资产，然后从阶段 A 一直执行到阶段 F 全部完成，最后完成全量验证、文档收口、执行日志更新、最终总结与交付清单输出。

一、执行前必须读取的文档

请先完整阅读以下文档，禁止跳过：

1. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_严厉批判式分析与改进建议.md`
2. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_下一阶段重构路线图.md`
3. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_第一阶段实施计划_仅规划.md`
4. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_第二阶段实施计划_仅规划.md`
5. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_第三阶段实施计划_仅规划.md`
6. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_第四阶段实施计划_仅规划.md`
7. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_全局优化总计划与新对话提示词.md`
8. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_全阶段总执行蓝图（连续执行版）.md`
9. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_面向Hermes级能力对齐的全量重构总规划.md`
10. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_Hermes对齐版全阶段执行蓝图（连续执行版）.md`
11. `/home/hanhan/Desktop/ROS2-Agent/docs/00_overview/current-capability-boundaries.md`
12. `/home/hanhan/Desktop/ROS2-Agent/docs/00_overview/final-platform-capability-summary.md`
13. `/home/hanhan/Desktop/ROS2-Agent/docs/01_architecture/capability_contract.md`

二、你的总体目标

你要把这个项目从当前状态连续推进到六个阶段全部完成：

### 阶段 A：统一命令模型与执行引擎
完成：
- CommandSpec / CommandResult / CommandStatus / NextAction schema
- registry 元数据重构
- CLI 与 TUI 共用执行引擎
- 轻量命令统一返回结构化结果
- 去掉“脚本直接 print JSON”的分裂执行方式

### 阶段 B：Hermes 风格基础命令族落地
完成：
- help
- status
- doctor
- inspect
- logs
- history
- profile
- validate
- quality
- runbook
- workflow
- report
- settings/config（至少只读展示与解释级别）

### 阶段 C：ROS2 专项能力命令升维
完成：
- collect / diagnose / inspect / doctor / suggest-fix / trace / replay / compare 命令族
- graph/tf/controller/workspace/launch 的用户导向结果视图
- fusion diagnosis 高层入口化
- 关键命令具备 summary / highlights / next_actions / raw_output

### 阶段 D：TUI 工作台升级
完成：
- 左侧命令目录
- 中间命令详情
- 右侧执行结果 / 原始输出 / 建议
- 命令搜索
- 最近运行历史
- 最近错误
- 长任务状态
- 重量级命令外部执行引导
- 键鼠交互统一

### 阶段 E：平台层与安装体验收口
完成：
- profile install / verify / show
- post-install validation
- README / README_EN / quickstart / developer-setup / capability boundaries / final summary 收口
- MCP readiness / gateway demo / cron demo 资产整理
- deployment readme 收口

### 阶段 F：最终体验闭环与交付
完成：
- 全量验证链
- 关键体验路径人工验证
- 最终执行日志
- 最终交付总结
- 剩余 open questions
- 明确 live / prototype / demo / readiness 边界

三、工作模式要求

你必须连续工作，直到全部阶段完成并完成最终收尾。不要在每个阶段结束后停下来问我“是否继续”。

只有遇到以下情况才允许停下来向我请求确认：
1. 会进行高风险、破坏性、不可逆操作
2. 会修改仓库外的重要系统文件
3. 会进行系统级安装、卸载或环境级危险变更
4. 发现规划与现实严重矛盾，继续执行会高概率造成错误

除以上情况外，不允许中途停下等待我的指示。

四、执行纪律

1. 先创建覆盖全部阶段的 todo list
2. 同一时间只允许一个任务是 in_progress
3. 每完成一个任务都要：
   - 更新 todo
   - 运行对应测试/验证
   - 更新执行日志
   - 简要汇报进展
4. 每个阶段结束时必须：
   - 运行阶段验证
   - 更新执行日志
   - 检查阶段 gate
5. 没通过 gate 不允许进入下一阶段
6. 优先最小可用、可验证、低风险实现
7. 优先能力层统一，再做 UI 包装
8. 先真实价值，再体验打磨
9. 不要只做几行原始代码输出
10. 不要只做 UI 不做能力闭环

五、执行日志要求

你开始执行后，必须尽快创建并持续维护：
`/home/hanhan/Desktop/ROS2-Agent/docs/planning/EXECUTION_LOG_HERMES_ALIGNMENT.md`

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

每个阶段结束时必须更新一次。

六、阶段门禁（必须遵守）

### Gate A：阶段 A -> 阶段 B
进入阶段 B 前必须确认：
- 统一命令模型已落地
- registry 已支持 execution_mode / maturity / risk / next actions 元数据
- CLI 与 TUI 共用执行引擎
- 轻量命令结果结构统一
- 对应测试通过

### Gate B：阶段 B -> 阶段 C
进入阶段 C 前必须确认：
- Hermes 风格基础命令族已建立
- help/status/logs/history/profile/validate/runbook/workflow/report 至少最小闭环
- 新命令测试通过
- 文档已更新到新命令族视角

### Gate C：阶段 C -> 阶段 D
进入阶段 D 前必须确认：
- ROS2 专项命令族已升维完成
- 关键命令具备 summary / highlights / next_actions / raw_output
- 用户不需要看纯 JSON 才能理解结果
- workflow / diagnosis / integration tests 通过

### Gate D：阶段 D -> 阶段 E
进入阶段 E 前必须确认：
- TUI 工作台已形成
- TUI 中可选择、执行、查看结果、查看建议
- 历史/错误/输出面板基本闭环
- 人工体验链关键路径通过

### Gate E：阶段 E -> 阶段 F
进入阶段 F 前必须确认：
- profile/install/validation/docs 已收口
- README / quickstart / deployment readme 与实际行为一致
- MCP/gateway/cron 资产边界说明清楚
- full quality gate 基本通过

### Gate F：最终收尾门禁
最终完成前必须确认：
- `/home/hanhan/Desktop/.ros2-agent/ros2-agent` 可直接体验
- 承诺范围内命令可体验
- 全量测试/验证链通过
- 执行日志与最终交付说明完成

七、你开始执行时的顺序

请按以下顺序开始：
1. 读取全部规划文档
2. 扫描项目目录与现有关键文件
3. 创建全阶段 todo list
4. 创建执行日志文件
5. 从阶段 A 开始逐项执行
6. 阶段 A 通过 Gate A 后再进入阶段 B
7. 阶段 B 通过 Gate B 后再进入阶段 C
8. 阶段 C 通过 Gate C 后再进入阶段 D
9. 阶段 D 通过 Gate D 后再进入阶段 E
10. 阶段 E 通过 Gate E 后再进入阶段 F
11. 阶段 F 完成后进入最终收尾

八、最终收尾要求

当六个阶段全部完成后，你必须继续完成以下收尾工作，不能只停在“功能做完”：

1. 运行完整验证链
至少包括：
- repository validation
- tests/tools
- tests/collectors
- tests/diagnosers
- tests/workflows
- tests/recovery
- tests/integration
- TUI tests
- command capture / command result tests
- benchmark/report pipeline
- final quality gate

2. 文档最终收口
至少检查并必要时更新：
- README.md
- README_EN.md
- docs/00_overview/quickstart.md
- docs/00_overview/developer-setup.md
- docs/00_overview/current-capability-boundaries.md
- docs/00_overview/final-platform-capability-summary.md
- docs/02_product/capability_matrix.md
- `/home/hanhan/Desktop/.ros2-agent/DEPLOYMENT_README.md`

3. 更新执行日志为最终状态

4. 输出最终交付总结，必须包含：
- 六个阶段分别完成了什么
- 新增/修改了哪些核心文件
- 哪些能力现在已 live
- 哪些能力仍然只是 prototype / demo / readiness
- 全量测试与验证结果
- 剩余 open questions
- 用户从哪里开始使用这个优化后的项目

九、特别强调

- 不要重新规划
- 不要中途频繁停下来问我要不要继续
- 不要只做 TUI 壳子
- 不要只做几行 JSON 输出
- 不要因为像 Hermes 就盲目抄一堆与 ROS2 无关的能力
- 不要跳过测试和 gate
- 不要把 demo/readiness 写成 production-ready
- 不要只做能力不做最终收口
- 不要只做功能不校正文档表述

十、你的第一条执行回复必须做什么

你的第一条执行回复必须包含：
1. 已读取哪些规划文档
2. 对全阶段执行目标的简要确认
3. 你建立的全阶段 todo list
4. 你准备创建/维护的执行日志路径
5. 你即将开始的第一个具体任务

现在开始执行，不要重新规划，直接进入全阶段连续重构流程。
