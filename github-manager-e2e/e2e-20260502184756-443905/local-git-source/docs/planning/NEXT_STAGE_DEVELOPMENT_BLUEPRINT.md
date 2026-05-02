# ROS2-Agent 下一阶段开发蓝图

## 目标
把 ROS2-Agent 从“高质量仓库”继续推进为“真正可安装、可验证、可教学、可评测、可持续演进的 ROS2 专家平台”。

## 核心推进方向

### A. 真实 Hermes 可用性做实
1. 写出真实 profile 首次使用 transcript。
2. 明确 repository-backed Hermes integration contract。
3. 让 profile install / bootstrap / 验证路径形成统一叙事。

### B. Runtime 工具从样例走向真实诊断器
1. `tools/ros2_graph_inspect.py`
2. `tools/ros2_controller_diagnose.py`
3. `tools/ros2_tf_diagnose.py`

### C. Benchmark 变成平台护城河
1. 扩大经典 ROS2 病例库。
2. 增加 benchmark scorecard 与 evaluation protocol。
3. 让不同工具/模型/配置可被同一套任务评估。

### D. 教学能力产品化
1. 增加教学型 skills。
2. 增加教学型 transcripts。
3. 增加 learning track 与 teaching strategy 文档。

### E. GitHub 产品竞争力继续增强
1. capability matrix
2. FAQ
3. architecture / capability visual assets

## 实施顺序
1. 文档先行，形成最终方向约束。
2. 实现 runtime 真实工具。
3. 补 benchmark 与 teaching 资产。
4. 扩 README / product docs / transcripts。
5. 补测试、验证、报告、日志。

## 完成判据
- 所有新增能力都有对应文档、测试、验证入口。
- 所有关键 claim 都有可运行或可复验资产背书。
- 仓库保持 GitHub 可发布级质量。
