# Launcher UI Workflow

最后更新：2026-05-01

## 目标
让用户在终端输入 `ros2-agent` 时，先进入专属交互入口，而不是直接面对零散脚本与文档。

## 当前实现阶段
- 已提供统一命令 runtime 驱动的高级 TUI 工作台
- 顶部有浅蓝主题 logo 文本资产
- 有中文使用向导
- 左侧命令目录 / 中间详情 / 右侧结果工作台三栏
- 支持 `--no-ui` 命令模式
- 右侧结果面板可在 summary / next_actions / payload / raw 四种视图间切换
- `Enter` 在工作台内部执行命令，`Tab` 切换结果视图
- 支持 `/` 聚焦搜索框并过滤命令目录
- 支持 `R` 查看最近 history，`E` 查看最近错误/阻塞记录
- 重量级命令会显示更明确的外部执行提示

## 当前命令入口
- `ros2-agent`
- `ros2-agent --dump-menu-json`
- `ros2-agent --no-ui capabilities`
- `ros2-agent --no-ui collect env`
- `ros2-agent --no-ui collect workspace`
- `ros2-agent --no-ui diagnose runtime`
- `ros2-agent --no-ui benchmark workflow`
- `ros2-agent --no-ui quality`

## 交互说明
- `/`：聚焦搜索框，按标题/分类/描述/子命令过滤
- `Enter`：执行当前选中命令
- `Tab`：在 summary / next_actions / payload / raw 之间切换
- `R`：展示最近命令历史（来自 `docs/planning/COMMAND_HISTORY.jsonl`）
- `E`：展示最近错误、blocked、not_implemented 记录
- 对于 heavyweight 命令，状态栏会明确提示“建议在 TUI 外执行”

## 说明
当前已经打通：
- 统一入口
- 中文向导
- 命令元数据
- 分类发现
- 三栏工作台结果显示
- summary / next_actions / payload / raw 四视图切换
- 搜索过滤
- TUI 内 history / recent errors 快速回看
- 长任务/重量级命令状态提示
