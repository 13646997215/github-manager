# ROS2-Agent 第一阶段实施计划（仅规划，不执行）

生成时间：2026-04-30
项目路径：/home/hanhan/Desktop/ROS2-Agent
计划性质：纯规划文档，禁止在本计划阶段直接开始实现

> For Hermes: 下一对话请使用本计划逐项执行，但当前文档只用于规划和排程，不进行任何代码修改。

**Goal:** 为 ROS2-Agent 建立第一阶段“真实运行时接入奠基层”，优先补齐 live evidence collection、统一 schema、integration-lite 验证与最小可用工作流设计。

**Architecture:** 第一阶段不追求全平台完成，而是先打穿最关键的底层通路：collector -> schema -> basic diagnoser compatibility -> integration-lite tests -> workflow docs。所有新增设计都围绕“先拿到真实证据，再做更强推理”展开。

**Tech Stack:** Python 3.10+, ROS2 Humble CLI, 可选 rclpy/tf2 适配, pytest, 现有 validation pipeline, repo-backed documentation assets。

---

## 0. 第一阶段范围边界

### 本阶段要完成什么
1. 设计并落地 runtime schema
2. 设计并落地 env/workspace/graph/tf/controller 五类 collector 方案
3. 设计 diagnoser 如何消费 schema
4. 设计 integration-lite tests
5. 设计新的最小 live-runtime debug workflow
6. 规划 README/能力边界的同步调整点

### 本阶段明确不做什么
1. 不做大规模多 Agent 编排
2. 不做完整 MCP server
3. 不做完整 gateway/cron 自动化
4. 不做 recovery benchmark 全量实现
5. 不做大规模目录搬迁式重构

### 本阶段成功标准
- 有清晰可执行的 collector 设计与文件级落点
- 有统一 schema 草案
- 有 integration-lite test 设计
- 有最小 workflow 文档结构
- 下一对话可以直接按计划开始开发，而无需再重新拆分任务

## 1. 推荐交付顺序

### Milestone 1：Schema 与 collector 总线设计
目标：统一语言，避免后续每个工具各写各的结构

### Milestone 2：核心 collectors 设计
目标：优先让 graph / tf / controller / env 拿到真实证据

### Milestone 3：diagnoser 对接方案
目标：让现有规则层逐步迁移到 schema 驱动

### Milestone 4：integration-lite 测试方案
目标：验证 collectors 不是只会读 fixture

### Milestone 5：workflow / docs / capability 边界更新
目标：让用户知道现在到底已经能做什么、还不能做什么

## 2. 文件级实施规划

## Task 1: 设计 runtime schema 模块

**Objective:** 建立统一的运行时证据结构，作为 collector / diagnoser / benchmark / report 的共享基础。

**Files:**
- Create: `tools/schemas/runtime_schema.py`
- Create: `tests/collectors/test_runtime_schema.py`
- Modify: `pyproject.toml`（仅当需要补类型/包导出信息时，下一对话再决定）

**Planned contents:**
- EnvironmentSnapshot
- WorkspaceSnapshot
- GraphNodeSnapshot
- TopicSnapshot
- TfSnapshot
- ControllerSnapshot
- LaunchProbeSnapshot（预留）
- LogEvidence（预留）
- RuntimeEvidenceBundle
- Common metadata fields:
  - source
  - collected_at
  - command_used
  - warnings
  - collection_success

**Design notes:**
- schema 优先用 dataclass，保持当前仓库风格一致
- 所有 snapshot 应可 asdict / JSON 化
- 不要一开始引入过重依赖，比如 pydantic，除非后面证明有强需求
- 预留字段优先于一次设计过满，遵守 YAGNI

**Validation plan:**
- schema 单测验证 JSON 序列化
- 验证默认字段完整性
- 验证 RuntimeEvidenceBundle 能组合多个子 snapshot

## Task 2: 设计环境采集器 ros2_env_collect.py

**Objective:** 从真实 shell/ROS 环境中采集结构化环境事实，替换当前偏静态的 audit 语义。

**Files:**
- Create: `tools/collectors/ros2_env_collect.py`
- Create: `tests/collectors/test_ros2_env_collect.py`
- Reference existing logic: `tools/ros2_env_audit.py`

**Planned capabilities:**
- 读取 ROS_DISTRO
- 读取 RMW_IMPLEMENTATION
- 检查 `/opt/ros/humble/setup.bash`
- 检查 ros2/colcon/rosdep/python3/gazebo/rviz2
- 记录 shell 级 warning
- 产出 EnvironmentSnapshot

**Design notes:**
- 保持只读
- 区分“缺失事实”和“失败事实”
- current audit_result 可作为兼容层保留，下一阶段再迁移

**Validation plan:**
- mock 环境变量
- mock command availability
- 验证 snapshot 输出结构

## Task 3: 设计工作区采集器 ros2_workspace_collect.py

**Objective:** 对 workspace 结构进行 schema 化采集，替代当前 inspect 函数的松散输出。

**Files:**
- Create: `tools/collectors/ros2_workspace_collect.py`
- Create: `tests/collectors/test_ros2_workspace_collect.py`
- Reference existing logic: `tools/ros2_workspace_inspect.py`

**Planned capabilities:**
- 扫描 src/ 下 package.xml
- 识别 ament_python / ament_cmake
- 扫描 launch/config/urdf/xacro
- 标记 looks_like_ros2_workspace
- 标记 package metadata 异常
- 产出 WorkspaceSnapshot

**Design notes:**
- 与当前 inspect_workspace 保持功能映射关系
- 先不强行删除旧工具，采用并行过渡方案

**Validation plan:**
- 用现有 demo workspace fixture
- 用 broken workspace fixture
- 验证包数、路径、warning 分类

## Task 4: 设计运行图采集器 ros2_graph_collect.py

**Objective:** 第一次真正把项目推进到 live ROS2 runtime 采集层。

**Files:**
- Create: `tools/collectors/ros2_graph_collect.py`
- Create: `tests/collectors/test_ros2_graph_collect.py`
- Create: `tests/integration/test_ros2_graph_collect_integration.py`
- Reference existing logic: `tools/ros2_graph_inspect.py`

**Planned capabilities:**
- 调用 `ros2 node list`
- 调用 `ros2 topic list`
- 调用 `ros2 topic info --verbose`（如果可用）
- 构造 GraphNodeSnapshot / TopicSnapshot
- 分类关键 topics
- 记录原始命令 used

**Design notes:**
- 先支持 CLI 采集，rclpy 不作为第一步强依赖
- 命令失败时要有可解释错误，而不是空列表装成功
- 如果 verbose 不可用，要有 graceful degradation

**Validation plan:**
- unit 测试 mock terminal/CLI 输出
- integration-lite 测试仅验证“有 ROS 环境时可运行并返回结构化数据”
- 不在第一阶段强求全仿真环境覆盖

## Task 5: 设计 TF 采集器 ros2_tf_collect.py

**Objective:** 补齐 TF 真实采集入口，避免 tf diagnosis 永远停留在人工输入层。

**Files:**
- Create: `tools/collectors/ros2_tf_collect.py`
- Create: `tests/collectors/test_ros2_tf_collect.py`
- Create: `tests/integration/test_ros2_tf_collect_integration.py`
- Reference existing logic: `tools/ros2_tf_diagnose.py`

**Planned capabilities:**
- 支持从命令或现有 TF 工具导出结构化 frame 信息
- 记录 frame_count
- 标记 stale_frames
- 标记 missing_chains（初版可基于配置/输入期望）
- 产出 TfSnapshot

**Design notes:**
- 第一阶段允许“真实采集 + 规则补全”的混合方式
- 不要在第一阶段就做过度复杂的 TF 可视化

**Validation plan:**
- fixture 单测
- integration-lite 测试检查 collector 的返回结构

## Task 6: 设计控制器采集器 ros2_controller_collect.py

**Objective:** 让 controller diagnosis 拿到真实 ros2_control 层数据来源。

**Files:**
- Create: `tools/collectors/ros2_controller_collect.py`
- Create: `tests/collectors/test_ros2_controller_collect.py`
- Create: `tests/integration/test_ros2_controller_collect_integration.py`
- Reference existing logic: `tools/ros2_controller_diagnose.py`

**Planned capabilities:**
- 调 `ros2 control list_controllers`
- 调 `ros2 control list_hardware_interfaces`
- 解析 controller 状态
- 解析 claimed/required interfaces（第一阶段允许部分支持）
- 产出 ControllerSnapshot

**Design notes:**
- 需要仔细处理 ros2_control 环境缺失场景
- collector 应区分“命令不可用”和“当前系统没有 controller manager”

**Validation plan:**
- mock CLI 输出测试
- integration-lite 在可用环境时跑

## Task 7: 设计 collector 到 diagnoser 的兼容层

**Objective:** 避免新 collector 上线后，现有工具链完全断层。

**Files:**
- Create: `tools/diagnosers/compat_adapters.py`
- Create: `tests/diagnosers/test_compat_adapters.py`
- Planned later references:
  - `tools/ros2_graph_inspect.py`
  - `tools/ros2_controller_diagnose.py`
  - `tools/ros2_tf_diagnose.py`

**Planned capabilities:**
- 把新 schema 映射到旧 diagnoser 需要的输入
- 或反过来把旧输出包装成新 finding 结构
- 让迁移分阶段进行，不必一次翻盘

**Design notes:**
- 第一阶段的关键是兼容，不是彻底重写全部 diagnoser
- 先建立桥，再逐步替换老接口

## Task 8: 设计 fusion diagnoser 骨架

**Objective:** 提前定义多证据融合接口，但第一阶段只做骨架，不追求完整能力。

**Files:**
- Create: `tools/diagnosers/fusion_diagnoser.py`
- Create: `tests/diagnosers/test_fusion_diagnoser.py`

**Planned capabilities:**
- 输入 RuntimeEvidenceBundle
- 输出 prioritized_candidates
- 输出 evidence_refs
- 输出 uncertainty_gaps
- 输出 recommended_next_probe

**Design notes:**
- 第一阶段只做结构，不追求复杂评分模型
- 先能表达“多个证据如何被组织”即可

## Task 9: 设计 integration-lite 测试层

**Objective:** 建立“不是只测 fixture”的测试入口。

**Files:**
- Create: `tests/integration/README.md`
- Create: `tests/integration/test_ros2_graph_collect_integration.py`
- Create: `tests/integration/test_ros2_tf_collect_integration.py`
- Create: `tests/integration/test_ros2_controller_collect_integration.py`
- Modify later: `pytest.ini`
- Modify later: `.github/workflows/ci.yml`

**Planned strategy:**
- integration-lite 默认可 skip
- 在缺 ROS 环境时给出明确 skip reason
- 不把重型集成测试强塞进所有 CI job

**Validation plan:**
- 本地可运行
- CI 可分层选择

## Task 10: 设计文档与能力边界同步更新包

**Objective:** 防止代码规划推进后，README 仍旧继续夸大能力。

**Files:**
- Create: `docs/00_overview/current-capability-boundaries.md`
- Create: `docs/03_workflows/live-runtime-debug-workflow.md`
- Planned modify later: `README.md`
- Planned modify later: `docs/02_product/capability_matrix.md`

**Planned contents:**
- 什么能力已经 live
- 什么能力仍是 fixture-based
- 什么能力仍在 prototype 阶段
- 用户如何安全使用第一阶段成果

## 3. 第一阶段建议的执行顺序（下一对话使用）

推荐严格按这个顺序执行，不要跳：

1. runtime_schema.py
2. ros2_env_collect.py
3. ros2_workspace_collect.py
4. ros2_graph_collect.py
5. ros2_tf_collect.py
6. ros2_controller_collect.py
7. compat_adapters.py
8. fusion_diagnoser.py skeleton
9. tests/integration/
10. docs/current-capability-boundaries + live-runtime-debug-workflow

## 4. 第一阶段测试与验证规划

### 单元测试
重点验证：
- schema JSON 化
- collector 对 mock 输出的解析
- warning / failure 分类
- compat adapter 映射正确性

### 集成轻测
重点验证：
- collector 在有 ROS 环境时能运行
- collector 在无 ROS 环境时能合理 skip / report
- 不要求第一阶段就完整接仿真

### 回归测试
重点验证：
- 现有 tests/tools 与 tests/workflows 不被破坏
- benchmark/report pipeline 不因 collector 新增而崩溃

## 5. 风险与取舍

### 风险 1：collector 直接接 ros2 CLI 后，环境差异会导致解析脆弱
应对：
- CLI 输出解析要最小假设
- 保留 graceful degradation

### 风险 2：过早引入 rclpy/tf2 依赖会增加实现负担
应对：
- 第一阶段优先 CLI
- 第二阶段再评估更深 API 集成

### 风险 3：一次重构太大，破坏现有可用资产
应对：
- 并行新增，不强删旧工具
- 通过 compat layer 平滑迁移

### 风险 4：README 不同步更新，继续制造错觉
应对：
- 文档同步更新作为第一阶段正式交付的一部分

## 6. 下一对话的开发纪律建议

下一对话实际开始开发时，请遵守：
1. 一次只做一个任务
2. 每完成一个任务就运行对应测试
3. 优先新增文件，不先大规模改旧文件
4. 所有新能力先最小可用，再逐步增强
5. 任何会扩大范围的想法，先记到后续阶段，不在第一阶段膨胀

## 7. 第一阶段完成后的预期成果

如果下一对话按本计划推进完成，ROS2-Agent 将至少获得这些实质性提升：
- 第一次具备 live runtime evidence collection 基础
- 第一次拥有统一 runtime schema
- 第一次建立 fixture reasoning 向 live diagnosis 迁移的桥梁
- 第一次能更诚实地区分 repository-validated 和 live-capable 能力

这会让项目从“规则资产仓库”正式迈向“现场诊断平台雏形”。
