# ROS2-Agent 下一阶段重构路线图

生成时间：2026-04-30
适用对象：/home/hanhan/Desktop/ROS2-Agent
定位目标：把当前“repository-backed ROS2 教学/评测资产仓库”逐步重构为“具备真实 runtime 接入能力、Hermes 深度集成能力、可验证现场效果的 ROS2 Agent 平台”

> 这份路线图不是空泛愿景，而是按照“真实场景效果优先、平台包装靠后”的原则设计的务实重构方案。

## 0. 重构目标一句话

下一阶段的核心目标，不是再写更多平台文档，而是优先建立：
1. live ROS2 运行时采集能力
2. 多证据融合诊断能力
3. 真实坏案例 benchmark 闭环
4. Hermes-native 集成壳层

只有这四件事逐步落地，ROS2-Agent 才会从“很像平台”变成“就是平台”。

## 1. 当前项目状态重新定义

为了避免重构方向继续跑偏，首先必须重新定义当前项目现状。

### 当前最准确定位
ROS2-Agent 当前应被定义为：
- 基于 Hermes Agent 的 repository-backed ROS2 领域资产仓库
- 重点包含：profile scaffold、规则化诊断工具、benchmark fixtures、validation pipeline、教学材料
- 当前主要强项是：离线结构化分析、教学导向、仓库自验证
- 当前主要弱项是：live ROS2 runtime 接入、现场诊断闭环、Hermes 原生运行时融合、真实用户成功率验证

### 当前不能再模糊表达的点
以后在 README / docs / 对外介绍里，必须明确区分三层：
1. 已落地能力
2. 原型能力
3. 规划能力

建议统一标记术语：
- production-ready
- repository-validated
- implemented prototype
- planned

不要再让“implemented prototype”在用户眼里看起来像“已经现场可用”。

## 2. 重构总原则

这次重构必须遵守下面 8 条原则，不然很容易再次落入“文档比产品更成熟”的坑。

### 原则 1：先做运行时能力，再做平台包装
优先级必须是：
- 能看现场 > 能讲故事
- 能接系统 > 能出报告
- 能缩短排障时间 > 能写漂亮文档

### 原则 2：一切围绕真实 ROS2 用户的最小有效收益
每个新模块都回答一个问题：
“它能不能在真实 ROS2 工作现场，把问题面缩小一点？”

如果不能，就降级优先级。

### 原则 3：优先做证据采集，不优先做推理话术
当前项目最不缺的是“怎么讲诊断逻辑”，最缺的是“从系统里拿到真实证据”。

### 原则 4：统一 schema，避免工具各说各话
所有 collector / diagnoser / benchmark / report 都要共享统一结构，不要每个脚本一个输出风格。

### 原则 5：先建立单 Agent 强能力，再谈多 Agent
多 Agent 不是不能做，而是现在还太早。
先把单 Agent 的 runtime 诊断闭环做扎实，再拆角色最稳。

### 原则 6：benchmark 必须逐渐转向“恢复成功率”
不能一直停留在“fixture 标签命中率”。

### 原则 7：profile scaffold 不等于平台安装
安装流程必须从“复制模板”升级为“环境感知 + 资产发现 + 验证引导”。

### 原则 8：风险控制必须机制化
安全规则不能只写在 AGENTS.md 里，必须逐步落实进执行流程和工具行为。

## 3. 目标架构蓝图

下一阶段建议把 ROS2-Agent 重构成 6 层结构：

1. Capability Surface Layer（能力表面层）
2. Runtime Collection Layer（运行时采集层）
3. Diagnosis Layer（诊断推理层）
4. Benchmark & Evidence Layer（基准与证据层）
5. Hermes Integration Layer（Hermes 集成层）
6. UX & Teaching Layer（用户体验与教学层）

下面逐层展开。

## 4. 第一优先级：Runtime Collection Layer 重构

这是整个项目最关键的一层，建议作为第一阶段主攻方向。

### 4.1 当前问题
当前 tools 目录中的 runtime 相关模块，大多是：
- 输入：人工或 fixture 构造的数据结构
- 输出：规则判断后的 root cause / next_actions

缺少：
- 对真实系统的 live 采集
- 与 ros2 CLI / rclpy / tf2 / controller_manager 的真实接入
- 现场数据归一化能力

### 4.2 下一阶段必须新增的 collector 模块
建议在 tools/ 下新增一组 collector，而不是继续把诊断逻辑和采集逻辑混在一起。

建议新增目录：
- tools/collectors/

建议新增文件：
- tools/collectors/ros2_env_collect.py
- tools/collectors/ros2_workspace_collect.py
- tools/collectors/ros2_graph_collect.py
- tools/collectors/ros2_topic_collect.py
- tools/collectors/ros2_tf_collect.py
- tools/collectors/ros2_controller_collect.py
- tools/collectors/ros2_launch_collect.py
- tools/collectors/ros2_log_collect.py

### 4.3 每个 collector 的职责建议

#### ros2_env_collect.py
职责：
- 采集 ROS_DISTRO
- 采集 RMW_IMPLEMENTATION
- 采集 underlay / overlay source 状态
- 采集 colcon / rosdep / python / gazebo / rviz2 可用性
- 检查 /opt/ros/<distro>/setup.bash
- 检查 shell 环境污染

输出建议：
- EnvironmentSnapshot
- EnvironmentWarnings
- EnvironmentRepairHints

#### ros2_workspace_collect.py
职责：
- 扫描 workspace 结构
- 列出 package.xml / setup.py / CMakeLists.txt
- 标记 ament_python / ament_cmake
- 检测 install/build/log 状态
- 标记缺失 package metadata
- 扫描 launch/config/urdf/xacro 资产

#### ros2_graph_collect.py
职责：
- 调 ros2 node list
- 调 ros2 topic list
- 调 ros2 topic info --verbose
- 尝试建立 node-topic 关系
- 分类关键 topics（传感器、tf、command、状态）
- 识别 orphan publisher / starved subscriber / suspicious namespace

#### ros2_topic_collect.py
职责：
- 对关键 topic 做抽样检查
- 采样消息频率
- 记录 publisher/subscriber 数
- 记录 QoS profile
- 必要时抓取有限样本

#### ros2_tf_collect.py
职责：
- 采集 TF tree
- 检查 stale frame
- 检查 missing chain
- 检查 frame authority
- 检查 sim_time / clock 相关异常
- 导出结构化 frame graph

#### ros2_controller_collect.py
职责：
- 调 ros2 control list_controllers
- 调 ros2 control list_hardware_interfaces
- 检查 active/inactive/unconfigured/failed controller
- 检查 claimed/required interfaces
- 记录 controller manager 可见状态

#### ros2_launch_collect.py
职责：
- 解析 launch file 路径
- 检查 package prefix
- 检查 referenced params/assets
- 记录 minimal launch probe 结果
- 提取 launch runtime 失败特征

#### ros2_log_collect.py
职责：
- 读取目标日志片段
- 裁剪噪声
- 提取 error/fatal/warn 上下文
- 产出结构化 evidence blocks

### 4.4 统一采集结果 schema
建议新增：
- tools/schemas/runtime_schema.py

核心 dataclass / schema 建议：
- EnvironmentSnapshot
- WorkspaceSnapshot
- GraphSnapshot
- TopicSnapshot
- TfSnapshot
- ControllerSnapshot
- LaunchSnapshot
- LogEvidence
- RuntimeEvidenceBundle

这样做好处：
1. collector 与 diagnoser 解耦
2. benchmark 可以直接喂 schema
3. report 层可以稳定渲染
4. 多 agent 未来也能共享同一种诊断语言

## 5. 第二优先级：Diagnosis Layer 重构

### 5.1 当前问题
现在的 diagnoser 偏规则模板化，粒度不够，且和 live system 脱钩。

### 5.2 重构目标
把诊断层分成两类：
1. Static/structural diagnosis
2. Live/runtime diagnosis

建议目录：
- tools/diagnosers/

建议文件：
- tools/diagnosers/env_diagnoser.py
- tools/diagnosers/workspace_diagnoser.py
- tools/diagnosers/build_diagnoser.py
- tools/diagnosers/launch_diagnoser.py
- tools/diagnosers/runtime_graph_diagnoser.py
- tools/diagnosers/tf_diagnoser.py
- tools/diagnosers/controller_diagnoser.py
- tools/diagnosers/fusion_diagnoser.py

### 5.3 从“标签输出”升级到“证据优先级排序”
每个 diagnoser 不应该只输出：
- root_cause_candidates
- next_actions

还应该输出：
- confidence
- evidence_refs
- uncertainty_gaps
- blocking_factors
- recommended_next_probe

建议统一结构：
- DiagnosisFinding
- CandidateCause
- EvidenceRef
- ProbeRecommendation
- RecoveryHint

### 5.4 增加 Fusion Diagnoser
这是最关键的诊断升级点之一。

fusion_diagnoser.py 职责：
- 综合 env / workspace / build / launch / graph / tf / controller / logs
- 对多个 root cause 做优先级排序
- 给出“最小信息增益下一步”
- 避免一次给用户十几条平铺建议

输出目标：
- Top-3 prioritized causes
- Why ranked this way
- Smallest next verification step
- What evidence is still missing

这一步做成之后，用户体验会比现在强非常多。

## 6. 第三优先级：Benchmark & Evidence Layer 重构

### 6.1 当前问题
当前 benchmark 更像“预设任务命中率验证”，不是“真实系统恢复能力验证”。

### 6.2 benchmark 的三阶段升级路线

#### 阶段 A：保留当前 fixture benchmark，但重新命名
建议把现有 benchmark 类型明确叫：
- offline reasoning benchmark
- fixture-based benchmark

不要让它看起来像现场成功率评测。

#### 阶段 B：新增 workflow benchmark
建议新增目录：
- benchmarks/workflows/

内容：
- 环境污染场景
- overlay 冲突场景
- launch 资产缺失场景
- TF stale + controller inactive 联动场景
- QoS mismatch 场景

每个 workflow benchmark 包含：
- 初始状态
- 采集步骤
- 预期诊断中间态
- 预期优先级排序
- 最小修复动作
- 修复后验证条件

#### 阶段 C：新增 recovery benchmark
这才是真正关键的终局方向。

建议新增目录：
- benchmarks/recovery/

评价指标改为：
- first diagnosis precision
- top-3 diagnosis recall
- recovery suggestion effectiveness
- verification pass rate after suggested fix
- mean time to narrow issue
- mean time to recovery

### 6.3 benchmark 产物升级
建议 benchmark 不只输出 json + md，还要输出：
- structured evidence pack
- benchmark replay manifest
- recovery summary
- false positive / false confidence analysis

建议目录：
- benchmarks/reports/json/
- benchmarks/reports/markdown/
- benchmarks/reports/evidence/

## 7. 第四优先级：Examples / Transcripts / Teaching 层重构

### 7.1 当前问题
transcript 偏轻、偏抽象、偏提纲式，不够像真实 runbook。

### 7.2 重构方向
把 examples 拆成三类：

建议目录：
- examples/demo_workflows/
- examples/broken_workflows/
- examples/runbooks/

### 7.3 transcript 升级标准
每份 transcript / runbook 必须包含：
1. 场景背景
2. 初始症状
3. 执行命令
4. 关键输出
5. 诊断证据
6. 排除路径
7. 修复动作
8. 修复后验证
9. 常见误判点

### 7.4 优先补的教学案例
建议优先做这些真实案例：
1. underlay / overlay 污染导致包错乱
2. launch file 找得到但 params 缺失
3. controller inactive + hardware interface 不完整
4. TF 链缺失导致 RViz/导航异常
5. QoS mismatch 导致传感器看似正常但消费者收不到
6. workspace 构建成功但 runtime graph 不健康

### 7.5 技能（skills）层升级建议
当前 skills 更像教学说明。
下一步建议把 skills 分为两类：
- teaching skills
- execution skills

建议目录结构：
- skills/teaching/
- skills/execution/

execution skills 重点要求：
- 调用哪些 collector
- 如何判定证据充分
- 如何排序下一步检查
- 如何给出最小风险建议

## 8. 第五优先级：Profile / 安装体验重构

### 8.1 当前问题
install_profile.sh 和 init_workspace.sh 过于轻量，只能叫模板安装器，不能叫平台安装流程。

### 8.2 重构目标
把安装流程升级为三段式：
1. install profile scaffold
2. discover repository capabilities
3. run post-install verification

### 8.3 install_profile.sh 升级建议
新增能力：
- 检查 Hermes 基本可用性
- 检查 repo 路径有效性
- 生成 capability manifest
- 生成 post-install checklist
- 标记哪些能力是 prototype / planned

### 8.4 init_workspace.sh 升级建议
建议升级为 workspace bootstrap assistant，而不是空目录生成器。

新增能力：
- 检查 /opt/ros/humble
- 检查 colcon / rosdep
- 生成 workspace metadata
- 可选写入 demo package 模板
- 可选生成 diagnostics/ 目录
- 提供 source / build / inspect / launch 的最小命令集

### 8.5 建议新增安装后验证脚本
新增：
- profile/ros2-agent/bootstrap/post_install_validate.sh

作用：
- 验证 profile 文件完整
- 验证 repo 资产可访问
- 验证基础 collectors 可运行
- 验证 benchmark/report pipeline 可用

## 9. 第六优先级：Hermes Integration Layer 重构

### 9.1 当前问题
Hermes 在当前项目里更像 profile 壳层，而不是运行时能力真正载体。

### 9.2 下一阶段集成目标
把“repo-backed assets”逐步变成“可被 Hermes 原生理解和消费的能力面”。

### 9.3 重点改造方向

#### 方向 1：能力清单显式化
建议新增：
- docs/01_architecture/capability_contract.md
- profile/ros2-agent/CAPABILITIES.md

明确定义：
- 当前能做什么
- 需要什么输入
- 产出什么输出
- 哪些能力是只读
- 哪些能力有风险

#### 方向 2：技能发现策略
当前必须明确 repo skill 与 Hermes global skill 的关系。

建议：
- 给 skills 增加 manifest
- 提供 sync / inspect / validate 脚本

例如新增：
- scripts/skills/inspect_repo_skills.py
- scripts/skills/export_skill_manifest.py
- scripts/skills/validate_skill_metadata.py

#### 方向 3：工具注册策略
为 collectors / diagnosers / reports 提供统一入口，而不是散装脚本。

建议新增：
- tools/registry.py
- tools/cli.py

目标：
- 用户能统一列出工具
- 用户能统一调用 collector / diagnoser
- Hermes 以后更容易挂接这些工具能力

#### 方向 4：MCP readiness
现在不一定要完整做 MCP server，但至少要预留：
- 明确 schema
- 明确 service boundaries
- 明确 stateless request/response contract

建议新增：
- mcp/contracts/
- mcp/schemas/
- mcp/README.md

## 10. 第七优先级：安全机制与执行护栏重构

### 10.1 当前问题
安全原则写得不少，但还没工具化。

### 10.2 重构目标
把安全原则变成执行护栏。

建议新增：
- tools/safety/preflight.py
- tools/safety/risk_classifier.py
- tools/safety/execution_gate.py

### 10.3 需要逐步具备的能力
1. sim-vs-real environment check
2. risky operation classification
3. dry-run recommendation
4. operator acknowledgement surface
5. post-action verification requirement

### 10.4 风险级别建议
统一把操作分成：
- read_only
- low_risk_local
- runtime_sensitive
- hardware_sensitive
- system_sensitive

所有建议动作都带 risk_level，避免用户把文字建议误当成无害建议。

## 11. 第八优先级：仓库结构重组建议

如果你愿意做一次中等规模重构，酥酥建议目录从“按历史堆积”转为“按能力分层”。

### 建议新结构

```text
ROS2-Agent/
├── README.md
├── pyproject.toml
├── profile/
│   └── ros2-agent/
├── skills/
│   ├── teaching/
│   └── execution/
├── tools/
│   ├── collectors/
│   ├── diagnosers/
│   ├── reporting/
│   ├── safety/
│   ├── schemas/
│   ├── registry.py
│   └── cli.py
├── benchmarks/
│   ├── fixtures/
│   ├── workflows/
│   ├── recovery/
│   ├── tasks/
│   └── reports/
├── examples/
│   ├── demo_workflows/
│   ├── broken_workflows/
│   └── runbooks/
├── scripts/
│   ├── validation/
│   ├── skills/
│   └── dev/
├── docs/
│   ├── 00_overview/
│   ├── 01_architecture/
│   ├── 02_product/
│   ├── 03_workflows/
│   ├── 04_benchmarks/
│   ├── 05_roadmap/
│   └── planning/
└── tests/
    ├── collectors/
    ├── diagnosers/
    ├── workflows/
    ├── recovery/
    └── integration/
```

### 重组收益
1. collector / diagnoser / report 分层清楚
2. benchmark 类型更清晰
3. teaching 与 execution 分离
4. 后续 CI、MCP、Hermes 集成更容易

## 12. 测试体系升级路线

### 12.1 当前测试体系定位
当前测试体系应被明确命名为：
- repository validation tests
- fixture reasoning tests
- pipeline smoke tests

### 12.2 下一阶段新增测试类型

#### integration tests
验证 collector 能否在真实/半真实 ROS 环境里拿到数据。

建议目录：
- tests/integration/

优先测试：
- graph collection
- tf collection
- controller collection
- launch probe

#### workflow tests
验证“采集 → 诊断 → 建议 → 验证”链路是否闭环。

建议目录：
- tests/workflows/

#### recovery tests
验证建议动作后，系统是否更接近恢复。

建议目录：
- tests/recovery/

### 12.3 CI 升级建议
CI 分层：
1. fast lint + unit
2. fixture benchmark
3. integration-lite
4. optional heavy sim workflow

不要把所有东西都挤进一个 validate-and-test job。

## 13. 文档体系重写建议

### 13.1 README 必须重写的部分
优先改：
1. 顶层定位
2. 当前能力边界
3. prototype 与 planned 的清晰区分
4. benchmark 含义说明
5. install profile != full platform install 的说明

### 13.2 新增文档建议
建议新增：
- docs/00_overview/current-capability-boundaries.md
- docs/01_architecture/runtime-evidence-schema.md
- docs/03_workflows/live-runtime-debug-workflow.md
- docs/04_benchmarks/recovery-benchmark-design.md
- docs/00_overview/risk-and-safety-model.md

### 13.3 删除或降级的文档表达
凡是下面这种表达，要谨慎：
- 专家级平台
- 完整平台
- 真正可验证平台
- 自动化就绪

除非对应能力已经有真实端到端证据支撑。

## 14. 推荐的阶段性交付计划

下面是酥酥按 4 个阶段排的务实版本。

## 阶段 1：Runtime 接入奠基（最高优先级）
预计目标：2~4 周

交付物：
- collectors 基础框架
- runtime schema
- env/workspace/graph/topic/tf/controller 基础采集器
- integration-lite tests
- 一版 live runtime debug workflow 文档

完成标准：
- 至少能对真实 ROS2 会话采集出结构化 evidence bundle
- 至少能稳定支持 1 个 demo workspace + 1 个 broken workspace

## 阶段 2：融合诊断与最小行动建议
预计目标：2~3 周

交付物：
- diagnosers 分层
- fusion_diagnoser
- confidence / evidence_refs / uncertainty_gaps
- 风险级别输出
- workflow benchmark 初版

完成标准：
- 用户不再只拿到“标签”，而是拿到带证据引用和优先级的诊断结论

## 阶段 3：恢复型 benchmark 与 runbook 体系
预计目标：2~4 周

交付物：
- recovery benchmark 设计
- broken_workflows / runbooks
- 修复前后验证流程
- metrics: first hit / recovery success / MTTR

完成标准：
- 至少有 3 个真实坏案例可重复评测
- benchmark 开始和现场恢复能力建立关联

## 阶段 4：Hermes-native 集成强化
预计目标：2~4 周

交付物：
- tool registry / cli
- capability contract
- skill manifest / validation
- post-install validation
- MCP readiness assets
- gateway/cron demo

完成标准：
- 用户能更清楚地区分 repo assets、profile、runtime capability
- Hermes 集成不再只是模板复制

## 15. 如果只允许你先做 5 件事，最该做什么

如果时间紧，酥酥建议你什么都别贪，一次只打最值钱的点。

最优先 5 件事：
1. 做 ros2_graph_collect.py
2. 做 ros2_tf_collect.py
3. 做 ros2_controller_collect.py
4. 做 runtime_schema.py + evidence bundle
5. 做 fusion_diagnoser.py

原因很简单：
这 5 个一旦起来，项目就会第一次真正接近“runtime diagnosis platform”，而不是继续停留在“规则化知识资产仓库”。

## 16. 最后结论

ROS2-Agent 的下一阶段，不应该继续“横向铺更多文档和概念”，而应该“纵向打穿真实运行时能力”。

重构成功的标志不是：
- README 更像平台
- report 更漂亮
- 文档更多

而是：
- 它能从真实 ROS2 系统里拿证据
- 它能把问题面明显缩小
- 它能帮助用户更快恢复系统
- 它能被 benchmark 证明对现场有效
- 它和 Hermes 的关系不再只是“挂个 profile 壳”

你如果按这份路线图推进，ROS2-Agent 会从“很会描述自己想成为什么”逐步变成“它确实已经是什么”。

这才是一个真正强平台该走的路。
