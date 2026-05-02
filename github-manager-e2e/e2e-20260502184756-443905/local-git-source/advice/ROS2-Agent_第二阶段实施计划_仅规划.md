# ROS2-Agent 第二阶段实施计划（仅规划，不执行）

生成时间：2026-04-30
项目路径：/home/hanhan/Desktop/ROS2-Agent
计划性质：纯规划文档，禁止在本计划阶段直接开始实现

> For Hermes: 只有当第一阶段全部完成并验证通过后，才进入本阶段执行。

**Goal:** 在第一阶段建立 live runtime evidence collection 基础后，继续构建多证据融合诊断层，让 ROS2-Agent 从“会采集”升级为“会高质量收敛问题面并给出最小行动建议”。

**Architecture:** 第二阶段以 schema 驱动诊断为核心，围绕 env/workspace/build/launch/runtime 等证据建立统一 finding/candidate/recommendation 模型，并引入 fusion diagnoser、risk-aware next probe、evidence refs、uncertainty gaps。该阶段重点是诊断质量，不追求广度扩张。

**Tech Stack:** Python 3.10+, 第一阶段 runtime schema, collectors outputs, pytest, existing tools, repo-backed docs.

---

## 0. 第二阶段范围边界

### 本阶段要完成什么
1. 建立统一 diagnosis schema / finding model
2. 完成 env/workspace/build/launch/runtime diagnosers 分层设计
3. 完成 fusion diagnoser 真正可用的优先级逻辑
4. 引入 confidence / evidence_refs / uncertainty_gaps / risk_level
5. 建立最小行动建议（recommended_next_probe）策略
6. 补齐 diagnoser 级测试与 workflow 级测试
7. 更新 capability matrix 与 live diagnosis 工作流文档

### 本阶段明确不做什么
1. 不做 recovery benchmark 正式体系
2. 不做 gateway/cron 自动化
3. 不做 MCP server 落地
4. 不做完整多 Agent 编排层
5. 不做大规模 examples/runbooks 体系翻新（留到第三阶段）

### 本阶段成功标准
- 诊断结果不再只是标签列表，而是带证据和优先级的结构化结论
- 用户能拿到“最小下一步检查”而不是长串平铺建议
- fusion diagnoser 能融合至少 env/workspace/graph/tf/controller 五类证据
- workflow 级测试能验证诊断输出的优先级和建议质量

## 1. 推荐交付顺序

### Milestone 1：Diagnosis schema 与 finding model
### Milestone 2：单领域 diagnosers 升级
### Milestone 3：Fusion diagnoser 完整化
### Milestone 4：Workflow diagnosis tests
### Milestone 5：能力说明与用户工作流更新

## 2. 文件级实施规划

## Task 1: 建立 diagnosis schema

**Objective:** 统一表达诊断结果、证据引用、候选根因和下一步建议。

**Files:**
- Create: `tools/schemas/diagnosis_schema.py`
- Create: `tests/diagnosers/test_diagnosis_schema.py`

**Planned contents:**
- DiagnosisFinding
- CandidateCause
- EvidenceRef
- ProbeRecommendation
- RecoveryHint
- DiagnosisReport
- RiskLevel enum or string convention
- Confidence convention

**Design notes:**
- 优先兼容第一阶段 runtime schema
- 不要一开始做过度复杂评分系统
- 保持 JSON-friendly

**Validation plan:**
- 单测验证结构序列化
- 验证 DiagnosisReport 组合能力

## Task 2: 升级 env/workspace diagnosers

**Objective:** 让环境与工作区诊断从旧工具输出迁移到 diagnosis schema。

**Files:**
- Create: `tools/diagnosers/env_diagnoser.py`
- Create: `tools/diagnosers/workspace_diagnoser.py`
- Create: `tests/diagnosers/test_env_diagnoser.py`
- Create: `tests/diagnosers/test_workspace_diagnoser.py`

**Planned capabilities:**
- 从 EnvironmentSnapshot / WorkspaceSnapshot 生成 DiagnosisFinding
- 标记 environment mismatch / missing setup / workspace structure issues
- 输出 recommended_next_probe
- 输出 risk_level（通常 read_only / low_risk_local）

## Task 3: 升级 build/launch diagnosers

**Objective:** 把现有 build/launch 工具纳入统一 diagnosis schema。

**Files:**
- Create: `tools/diagnosers/build_diagnoser.py`
- Create: `tools/diagnosers/launch_diagnoser.py`
- Create: `tests/diagnosers/test_build_diagnoser.py`
- Create: `tests/diagnosers/test_launch_diagnoser.py`
- Reference existing:
  - `tools/colcon_build_summary.py`
  - `tools/ros2_launch_diagnose.py`

**Planned capabilities:**
- 从 build summary / launch probe 输出 finding
- 归一化 root cause categories
- 附带 evidence refs 与 next probe

## Task 4: 升级 runtime graph / tf / controller diagnosers

**Objective:** 把核心 runtime diagnosis 提升为 schema-first 诊断器。

**Files:**
- Create: `tools/diagnosers/runtime_graph_diagnoser.py`
- Create: `tools/diagnosers/tf_diagnoser.py`
- Create: `tools/diagnosers/controller_diagnoser.py`
- Create: `tests/diagnosers/test_runtime_graph_diagnoser.py`
- Create: `tests/diagnosers/test_tf_diagnoser.py`
- Create: `tests/diagnosers/test_controller_diagnoser.py`

**Planned capabilities:**
- orphan topic / starved subscriber diagnosis
- tf staleness / missing chain diagnosis
- controller inactive / hardware interface export issue diagnosis
- confidence / evidence_refs 输出

## Task 5: 完成 fusion diagnoser 真正可用版

**Objective:** 让系统能从多源证据中收敛出高优先级、低歧义的行动建议。

**Files:**
- Modify planned: `tools/diagnosers/fusion_diagnoser.py`
- Create: `tests/diagnosers/test_fusion_diagnoser_prioritization.py`

**Planned capabilities:**
- 输入多个 DiagnosisReport / RuntimeEvidenceBundle
- 合并 candidate causes
- 依据 evidence density / conflict / severity 做排序
- 输出 top prioritized causes
- 输出 smallest next information-gain step
- 输出 uncertainty gaps

**Design notes:**
- 第一版只需要 deterministic heuristics
- 暂不引入 ML/LLM scoring 逻辑

## Task 6: 建立 workflow diagnosis tests

**Objective:** 不只测试单模块，还验证多模块结合后的诊断行为。

**Files:**
- Create: `tests/workflows/test_diagnosis_workflows.py`
- Create: `tests/workflows/test_fusion_next_probe_selection.py`

**Planned scenarios:**
- 环境不匹配 + workspace 正常
- launch 成功但 runtime graph 不健康
- tf stale + controller inactive 联动场景
- QoS mismatch 样例（若第二阶段末可支持）

## Task 7: 文档与能力边界同步升级

**Objective:** 让用户知道第二阶段后系统“会诊断到什么程度”。

**Files:**
- Modify planned: `docs/00_overview/current-capability-boundaries.md`
- Modify planned: `docs/03_workflows/live-runtime-debug-workflow.md`
- Modify planned: `docs/02_product/capability_matrix.md`
- Create: `docs/03_workflows/fusion-diagnosis-workflow.md`

**Planned contents:**
- evidence-driven diagnosis flow
- confidence 与 uncertainty 的含义
- 什么建议可以自动执行，什么只能提示
- 第二阶段能力边界

## 3. 第二阶段建议执行顺序

1. diagnosis_schema.py
2. env_diagnoser.py
3. workspace_diagnoser.py
4. build_diagnoser.py
5. launch_diagnoser.py
6. runtime_graph_diagnoser.py
7. tf_diagnoser.py
8. controller_diagnoser.py
9. fusion_diagnoser.py 完整化
10. workflow diagnosis tests
11. docs / capability updates

## 4. 第二阶段测试与验证规划

### 单元测试
- 各 diagnoser 输入 snapshot 后输出结构正确
- evidence_refs / confidence / risk_level 存在

### 工作流测试
- 多证据场景优先级排序合理
- recommended_next_probe 不是随机堆建议

### 回归验证
- 第一阶段 collectors 不被破坏
- 现有 benchmark/report pipeline 仍可运行

## 5. 风险与取舍

### 风险 1：诊断层过早过重，导致 collector 价值被淹没
应对：
- 第二阶段始终围绕 collector outputs，不重回文本猜测式设计

### 风险 2：推荐建议数量过多，用户体验变差
应对：
- 强制输出 top causes + smallest next probe

### 风险 3：confidence 表达过度主观
应对：
- 第一版只做规则启发式 confidence，不装作概率学精确值

## 6. 第二阶段完成后的预期成果

- ROS2-Agent 从“能采集事实”升级到“能组织事实并收敛诊断路径”
- 输出不再只是标签，而是结构化、可解释、带证据的诊断结果
- 为第三阶段 recovery benchmark 与 runbook 建立基础
