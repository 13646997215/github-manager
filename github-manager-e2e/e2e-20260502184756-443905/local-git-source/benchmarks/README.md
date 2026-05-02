# ROS2-Agent Benchmarks

## 当前 benchmark 分类
- offline reasoning benchmark
- workflow benchmark
- recovery benchmark

## 目录说明
- `fixtures/`：静态样例与旧 benchmark 输入
- `tasks/`：任务说明与评测目标
- `workflows/`：多步采集/诊断 workflow benchmark
- `recovery/`：恢复导向 benchmark 资产
- `reports/`：json / markdown / evidence / replay manifests 等报告输出

## 成熟度提醒
当前 benchmark 体系正在从 fixture-based reasoning 向 workflow/recovery 过渡。
不要把旧报告分数直接解释为真实恢复成功率。
