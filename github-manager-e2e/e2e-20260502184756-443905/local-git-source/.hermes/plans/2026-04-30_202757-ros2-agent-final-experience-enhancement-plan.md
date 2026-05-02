# ROS2-Agent 最终增强规划（体验超越 Hermes 方向）

生成时间：2026-04-30_202757
项目路径：/home/hanhan/Desktop/ROS2-Agent
规划性质：只做最终规划，不执行实现。待用户确认后，再进入完整实施与最终收尾。

> 目标：把 ROS2-Agent 从“功能上可用的 repository-backed ROS2 平台原型”进一步增强为“在日常使用体验、交互效率、平台辨识度、学习曲线、反馈透明度上明显优于 Hermes 原生体验的专属 Agent 产品”。

---

## 0. 规划目标一句话

下一轮不再只是补功能，而是围绕“体验感强于 Hermes”做一次完整的产品化增强规划。

核心标准不是“又多了几个脚本”，而是：
1. 启动更顺手
2. 入口更统一
3. 终端交互更漂亮、更低门槛
4. 常用能力更可发现
5. 运行反馈更强
6. 学习成本更低
7. 品牌感更明确
8. 安全边界更清晰
9. 文档、命令、UI、runbook、平台表面完全一致

---

## 1. 当前状态与本轮增强定位

### 当前已经具备的基础
当前 ROS2-Agent 已具备：
- runtime collectors
- diagnosis schema + diagnosers + fusion prioritization
- workflow/recovery benchmark 资产
- registry / cli / install validation / MCP readiness / gateway demo
- 能力边界文档、质量门、执行日志体系

### 当前最大的体验短板
虽然基础平台能力已经成型，但“用户使用体验”仍明显弱于理想状态，主要体现在：
1. 启动入口分散
2. 终端没有真正的专属交互首页
3. 命令发现成本高
4. 视觉品牌感不强
5. 初学者不知道先点哪个、先跑哪个
6. collector / diagnoser / workflow / runbook 之间的入口仍然偏文档化
7. 用户对“当前模式是什么”“下一步做什么”缺少即时可视化反馈
8. 还没有形成“输入 ros2-agent 就像打开一个完整产品”的感觉

### 本轮增强的总定位
这一轮增强是：
- 最后一轮“大体验增强规划”
- 偏产品设计 + 交互设计 + 命令体验 + 品牌表面 + 信息架构 + 使用闭环
- 重点不是再扩 ROS2 技术广度，而是让同样的能力更好用、更顺手、更像成熟产品

---

## 2. 你提出的关键建议，酥酥先纳入主轴

你提出的建议会作为本轮规划的核心主轴之一：

### 目标入口体验
以后在终端输入：
- `ros2-agent`

就直接进入一个专属交互界面，而不是只看到零散文档或需要自己记命令。

### 这个交互界面的核心要求
1. 顶部显示 ROS2-Agent 专属 logo
   - 风格参考 Hermes-Agent 的 logo
   - 主色调改成浅蓝色
   - 保持机器人/Agent/专业感，但更温柔、更清爽、更有你自己的辨识度

2. 顶部展示中文使用引导
   - 不是堆说明书
   - 而是“用户第一次打开就知道怎么用”的短引导
   - 强调：怎么选命令、怎么进入执行、怎么返回、怎么查看帮助

3. 中间是“所有常用命令 + 中文解释”的交互框
   - 命令按类别组织
   - 每个命令都要有一句中文解释
   - 用户不需要背命令

4. 支持鼠标滚轮上下选择
5. 支持键盘上下方向键
6. 回车 Enter 直接执行选中的命令
7. 进入子命令后，要有明确返回路径
8. 不是一次性 demo，而是成为正式平台入口

这个建议会被吸收进下面的“P0 旗舰增强模块”。

---

## 3. 本轮增强的总体设计原则

### 原则 1：统一入口优先于继续堆功能
如果用户连能力都找不到，再多能力也没意义。

### 原则 2：终端产品感优先于脚本集合感
要从“仓库里有很多脚本”升级成“这是一个可直接使用的产品”。

### 原则 3：中文优先、引导优先
目标体验不是给高级用户看源码，而是让你自己每天真愿意打开它。

### 原则 4：品牌统一
logo、欢迎页、命令名、文档、README、运行提示必须统一成一个产品语言。

### 原则 5：常用动作一跳到达
环境检查、工作区检查、runtime 诊断、benchmark、runbook、质量门、安装验证这些高频动作必须做到 1-2 次选择可到达。

### 原则 6：视觉增强服务于效率，不做花架子
UI 再好看，也必须帮助更快理解、更快执行、更快返回。

### 原则 7：不要把 demo 写成产品完成态
尤其是 interactive launcher、gateway demo、MCP readiness，要严格区分成熟度。

---

## 4. 全局增强蓝图（建议分 8 大模块）

### 模块 A：P0 旗舰入口——`ros2-agent` 专属交互启动器
这是本轮最重要模块。

### 模块 B：终端 IA（Information Architecture，信息架构）重构
让“命令怎么组织、怎么分层、怎么被用户理解”彻底清晰。

### 模块 C：品牌与视觉系统升级
浅蓝色 logo、banner、欢迎页、状态标签、能力成熟度提示统一。

### 模块 D：交互反馈系统升级
让执行中的状态、成功/失败、下一步建议、风险提醒更像成熟产品。

### 模块 E：命令系统与快捷流升级
高频能力一键触发、支持菜单进入、支持命令执行、支持分层 drill-down。

### 模块 F：新手引导 / 帮助 / 学习路径升级
让第一次用的人不迷路。

### 模块 G：开发者体验与安装分发升级
让你在终端里“安装、启动、更新、验证”都更自然。

### 模块 H：最终文档与收尾标准升级
确保体验增强落地后，文档、测试、发布入口完全一致。

---

## 5. 模块 A：P0 旗舰入口——交互式 `ros2-agent` Launcher

## A.1 最终目标
在终端输入：
- `ros2-agent`

默认打开一个全屏或半屏 TUI（terminal UI）启动页，而不是直接跑裸脚本。

## A.2 启动页结构
建议采用 5 区结构：

### 区域 1：顶部品牌区
包含：
- 浅蓝色 ROS2-Agent logo
- 产品名：ROS2-Agent
- 一句定位说明
  - 例如：
    “面向 ROS2 工程诊断、工作流验证与平台化开发的专属 Agent”

### 区域 2：中文快速引导区
短引导，不要超过 6 行：
- ↑ / ↓ 选择命令
- 鼠标滚轮滚动选择
- Enter 执行
- Tab 切换分类
- H 查看帮助
- Q 退出

### 区域 3：命令列表区（主交互框）
按分类分组显示：
- 快速开始
- 环境与工作区
- Runtime 诊断
- Benchmark / Runbook
- 平台与配置
- 验证与质量门
- 开发者工具

每个条目显示：
- 命令名
- 中文解释
- 风险级别标签
- 成熟度标签

例如：
- 环境采集：检查当前 ROS_DISTRO、RMW、setup、命令可用性
- 工作区采集：检查 src、包结构、launch/config/urdf/xacro
- Runtime 图诊断：检查 node/topic 结构与关键 topic 消费情况

### 区域 4：右侧详情区（或底部详情区）
当焦点移动到某个命令时，显示：
- 详细说明
- 会调用哪些脚本
- 适用场景
- 风险级别
- 预期输出
- 相关 runbook / docs

### 区域 5：底部状态栏
显示：
- 当前 profile / repo path
- 当前模式（safe mode / advanced mode）
- 当前选择项
- 快捷键提示

## A.3 交互能力要求
必须规划支持：
- 键盘上下方向键选择
- 鼠标滚轮上下滚动
- Enter 执行
- Esc / Backspace 返回上一级
- H 打开帮助
- / 搜索命令
- F 收藏高频命令（后续可选）
- Q 退出

## A.4 执行后的行为设计
执行命令时建议有三种模式：
1. 直接执行并显示流式输出
2. 弹出确认页（高风险命令）
3. 跳转到子菜单（例如“诊断工具箱”）

## A.5 推荐技术实现路线
建议规划两条技术路线，优先一条：

### 方案 A：Textual / prompt_toolkit / rich 驱动的现代 TUI
优点：
- 鼠标支持更自然
- 颜色/布局更强
- 后续可扩状态面板

### 方案 B：简单 curses 风格菜单
优点：
- 依赖更少
- 更稳

建议最终规划选择：
- P0 主实现：Textual 风格 TUI
- P1 兼容降级：无鼠标/无高级终端时回退到简化菜单模式

## A.6 命令系统设计
建议为 launcher 建立命令元数据 registry，例如：
- id
- title
- description_zh
- category
- maturity
- risk_level
- entry_type（script / submenu / doc / workflow）
- command
- related_docs
- expected_output

这样菜单和 CLI 可以共用一套元数据。

## A.7 与当前平台的对接点
launcher 不应重写已有功能，而应接已有能力：
- collectors
- diagnosers
- benchmark scripts
- validation scripts
- bootstrap scripts
- docs/runbooks

它是统一入口，不是重复造轮子。

---

## 6. 模块 B：终端信息架构（IA）重构

### B.1 当前问题
现在虽然有很多能力，但用户脑内路径不自然：
- 不知道先去哪
- 不知道 collector 和 diagnoser 的关系
- 不知道 benchmark、runbook、quality gate 分别什么时候用

### B.2 目标
让信息架构符合真实使用顺序：
1. 开始使用
2. 检查环境
3. 检查工作区
4. 收集 runtime 证据
5. 做诊断
6. 看 workflow benchmark / runbook
7. 执行验证
8. 看平台状态/配置

### B.3 建议分类结构
一级菜单建议：
- 开始使用
- 诊断现场
- 工作区与构建
- Runtime 与控制
- Benchmark 与复演
- Runbook 与学习
- 平台配置
- 验证与质量门
- 开发者模式

### B.4 命名统一
所有命令、文档、菜单项要统一词汇：
- 采集 = collect
- 诊断 = diagnose
- 工作流基准 = workflow benchmark
- 恢复基准 = recovery benchmark
- 复演清单 = replay manifest

不要一个地方叫 inspect，一个地方叫 audit，一个地方叫 summarize，但实际用户不懂区别。

---

## 7. 模块 C：品牌与视觉系统升级

### C.1 浅蓝色视觉体系
你已经给出非常明确方向：
- logo 类似 Hermes-Agent
- 但主色为浅蓝色

建议规划品牌色：
- 主色：浅蓝（清爽、科技、稳定）
- 辅色：白 / 深灰 / 少量青蓝强调
- 风险色：黄 / 红仅用于提示，不喧宾夺主

### C.2 视觉资产清单
建议最终补齐：
- CLI / TUI 顶部 logo ASCII 或 SVG→终端可渲染版本
- README 用 logo
- 启动页 banner
- 颜色 token 文档
- 成熟度标签颜色规范
- 风险标签颜色规范

### C.3 品牌语言统一
建议统一对外表达：
- ROS2-Agent 不是通用聊天 Agent
- 而是你的 ROS2 工程平台助手
- 语气专业但不冷冰冰
- 中文优先

---

## 8. 模块 D：交互反馈系统升级

### D.1 执行中反馈
执行命令后要让用户立刻知道：
- 当前在做什么
- 已执行到哪一步
- 预计还剩什么
- 是否在等待用户输入

### D.2 结果反馈模板化
每次命令完成后，建议统一输出结构：
- 结果概览
- 发现的问题
- 关键证据
- 推荐下一步
- 相关文档/Runbook

### D.3 风险提示分级
统一显示：
- 只读
- 本地低风险
- 需要确认
- 高风险

### D.4 错误体验优化
错误不要只丢 traceback。
建议设计：
- 简短人话解释
- 原始错误折叠/展开
- 可能原因
- 推荐下一步

---

## 9. 模块 E：命令系统与快捷流升级

### E.1 `ros2-agent` 顶级命令族
除了默认打开 TUI，还建议规划：
- `ros2-agent ui`：显式打开交互界面
- `ros2-agent doctor`：平台健康检查
- `ros2-agent collect env`
- `ros2-agent collect workspace <path>`
- `ros2-agent collect graph`
- `ros2-agent diagnose runtime`
- `ros2-agent benchmark workflow`
- `ros2-agent benchmark recovery`
- `ros2-agent runbook list`
- `ros2-agent validate`
- `ros2-agent quality`
- `ros2-agent profile install`
- `ros2-agent profile verify`

### E.2 高频快捷入口
在 UI 首页给出：
- 一键环境检查
- 一键工作区检查
- 一键 runtime 健康检查
- 一键完整验证链
- 一键查看 runbooks
- 一键打开 benchmark 入口

### E.3 收藏/最近使用
建议规划：
- 最近使用命令
- 收藏命令
- 上次执行记录

---

## 10. 模块 F：新手引导 / 帮助 / 学习路径升级

### F.1 首次启动引导
第一次启动 `ros2-agent` 时：
- 展示 3~5 个推荐动作
- 比如：
  1. 先跑环境检查
  2. 再看工作区检查
  3. 再进入 runtime 诊断

### F.2 中文帮助中心
规划一个统一帮助页：
- 我是新手该从哪开始
- 我现在机器出问题先点哪个
- 我想验证项目状态点哪个
- 我想学习 ROS2 问题分析点哪个

### F.3 学习路径与运行路径分离
不要把“学习材料”和“执行命令”混成一锅。
应该清晰分为：
- 我要做事
- 我要学习

---

## 11. 模块 G：开发者体验与分发升级

### G.1 可执行入口脚本
你提的 `ros2-agent` 命令，最终应成为正式安装入口，不是临时 alias。

建议规划：
- pyproject console_scripts 注册 `ros2-agent`
- 安装后直接可用
- 同时保留 Python 模块入口

### G.2 启动模式分层
建议规划：
- 默认：UI 模式
- `--no-ui`：纯命令行模式
- `--safe`：只读安全模式
- `--advanced`：显示全部高级命令

### G.3 更新与版本说明
建议未来规划：
- `ros2-agent version`
- `ros2-agent changelog`
- `ros2-agent self-check`

---

## 12. 模块 H：文档、测试、收尾标准升级

### H.1 本轮规划确认后，未来实施必须同步的文件
至少会涉及：
- README.md
- README_EN.md
- docs/00_overview/quickstart.md
- docs/00_overview/developer-setup.md
- docs/00_overview/current-capability-boundaries.md
- docs/00_overview/final-platform-capability-summary.md
- docs/01_architecture/capability_contract.md
- docs/03_workflows/*
- docs/05_roadmap/*
- profile/ros2-agent/bootstrap/*
- tools/registry.py
- tools/cli.py
- 以及新增的 UI/launcher 代码

### H.2 本轮未来实施必须新增的测试类型
- TUI launcher smoke tests
- command registry integrity tests
- CLI entrypoint tests
- menu metadata consistency tests
- navigation behavior tests
- fallback mode tests
- install + launch verification tests

### H.3 本轮未来实施完成后的收尾要求
- 所有入口一致
- 所有命令帮助一致
- 所有文档与 UI 说法一致
- 所有成熟度标签一致
- 不把 demo 说成 production-ready

---

## 13. 建议的最终增强实施阶段划分（供你确认后执行）

建议下一轮“最终增强实施”分为 6 个执行阶段：

### 阶段 A：产品入口与命令架构设计落地
- `ros2-agent` 顶级入口
- 命令 registry 扩展
- CLI/launcher 元数据结构

### 阶段 B：交互式 TUI Launcher 落地
- 顶部浅蓝 logo
- 中文向导
- 分类菜单
- 鼠标滚轮 / 方向键 / Enter / 返回

### 阶段 C：命令执行流与反馈系统升级
- 执行页
- 结果页
- 风险提示
- 下一步建议

### 阶段 D：学习/帮助/运行路径统一
- 新手引导
- 帮助中心
- runbook / benchmark / collect / diagnose 的信息架构统一

### 阶段 E：安装、分发、兼容模式与测试收口
- console_scripts
- fallback mode
- install/update/verify 流程
- 全量测试

### 阶段 F：最终文档收口与产品体验审校
- README / docs / status / capability 边界
- 最终体验验收
- 收尾总结

---

## 14. 优先级排序（非常关键）

### P0 必做
1. `ros2-agent` 可执行顶级入口
2. 交互式 TUI launcher
3. 顶部浅蓝 logo + 中文向导
4. 菜单式命令选择 + 中文解释
5. 鼠标滚轮 / 键盘上下 / Enter 执行
6. 命令元数据统一 registry
7. CLI / UI / docs 的用词统一

### P1 强烈建议做
1. 结果页与风险提示统一
2. 搜索命令
3. 最近使用 / 收藏命令
4. 新手引导
5. safe / advanced mode
6. fallback 非 UI 模式

### P2 可选增强
1. 更精致的动画/过渡
2. 更复杂的多面板布局
3. 会话历史面板
4. 自定义主题
5. 更高级的鼠标交互

---

## 15. 风险与取舍

### 风险 1：为了好看把 UI 做太重
应对：
- UI 服务于效率，不做炫技

### 风险 2：实现 launcher 时重复已有能力
应对：
- launcher 只做统一入口，不重写 collector/diagnoser 核心逻辑

### 风险 3：把 demo launcher 误当成熟产品
应对：
- 文档中明确 maturity label

### 风险 4：终端兼容性不一致
应对：
- 规划 fallback 文本模式

### 风险 5：实现体验增强时破坏现有质量门
应对：
- 必须新增入口/导航测试，并跑完整质量门

---

## 16. 未来实施时的验证标准

如果你确认本规划，下一轮实施完成后必须至少通过：
1. `ros2-agent` 直接可启动
2. TUI 可展示 logo、中文引导、菜单、说明
3. 鼠标滚轮可滚动选择（若终端支持）
4. 键盘上下选择、Enter 执行可用
5. 高风险项有确认机制
6. fallback 模式可用
7. README 与 quickstart 完全更新
8. tests/tools tests/workflows 新增入口测试通过
9. full quality gate 通过
10. 最终收尾文档与执行日志更新完成

---

## 17. 最终建议

如果你要的是“体验感强于 Hermes”，那下一轮最值得做的，不是继续加更多底层 collector，而是：
- 做一个真正像产品首页的 `ros2-agent` 入口
- 做一个中文友好的交互式终端 launcher
- 做统一的信息架构和反馈系统
- 让每个高频动作都能被快速发现、快速执行、快速理解

说白了就是：
下一轮要从“工程能力已经不错”升级到“打开就想用，而且比 Hermes 更贴合你自己的工作流”。

这才是最后一轮增强最值钱的地方。

---

## 18. 本次规划交付结论

本次按你的要求：
- 只完成最终增强规划
- 不进行实现
- 规划已覆盖你提出的 launcher/logo/中文向导/滚轮选择/Enter 执行建议
- 同时补齐了全局体验增强、命令架构、品牌、引导、测试、收尾等所有关键维度

待你确认这份规划后，下一轮就可以进入：
- 完整实施
- 完整验证
- 完整收尾
