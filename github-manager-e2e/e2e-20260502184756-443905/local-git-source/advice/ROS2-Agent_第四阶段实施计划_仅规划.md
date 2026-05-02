# ROS2-Agent 第四阶段实施计划（仅规划，不执行）

生成时间：2026-04-30
项目路径：/home/hanhan/Desktop/ROS2-Agent
计划性质：纯规划文档，禁止在本计划阶段直接开始实现

> For Hermes: 只有当第三阶段全部完成并验证通过后，才进入本阶段执行。

**Goal:** 把 ROS2-Agent 从“具备 runtime 诊断能力的仓库型平台”进一步推进为“更 Hermes-native、能力注册清晰、安装闭环更完整、自动化准备更成熟”的平台化产物。

**Architecture:** 第四阶段围绕平台化与产品化收尾，重点包括 tool registry / cli、capability contract、skill manifest/validation、post-install validation、MCP readiness assets、gateway/cron demo、最终文档与质量门收口。该阶段是“把能力做成平台表面”的阶段。

**Tech Stack:** Python 3.10+, existing tools/diagnosers/benchmarks, repo validation scripts, Hermes profile assets, docs, CI.

---

## 0. 第四阶段范围边界

### 本阶段要完成什么
1. 建立 tool registry / unified CLI
2. 建立 capability contract
3. 建立 skill manifest / validation 机制
4. 建立 post-install validation
5. 准备 MCP contracts/schemas/readiness assets
6. 设计并落地 gateway/cron demo 级资产
7. 完成 README/quickstart/developer-setup/final quality gate 收口

### 本阶段明确不做什么
1. 不强求完整生产级 MCP server 实现
2. 不强求完整平台 SaaS 化
3. 不扩展到超出 ROS2-Agent 当前定位的新领域

### 本阶段成功标准
- 用户能清晰知道平台能做什么、怎样调用、怎样验证
- profile 安装不再只是复制模板，而是具备可验证闭环
- Hermes 集成表面不再模糊
- 自动化至少有 demo 级可执行路径，而不是 فقط future hooks

## 1. 推荐交付顺序

### Milestone 1：Registry / CLI / Capability Contract
### Milestone 2：Skill / install / validation 完整化
### Milestone 3：MCP readiness assets
### Milestone 4：gateway/cron demo
### Milestone 5：README / docs / quality gate 最终收口

## 2. 文件级实施规划

## Task 1: 建立 tool registry 与统一 CLI

**Objective:** 把 collectors / diagnosers / reports 从散装脚本升级为统一能力入口。

**Files:**
- Create: `tools/registry.py`
- Create: `tools/cli.py`
- Create: `tests/tools/test_registry.py`
- Create: `tests/tools/test_cli.py`

**Planned capabilities:**
- 列出可用 collectors
- 列出可用 diagnosers
- 调用指定 collector
- 调用指定 diagnoser
- 输出结构化 JSON / markdown digest

## Task 2: 建立 capability contract

**Objective:** 明确平台当前能力边界、输入输出、风险级别和依赖关系。

**Files:**
- Create: `docs/01_architecture/capability_contract.md`
- Create: `profile/ros2-agent/CAPABILITIES.md`
- Create: `tests/workflows/test_capability_contract_refs.py`

**Planned contents:**
- capability name
- current maturity level
- required inputs
- outputs
- risk level
- validation path
- related docs/tools/tests

## Task 3: 建立 skill manifest / validation 机制

**Objective:** 把 repo skills 变成可审计、可检查、可同步的资产集合。

**Files:**
- Create: `scripts/skills/inspect_repo_skills.py`
- Create: `scripts/skills/export_skill_manifest.py`
- Create: `scripts/skills/validate_skill_metadata.py`
- Create: `tests/workflows/test_skill_manifest_pipeline.py`
- Create: `docs/03_workflows/skill-asset-governance.md`

## Task 4: 升级安装与 post-install validation

**Objective:** 让 profile 安装从模板复制升级为可验证的安装闭环。

**Files:**
- Modify planned: `profile/ros2-agent/bootstrap/install_profile.sh`
- Modify planned: `profile/ros2-agent/bootstrap/init_workspace.sh`
- Create: `profile/ros2-agent/bootstrap/post_install_validate.sh`
- Create: `tests/workflows/test_post_install_validate.py`
- Modify planned: `docs/03_workflows/bootstrap-workflow.md`

**Planned capabilities:**
- 验证 profile 文件完整性
- 验证 capability manifest 可访问
- 验证 repo assets 可引用
- 验证至少一个 collector / report pipeline 可运行

## Task 5: 准备 MCP readiness assets

**Objective:** 不强行现在实现完整 MCP server，但把未来接口面定义清楚。

**Files:**
- Create: `mcp/README.md`
- Create: `mcp/contracts/collector_contract.md`
- Create: `mcp/contracts/diagnosis_contract.md`
- Create: `mcp/schemas/runtime_evidence.schema.json`
- Create: `mcp/schemas/diagnosis_report.schema.json`
- Create: `tests/workflows/test_mcp_schema_assets.py`

## Task 6: 设计并落地 gateway/cron demo 级资产

**Objective:** 把“future hooks”推进到可展示、可验证的 demo 级自动化流。

**Files:**
- Create: `docs/03_workflows/gateway-cron-demo-workflow.md`
- Create: `scripts/validation/run_gateway_demo_pipeline.sh`
- Create: `tests/workflows/test_gateway_demo_assets.py`
- Modify planned: existing scheduled reporting docs

**Planned scope:**
- 周期性收集 benchmark/report 资产的 demo 流程
- 产出可交付 markdown digest
- 明确哪些部分仍需 Hermes 外部配置

## Task 7: README / docs / quality gate 最终收口

**Objective:** 在全部阶段完成后，把对外表述、快速开始、验证入口全部收敛一致。

**Files:**
- Modify planned: `README.md`
- Modify planned: `README_EN.md`
- Modify planned: `docs/00_overview/quickstart.md`
- Modify planned: `docs/00_overview/developer-setup.md`
- Modify planned: `docs/00_overview/status.md`
- Modify planned: `scripts/validation/run_full_quality_gate.sh`
- Create: `docs/00_overview/final-platform-capability-summary.md`

**Planned outcomes:**
- README 表述与真实能力对齐
- quickstart 不再误导用户以为已经全平台安装完成
- final quality gate 覆盖阶段性核心成果

## 3. 第四阶段建议执行顺序

1. registry.py + cli.py
2. capability_contract.md + CAPABILITIES.md
3. skill manifest pipeline
4. install/post-install validation upgrade
5. MCP readiness assets
6. gateway/cron demo assets
7. README/docs/quality gate 收口

## 4. 第四阶段测试与验证规划

### 单元与工作流测试
- registry / cli 可用
- skill manifest 可导出与校验
- post-install validate 可运行
- MCP schema assets 存在且可读
- gateway demo pipeline 不崩溃

### 收口验证
- full quality gate 通过
- benchmark/report assets 仍可导出
- capability docs 与真实文件一致

## 5. 风险与取舍

### 风险 1：为了平台感做太多外壳，反而模糊已实现能力
应对：
- 所有 contract 都必须指向真实工具和测试，不写空承诺

### 风险 2：gateway/cron 演示被误解成完整生产自动化
应对：
- 明确标注为 demo / readiness，说明外部依赖边界

### 风险 3：README 收口时再次语言膨胀
应对：
- 所有宣传性表述必须与 capability contract 对应

## 6. 第四阶段完成后的预期成果

- ROS2-Agent 具备更清晰的 Hermes-native 平台表面
- 安装、能力发现、调用、验证、自动化演示形成闭环
- 项目从“有强原型能力”进化为“更完整、更可信、更可持续的仓库型平台产品”
