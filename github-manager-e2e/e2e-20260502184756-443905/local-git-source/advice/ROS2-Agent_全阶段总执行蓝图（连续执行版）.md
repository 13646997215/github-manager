# ROS2-Agent 全阶段总执行蓝图（连续执行版）

生成时间：2026-04-30
项目路径：/home/hanhan/Desktop/ROS2-Agent
用途：为新的执行对话提供完整阶段蓝图、阶段门禁、连续工作规则与最终收尾标准

## 0. 总体目标

让新的对话执行代理从当前 ROS2-Agent 状态出发，连续完成从第一阶段到第四阶段的全部优化工作，并在完成后完成：
- 全量验证
- 文档收口
- 能力边界校正
- 最终总结与下一步建议

这个执行蓝图服务于“用户不想参与中间过程”的模式，因此必须强调：
- 连续执行
- 不中途停下来征求低价值确认
- 每个阶段自带验证和收尾
- 只有遇到真正高风险、超范围、破坏性操作时才停

## 1. 全阶段文档清单

执行前必须读取这些文档：

1. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_严厉批判式分析与改进建议.md`
2. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_下一阶段重构路线图.md`
3. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_第一阶段实施计划_仅规划.md`
4. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_第二阶段实施计划_仅规划.md`
5. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_第三阶段实施计划_仅规划.md`
6. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_第四阶段实施计划_仅规划.md`
7. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_全局优化总计划与新对话提示词.md`
8. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_全阶段总执行蓝图（连续执行版）.md`

## 2. 阶段划分

### 阶段 1：真实运行时接入奠基
目标：collector + schema + integration-lite + capability boundary docs

### 阶段 2：融合诊断与最小行动建议
目标：diagnosis schema + diagnosers + fusion prioritization + workflow diagnosis tests

### 阶段 3：workflow/recovery benchmark 与 runbook 体系
目标：benchmark taxonomy + workflow/recovery cases + runbooks + evidence packs + reporting upgrade

### 阶段 4：Hermes-native 平台收口
目标：registry/cli + capability contract + skill manifest + install/post-install validation + MCP readiness + gateway/cron demo + README 收口

## 3. 连续执行规则

新的执行对话必须遵守这些规则：

1. 先读完整规划文档，再进入执行
2. 建立一个覆盖全部阶段的 todo list
3. 每次只允许一个任务处于 in_progress
4. 同一阶段完成前，不提前进入下一阶段
5. 每阶段结束时必须进行阶段验证
6. 每阶段结束时必须更新执行日志
7. 每阶段结束时必须检查是否满足进入下一阶段的 gate
8. 除非遇到真正高风险操作，否则不中途停下来问“要不要继续”
9. 对于目录结构大改、危险 shell 操作、破坏性变更、系统级安装等高风险行为，必须单独停下并说明原因

## 4. 必须创建的执行日志

新的执行对话开始后，第一批工作之一必须是创建：
- `/home/hanhan/Desktop/ROS2-Agent/docs/planning/EXECUTION_LOG_STAGE_REBUILD.md`

日志结构至少包含：
- 当前日期/阶段
- 已完成任务
- 修改文件列表
- 测试/验证结果
- 当前项目状态
- 下一阶段入口条件
- 遗留问题

要求：
- 每个阶段完成后更新一次
- 遇到重要分叉决策时也要更新

## 5. 全阶段门禁（Gates）

### Gate A：阶段 1 完成门禁
进入阶段 2 前必须满足：
- runtime schema 已落地
- env/workspace/graph/tf/controller collectors 已完成
- integration-lite tests 已存在并可运行
- capability boundary docs 已更新
- 第一阶段相关测试通过

### Gate B：阶段 2 完成门禁
进入阶段 3 前必须满足：
- diagnosis schema 已落地
- 单领域 diagnosers 已完成
- fusion diagnoser 可输出 prioritized causes
- workflow diagnosis tests 已存在并通过
- 第二阶段文档更新完成

### Gate C：阶段 3 完成门禁
进入阶段 4 前必须满足：
- benchmark taxonomy 已重构
- workflow benchmark 已存在
- recovery benchmark 设计与首批案例已存在
- runbooks / broken workflows 已成型
- evidence packs / replay manifests 已可导出
- 第三阶段测试通过

### Gate D：阶段 4 完成门禁
进入最终收尾前必须满足：
- registry / cli 可用
- capability contract 已完成
- skill manifest / validation 已完成
- post-install validation 已完成
- MCP readiness assets 已存在
- gateway/cron demo 资产已完成
- README / quickstart / docs 已收口
- full quality gate 通过

## 6. 各阶段结束时必须做的事情

### 每阶段结束的固定动作
1. 运行本阶段相关测试
2. 运行必要的回归测试
3. 更新 execution log
4. 更新 todo 状态
5. 核查阶段 gate
6. 只有 gate 通过才进入下一阶段

## 7. 最终收尾标准

全部阶段完成后，新的执行对话必须完成以下收尾工作：

1. 运行完整测试与验证链
至少包括：
- repository validation
- tests/tools
- tests/workflows
- tests/collectors
- tests/diagnosers
- tests/integration
- tests/recovery（若本次已建立）
- benchmark/report pipeline
- final quality gate

2. 进行最终文档收口
- README
- README_EN
- quickstart
- developer-setup
- capability matrix
- current capability boundaries
- final platform capability summary

3. 输出最终项目状态总结
必须包含：
- 完成了哪些阶段
- 新增了哪些核心模块
- 哪些能力已 live
- 哪些仍是 prototype/demo/readiness
- 剩余 open questions

4. 输出最终交付清单
必须包含：
- 新增文件
- 修改文件
- 测试结果
- benchmark/report 结果
- 用户可从哪里开始使用

## 8. 范围控制要求

为了防止执行对话跑偏，必须明确：

### 可以主动连续做的事情
- 代码新增/修改
- 测试编写与运行
- 文档更新
- 规划文档引用
- 目录结构内的合理演进
- benchmark/report 资产升级

### 不可擅自做的事情
- 系统级危险安装
- 删除大量现有资产
- 改动与 ROS2-Agent 优化无关的仓库外文件
- 引入超出项目定位的大型新子系统
- 跳过阶段 gate 直接做终局包装

## 9. 质量优先规则

新的执行对话必须始终遵守：
1. 先最小可用，再增强
2. 先验证，再宣称完成
3. 先兼容，再替换
4. 先证据采集，再推理扩张
5. 先真实价值，再平台包装

## 10. 结束时的最终回复格式建议

全部工作完成后，新的执行对话最终回复应至少包含：
1. 全阶段完成状态
2. 关键成果摘要
3. 核心新增能力
4. 测试与验证结果
5. 剩余局限
6. 建议的后续演进方向（若仍有）
7. 关键文档与入口路径

## 11. 这份蓝图的核心精神

这不是一次“做一点点优化”的任务，而是一轮完整的平台重构与收口。

因此新的执行对话必须：
- 像项目负责人一样连续推进
- 像审稿人一样不断验证
- 像产品经理一样持续校正能力边界
- 像工程师一样把最终交付闭环做完

只有做到这些，才算真正“完成所有规划中的任务和要求，并完成收尾工作”。
