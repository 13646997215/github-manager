# Fusion Diagnosis Workflow（阶段2）

最后更新：2026-04-30
阶段状态：Phase-2 diagnosis enabled

## 1. 目标

在 phase-1 collectors 提供统一 runtime evidence 之后，phase-2 的目标是：
- 把多源证据转化为结构化 DiagnosisReport
- 给出 prioritized candidate causes
- 给出 smallest next probe
- 明确 evidence refs / uncertainty gaps / risk level

## 2. 输入层
- EnvironmentSnapshot
- WorkspaceSnapshot
- Build summary（legacy bridge）
- LaunchProbeSnapshot
- RuntimeEvidenceBundle（graph / tf / controller）

## 3. 单领域 diagnosers
- `tools/diagnosers/env_diagnoser.py`
- `tools/diagnosers/workspace_diagnoser.py`
- `tools/diagnosers/build_diagnoser.py`
- `tools/diagnosers/launch_diagnoser.py`
- `tools/diagnosers/runtime_graph_diagnoser.py`
- `tools/diagnosers/tf_diagnoser.py`
- `tools/diagnosers/controller_diagnoser.py`

每个 diagnoser 当前都输出：
- findings
- candidate_causes
- recommended_next_probe

## 4. 融合层
- `tools/diagnosers/fusion_diagnoser.py`

当前策略：
- 基于 deterministic heuristic weights 排序
- 聚合 evidence_refs
- 输出 uncertainty_gaps
- 从高优先级 report 继承推荐 probe

## 5. 当前限制
- confidence 仍是 heuristic string，不是统计概率
- risk_level 仅做阶段化安全分级
- 尚未形成 recovery loop
- launch/build 输入仍部分依赖 legacy summary/probe 结构

## 6. 使用建议
- 把 fusion 输出视为“高质量收敛建议”，不是最终真理
- 优先执行 smallest next probe，而不是一次展开所有建议
- 对 needs_confirmation 级动作，仍应由用户最终确认
