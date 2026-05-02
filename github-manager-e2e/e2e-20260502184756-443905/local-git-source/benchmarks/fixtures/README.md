# Benchmark Fixtures Plan

此目录用于存放：
- 样例环境输出
- 样例 workspace 结构
- 样例 build 失败日志
- 样例 launch 失败日志
- 样例 runtime graph / controller / tf 异常 JSON
- 与之配套的真实风格日志片段

当前已覆盖的 fixture 类型：
- colcon success / dependency failure / interface failure / compile failure
- launch 文件缺失 / 参数文件缺失 / 运行期资产缺失
- runtime QoS 不匹配导致下游节点饥饿
- ros2_control 控制器激活失败 + TF stale frame

设计原则：
- fixture 不只是展示，而是必须能被 tests、scoring、report pipeline 共同消费
- 尽量保持贴近真实 ROS2/Humble 调试现场，避免空洞示例
- 所有 fixture 都应导向明确 next_actions，服务于专家 agent 的教学与引导能力
