# Recovery Benchmark Design

最后更新：2026-04-30
阶段状态：Phase-3 initial design

## 1. 目标
把 benchmark 从“诊断像不像”推进到“建议是否帮助恢复”。

## 2. 核心指标
- first diagnosis precision
- top-3 diagnosis recall
- recovery suggestion effectiveness
- verification pass rate after suggested fix
- mean time to narrow issue（协议级）
- mean time to recovery（协议级）

## 3. 现实约束
当前阶段先定义协议和首批案例，不伪造统计精度。

## 4. 最小 case 结构
- broken_state.md
- suggested_fix.md
- verification.md
- scorecard.md
