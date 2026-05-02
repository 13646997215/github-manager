# Competitive Runtime Differentiators

ROS2-Agent 想真正吸引大量用户，核心不只是 persona 或 prompt，而是要在历史性难题上建立可信优势。

## 必须正面攻克的历史难题
- 环境会话污染：source 顺序、overlay 污染、依赖版本漂移。
- colcon 失败信息碎片化：新手看不懂第一失败包，老手懒得人工总结。
- launch 成功但系统不可用：参数存在但运行期资产缺失。
- runtime 图存在但数据不通：QoS mismatch、topic starvation、controller activation failure。
- 诊断结果难沉淀：一次排障有结论，但没有形成可复验资产。

## ROS2-Agent 的差异化方向
- Structured diagnosis first：优先结构化事实，再做教学解释。
- Benchmark-backed expertise：每种“专家判断”都尽量有 fixture 与测试支撑。
- Teaching-grade next actions：不是只报错，而是给出适合新手和工程师都能执行的 next actions。
- Repo-native automation：报告、验证、评分、导出全部留在仓库内，便于 GitHub 社区复现。
- Runtime-centric credibility：真正覆盖 ROS2 项目最痛的 bring-up / runtime 层问题。

## 对 GitHub 用户为什么有吸引力
- 能拿来学：有技能、文档、分层路线图。
- 能拿来用：有结构化工具、验证脚本、报告资产。
- 能拿来改：有测试、fixtures、评分、模板，方便贡献。
- 能看出专业性：不是“通用 AI 套壳”，而是 ROS2 仿真开发的工程专家平台。
