# ROS2-Agent 第三阶段实施计划（仅规划，不执行）

生成时间：2026-04-30
项目路径：/home/hanhan/Desktop/ROS2-Agent
计划性质：纯规划文档，禁止在本计划阶段直接开始实现

> For Hermes: 只有当第二阶段全部完成并验证通过后，才进入本阶段执行。

**Goal:** 将 ROS2-Agent 的验证体系从 fixture-based reasoning 升级为 workflow/recovery-oriented evaluation，并把 examples/transcripts 升级成真实可复演的 runbook 体系。

**Architecture:** 第三阶段围绕“真实坏案例 -> 采集 -> 诊断 -> 建议 -> 修复验证”构建 benchmark 与 runbook 层，重点建立 workflow benchmark、recovery benchmark、broken workflows、evidence pack 和 replay manifests。该阶段是项目从“能诊断”走向“能证明自己有用”的关键。

**Tech Stack:** Python 3.10+, prior collectors + diagnosers, pytest, benchmark scripts, markdown reports, repo fixtures/examples/docs.

---

## 0. 第三阶段范围边界

### 本阶段要完成什么
1. 重新分层 benchmark 类型
2. 建立 workflow benchmark
3. 建立 recovery benchmark 设计与首批案例
4. 重构 examples/transcripts 为 demo_workflows / broken_workflows / runbooks
5. 建立 evidence packs / replay manifests
6. 补齐 workflow/recovery tests
7. 更新 benchmark docs、team reporting docs、teaching docs

### 本阶段明确不做什么
1. 不做完整 Hermes-native 平台注册
2. 不做 MCP server 真部署
3. 不做完整 gateway automation 产品化
4. 不做多 Agent orchestration 平台层

### 本阶段成功标准
- benchmark 不再只有标签命中率
- 至少有 3 类真实 broken workflow 可复演
- report 能说明恢复有效性，而非 فقط规则命中
- examples/transcripts 升级为可执行 runbook 风格

## 1. 推荐交付顺序

### Milestone 1：Benchmark taxonomy 重构
### Milestone 2：Workflow benchmarks
### Milestone 3：Recovery benchmarks
### Milestone 4：Runbooks / broken workflows 体系
### Milestone 5：Reporting & docs 升级

## 2. 文件级实施规划

## Task 1: 重构 benchmark taxonomy

**Objective:** 明确 offline reasoning / workflow / recovery 三类 benchmark，不再混淆。

**Files:**
- Create: `docs/04_benchmarks/benchmark-taxonomy.md`
- Modify planned: `docs/04_benchmarks/benchmark_evaluation_protocol.md`
- Modify planned: `benchmarks/README.md`（若不存在则新增）

**Planned taxonomy:**
- offline reasoning benchmark
- workflow benchmark
- recovery benchmark

## Task 2: 建立 workflow benchmark 目录与规范

**Objective:** 建立以“多步采集+诊断”为核心的中层 benchmark。

**Files:**
- Create: `benchmarks/workflows/README.md`
- Create: `benchmarks/workflows/workflow_manifest.schema.json`（可选，若仓库风格允许）
- Create: `benchmarks/workflows/launch_runtime_graph_failure/`
- Create: `benchmarks/workflows/tf_controller_interaction_failure/`
- Create: `benchmarks/workflows/environment_overlay_conflict/`

**Planned contents per workflow:**
- scenario description
- initial evidence
- expected diagnosis shape
- expected next probes
- expected safe recovery hint
- verification condition

## Task 3: 建立 recovery benchmark 设计与首批样例

**Objective:** 从“诊断对不对”提升到“建议是否帮助恢复”。

**Files:**
- Create: `docs/04_benchmarks/recovery-benchmark-design.md`
- Create: `benchmarks/recovery/README.md`
- Create: `benchmarks/recovery/recovery_scorecard_template.md`
- Create: `benchmarks/recovery/cases/`

**Planned metrics:**
- first diagnosis precision
- top-3 diagnosis recall
- recovery suggestion effectiveness
- verification pass rate after suggested fix
- mean time to narrow issue
- mean time to recovery（若无法真实量化，可先定义协议）

## Task 4: 建立 evidence packs / replay manifests

**Objective:** 让 benchmark 和真实案例都能留存结构化证据，而不是只剩摘要文本。

**Files:**
- Create: `benchmarks/reports/evidence/README.md`
- Create: `benchmarks/reports/replay_manifest_template.json`
- Create: `scripts/validation/export_evidence_pack.py`
- Create: `tests/workflows/test_evidence_pack_export.py`

**Planned capabilities:**
- 从 collectors/diagnosers 输出 evidence pack
- 为每个 workflow/recovery case 生成 replay manifest
- 用于复盘与未来 agent 重放

## Task 5: examples 目录升级为 workflow/runbook 结构

**Objective:** 把抽象 transcript 升级为真实可复演资产。

**Files:**
- Create: `examples/demo_workflows/`
- Create: `examples/broken_workflows/`
- Create: `examples/runbooks/`
- Migrate planned from existing:
  - `examples/transcripts/`
  - `examples/broken_cases/`
  - `examples/demo_workspace/`

**Runbook required sections:**
- 场景背景
- 初始症状
- 执行命令
- 关键输出
- 证据解释
- 排除路径
- 修复动作
- 修复后验证
- 常见误判点

## Task 6: workflow / recovery 测试层

**Objective:** 不只验证工具存在，还验证场景闭环。

**Files:**
- Create: `tests/workflows/test_workflow_benchmarks.py`
- Create: `tests/recovery/test_recovery_benchmarks.py`
- Create: `tests/recovery/test_replay_manifests.py`

**Planned scenarios:**
- launch file ok but runtime unhealthy
- tf chain issue plus controller inactive
- overlay conflict causing misleading build/runtime symptoms

## Task 7: 报告与教学资产升级

**Objective:** 让第三阶段成果能对外展示真实价值，而不只是输出更多 JSON。

**Files:**
- Modify planned: `docs/02_product/reporting_asset_roadmap.md`
- Modify planned: `docs/02_product/team_report_template.md`
- Modify planned: `docs/02_product/lab_daily_report_template.md`
- Create: `docs/02_product/recovery-evaluation-summary-template.md`
- Create: `docs/05_roadmap/runbook-learning-track.md`

## 3. 第三阶段建议执行顺序

1. benchmark-taxonomy.md
2. workflow benchmark structure
3. recovery benchmark design + cases skeleton
4. evidence pack export
5. examples/runbooks structure
6. workflow/recovery tests
7. reporting/docs updates

## 4. 第三阶段测试与验证规划

### 结构验证
- benchmark manifests 完整
- evidence pack 可导出
- replay manifest 可读

### 工作流验证
- benchmark 能运行到 diagnosis / verification 层
- runbook 内容与 benchmark case 对齐

### 回归验证
- 第一、第二阶段工具与测试不被破坏
- latest benchmark report pipeline 可升级但不崩溃

## 5. 风险与取舍

### 风险 1：想一次性把所有案例做满，导致质量下降
应对：
- 先做 3 个强代表案例，不追求数量

### 风险 2：runbook 写成又长又空的文档
应对：
- 强制包含命令、输出、验证，不接受纯叙事

### 风险 3：recovery metrics 虚化
应对：
- 第一版先定义协议与收集方式，避免造假精确指标

## 6. 第三阶段完成后的预期成果

- ROS2-Agent 能通过 workflow / recovery benchmark 证明自己不只是“会说”，而是“有实际恢复价值”
- examples/transcripts 从展示材料升级为可复演 runbook
- 项目对外可信度和教学实用度显著提升
