# ROS2-Agent 全局优化总计划与新对话提示词

生成时间：2026-04-30
项目路径：/home/hanhan/Desktop/ROS2-Agent
文档用途：汇总所有后续规划，供下一次新对话直接承接执行

## 0. 你现在已经拥有的规划资产

目前 advice 目录下已经形成 3 份核心规划/分析文档：

1. 严厉批判分析
- `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_严厉批判式分析与改进建议.md`

2. 下一阶段重构路线图
- `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_下一阶段重构路线图.md`

3. 第一阶段实施计划（仅规划）
- `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_第一阶段实施计划_仅规划.md`

这三份文档的关系是：
- 第 1 份负责指出问题
- 第 2 份负责给出全局重构方向
- 第 3 份负责拆出下一对话可以直接开工的第一阶段任务

## 1. 后续完整优化总安排

为了让你在新对话里直接进入优化执行，后续工作建议分成 4 个阶段推进。

### 阶段 1：真实运行时接入奠基
目标：把项目从“离线规则资产”推进到“live runtime evidence collection 雏形”

核心任务：
- runtime schema
- env/workspace/graph/tf/controller collectors
- compat adapters
- fusion diagnoser skeleton
- integration-lite tests
- live capability boundary docs

执行依据：
- `ROS2-Agent_第一阶段实施计划_仅规划.md`

### 阶段 2：融合诊断与最小行动建议
目标：把采集到的多源证据转化为优先级明确、信息增益高的诊断建议

计划方向：
- env/workspace/build/launch/runtime evidence 融合
- confidence / evidence_refs / uncertainty_gaps
- prioritized next probe
- risk_level 输出

### 阶段 3：恢复型 benchmark 与 runbook 体系
目标：让 benchmark 从“标签命中率”转向“真实恢复有效性”

计划方向：
- workflow benchmarks
- recovery benchmarks
- broken workflows
- replay manifests
- 修复前后验证链

### 阶段 4：Hermes-native 集成强化
目标：让 Hermes 在项目里不只是 profile 壳，而是能力载体

计划方向：
- tool registry / cli
- capability contract
- skill manifest / validation
- post-install validation
- MCP readiness assets
- gateway/cron demo

## 2. 下一对话应该严格遵守的边界

为了避免新对话一开局就范围失控，建议你在新对话中明确这些约束：

1. 先只执行第一阶段，不跨到第二阶段
2. 一次只做一个任务，不并行乱改
3. 先新增 collector/schema，再改旧工具
4. 每完成一个任务都要测试验证
5. 不允许顺手做文档大改、MCP、大规模目录搬迁、多 Agent 编排
6. 不允许因为“想到更好的架构”就中途扩 scope

一句话：
下一对话的目标不是“做完整个平台”，而是“把第一阶段打穿”。

## 3. 下一对话的推荐起手顺序

新对话开始后，建议执行顺序固定为：

1. 阅读三份 advice 文档
2. 创建 todo list
3. 从 `runtime_schema.py` 开始
4. 再做 `ros2_env_collect.py`
5. 再做 `ros2_workspace_collect.py`
6. 再做 `ros2_graph_collect.py`
7. 再做 `ros2_tf_collect.py`
8. 再做 `ros2_controller_collect.py`
9. 再做 `compat_adapters.py`
10. 再做 `fusion_diagnoser.py` 骨架
11. 再补 `tests/integration/`
12. 最后做 capability boundary docs

## 4. 新对话开始提示词（推荐直接复制）

下面这段就是你下一个对话框可以直接发的提示词。

---

你现在继续优化 `/home/hanhan/Desktop/ROS2-Agent` 项目。

请先完整阅读以下 3 份文档，然后严格按照其中的规划执行，不要跳步，不要擅自扩大范围：

1. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_严厉批判式分析与改进建议.md`
2. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_下一阶段重构路线图.md`
3. `/home/hanhan/Desktop/ROS2-Agent/advice/ROS2-Agent_第一阶段实施计划_仅规划.md`

本次任务目标：
只执行“第一阶段实施计划”中的内容，不允许跨阶段，不允许提前做第二阶段、第三阶段、第四阶段的工作。

强约束：
1. 先创建 todo list，并按任务顺序逐个完成
2. 一次只做一个任务，做完立即测试验证
3. 优先新增文件，不要一上来大改旧文件
4. 严格控制范围，禁止顺手重构无关模块
5. 每完成一个任务，都要汇报：改了什么、为什么这样改、怎么验证的、结果如何
6. 如遇到设计分叉，优先选择最小可用、最稳妥、最不容易引入新 bug 的方案
7. 所有实现必须围绕“先建立 live runtime evidence collection 基础”这个核心目标

本次执行顺序固定为：
1. `tools/schemas/runtime_schema.py`
2. `tools/collectors/ros2_env_collect.py`
3. `tools/collectors/ros2_workspace_collect.py`
4. `tools/collectors/ros2_graph_collect.py`
5. `tools/collectors/ros2_tf_collect.py`
6. `tools/collectors/ros2_controller_collect.py`
7. `tools/diagnosers/compat_adapters.py`
8. `tools/diagnosers/fusion_diagnoser.py`
9. `tests/integration/` 相关测试
10. `docs/00_overview/current-capability-boundaries.md`
11. `docs/03_workflows/live-runtime-debug-workflow.md`

开始前先做三件事：
- 读取三份 advice 文档
- 扫描当前项目相关目录结构
- 输出你将执行的第一阶段任务清单与顺序确认

注意：
这次不是重新规划，而是严格按既有规划进入执行。

---

## 5. 如果你想让下一对话更稳，还可以附加一句

可选附加句：
“如果某一步需要在两种设计之间选择，请默认选择更保守、更易测试、更少改动现有系统的方案，并明确说明取舍理由。”

## 6. 最后总结

酥酥已经把你下一次开新对话前最重要的规划工作都补齐啦：
- 问题批判有了
- 全局路线图有了
- 第一阶段实施计划有了
- 新对话直接可用的启动提示词也有了

你下一个对话框直接复制上面的提示词，就可以无缝进入正式优化执行啦。
