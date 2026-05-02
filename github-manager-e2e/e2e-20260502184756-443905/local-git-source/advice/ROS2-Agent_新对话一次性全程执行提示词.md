# ROS2-Agent 新对话一次性全程执行提示词

下面这段提示词，是为“新开一个对话框后，让新的 agent 按完整规划持续高质量工作直到全部优化完成并收尾”而写的。可直接复制使用。

---

你现在开始对 `/home/hanhan/Desktop/ROS2-Agent` 项目进行一次完整、连续、不中途停下的系统性优化执行。

你的任务不是重新规划，而是严格读取现有规划资产，然后从第一阶段一直执行到第四阶段全部完成，最后完成全量验证、文档收口、执行日志更新、最终总结与交付清单输出。

## 一、执行前必须读取的文档

请先完整阅读以下文档，禁止跳过：

1. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_严厉批判式分析与改进建议.md`
2. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_下一阶段重构路线图.md`
3. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_第一阶段实施计划_仅规划.md`
4. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_第二阶段实施计划_仅规划.md`
5. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_第三阶段实施计划_仅规划.md`
6. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_第四阶段实施计划_仅规划.md`
7. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_全局优化总计划与新对话提示词.md`
8. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_全阶段总执行蓝图（连续执行版）.md`

## 二、你的总体目标

你要把这个项目从当前状态连续推进到四个阶段全部完成：

### 阶段 1：真实运行时接入奠基
完成：
- runtime schema
- env/workspace/graph/tf/controller collectors
- compat adapters
- fusion diagnoser skeleton
- integration-lite tests
- capability boundary docs

### 阶段 2：融合诊断与最小行动建议
完成：
- diagnosis schema
- env/workspace/build/launch/runtime diagnosers
- fusion diagnoser prioritization
- confidence / evidence_refs / uncertainty_gaps / risk_level
- workflow diagnosis tests
- fusion diagnosis workflow docs

### 阶段 3：workflow/recovery benchmark 与 runbook 体系
完成：
- benchmark taxonomy 重构
- workflow benchmarks
- recovery benchmark 设计与首批案例
- evidence packs / replay manifests
- examples 升级为 demo_workflows / broken_workflows / runbooks
- workflow/recovery tests
- reporting 与教学文档升级

### 阶段 4：Hermes-native 平台收口
完成：
- tool registry / cli
- capability contract
- skill manifest / validation pipeline
- install / post-install validation upgrade
- MCP readiness assets
- gateway/cron demo 资产
- README / quickstart / developer-setup / final quality gate 收口

## 三、工作模式要求

你必须连续工作，直到全部阶段完成并完成最终收尾。不要在每个阶段结束后停下来问我“是否继续”。

只有遇到以下情况才允许停下来向我请求确认：
1. 会进行高风险、破坏性、不可逆操作
2. 会修改仓库外的重要系统文件
3. 会进行系统级安装、卸载或环境级危险变更
4. 发现规划与现实严重矛盾，继续执行会高概率造成错误

除以上情况外，不允许中途停下等待我的指示。

## 四、执行纪律

1. 先创建覆盖全部阶段的 todo list
2. 同一时间只允许一个任务是 in_progress
3. 每完成一个任务都要：
   - 更新 todo
   - 运行对应测试/验证
   - 简要汇报进展
4. 每个阶段结束时必须：
   - 运行阶段验证
   - 更新执行日志
   - 检查阶段 gate
5. 没通过 gate 不允许进入下一阶段
6. 优先最小可用、可验证、低风险实现
7. 优先新增文件，不要过早大改旧文件
8. 先兼容，再替换
9. 先证据采集，再推理扩张
10. 先真实价值，再平台包装

## 五、执行日志要求

你开始执行后，必须尽快创建并持续维护：
`/home/hanhan/Desktop/ROS2-Agent/docs/planning/EXECUTION_LOG_STAGE_REBUILD.md`

日志必须持续记录：
- 当前阶段
- 已完成任务
- 修改文件
- 测试结果
- 阶段 gate 状态
- 当前项目状态
- 下一步任务
- 遗留问题

每个阶段结束时必须更新一次。

## 六、阶段门禁（必须遵守）

### Gate A：阶段 1 -> 阶段 2
进入阶段 2 前必须确认：
- runtime schema 已落地
- env/workspace/graph/tf/controller collectors 已完成
- integration-lite tests 已存在并可运行
- capability boundary docs 已更新
- 第一阶段测试通过

### Gate B：阶段 2 -> 阶段 3
进入阶段 3 前必须确认：
- diagnosis schema 已落地
- env/workspace/build/launch/runtime diagnosers 已完成
- fusion diagnoser 可输出 prioritized causes
- workflow diagnosis tests 已通过
- 第二阶段文档已更新

### Gate C：阶段 3 -> 阶段 4
进入阶段 4 前必须确认：
- benchmark taxonomy 已重构
- workflow benchmark 已建立
- recovery benchmark 设计与首批案例已建立
- runbooks / broken workflows 已成型
- evidence packs / replay manifests 可导出
- 第三阶段测试通过

### Gate D：阶段 4 -> 最终收尾
进入最终收尾前必须确认：
- registry / cli 可用
- capability contract 已完成
- skill manifest / validation 已完成
- post-install validation 已完成
- MCP readiness assets 已存在
- gateway/cron demo 资产已完成
- README / docs 已收口
- full quality gate 通过

## 七、你开始执行时的顺序

请按以下顺序开始：
1. 读取全部规划文档
2. 扫描项目目录与现有关键文件
3. 创建全阶段 todo list
4. 创建执行日志文件
5. 从阶段 1 开始逐项执行
6. 阶段 1 通过 Gate A 后再进入阶段 2
7. 阶段 2 通过 Gate B 后再进入阶段 3
8. 阶段 3 通过 Gate C 后再进入阶段 4
9. 阶段 4 通过 Gate D 后进入最终收尾

## 八、最终收尾要求

当四个阶段全部完成后，你必须继续完成以下收尾工作，不能只停在“功能做完”：

1. 运行完整验证链
至少包括：
- repository validation
- tests/tools
- tests/workflows
- tests/collectors
- tests/diagnosers
- tests/integration
- tests/recovery（若已建立）
- benchmark/report pipeline
- final full quality gate

2. 文档最终收口
至少检查并必要时更新：
- README.md
- README_EN.md
- docs/00_overview/quickstart.md
- docs/00_overview/developer-setup.md
- docs/00_overview/status.md
- docs/02_product/capability_matrix.md
- docs/00_overview/current-capability-boundaries.md
- docs/00_overview/final-platform-capability-summary.md

3. 更新执行日志为最终状态

4. 输出最终交付总结，必须包含：
- 四个阶段分别完成了什么
- 新增/修改了哪些核心文件
- 哪些能力现在已经 live
- 哪些能力仍然只是 prototype / demo / readiness
- 全量测试与验证结果
- 剩余 open questions
- 用户从哪里开始使用这个优化后的项目

## 九、特别强调

- 不要重新规划
- 不要中途频繁停下来问我要不要继续
- 不要因为想到更大架构就扩 scope
- 不要跳过测试和 gate
- 不要只做代码不做收尾
- 不要只做功能不校正文档表述
- 不要把 demo/readiness 写成 production-ready

## 十、你的第一条执行回复应该做什么

你的第一条执行回复必须包含：
1. 已读取哪些规划文档
2. 对全阶段执行目标的简要确认
3. 你建立的全阶段 todo list
4. 你准备创建/维护的执行日志路径
5. 你即将开始的第一个具体任务

现在开始执行，不要重新规划，直接进入全阶段连续优化流程。

---
