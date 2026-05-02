# Benchmark Taxonomy

最后更新：2026-04-30
阶段状态：Phase-3 benchmark restructuring

## 1. 目的

本文件用于明确区分 ROS2-Agent 当前的三类 benchmark，避免把 repository fixture 命中率误写成现场恢复能力。

## 2. 三类 benchmark

### 2.1 Offline reasoning benchmark
- 别名：fixture-based benchmark
- 输入：仓库内静态 fixtures / transcripts / expected labels
- 输出：分类、建议、结构化报告命中情况
- 适用：验证规则资产、格式稳定性、基础 reasoning 路径
- 当前成熟度：repository-validated

### 2.2 Workflow benchmark
- 输入：多步采集/诊断场景定义
- 输出：预期 diagnosis shape、优先级、next probe、verification condition
- 适用：验证 collector + diagnoser + fusion 的闭环行为
- 当前成熟度：implemented prototype

### 2.3 Recovery benchmark
- 输入：broken workflow + 建议动作 + 修复后验证条件
- 输出：建议有效性、验证通过率、恢复总结
- 适用：验证“建议是否真的有恢复价值”
- 当前成熟度：early prototype / protocol-first

## 3. 禁止混淆的表述
- Offline reasoning score 高，不等于 live runtime diagnosis 强
- Workflow benchmark 通过，不等于 production-ready 恢复闭环
- Recovery benchmark 首批案例存在，不等于已经证明广泛现场鲁棒性

## 4. 当前建议用语
- repository-validated
- implemented prototype
- recovery-readiness
- planned
