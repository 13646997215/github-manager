"""Structured command registry for Hermes-aligned ROS2-Agent runtime."""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence

from tools.command_models import CommandSpec, NextAction


COLLECTORS = [
    "ros2_env_collect",
    "ros2_workspace_collect",
    "ros2_graph_collect",
    "ros2_tf_collect",
    "ros2_controller_collect",
]

DIAGNOSERS = [
    "env_diagnoser",
    "workspace_diagnoser",
    "build_diagnoser",
    "launch_diagnoser",
    "runtime_graph_diagnoser",
    "tf_diagnoser",
    "controller_diagnoser",
    "fusion_diagnoser",
]


COMMAND_SPECS: List[CommandSpec] = [
    CommandSpec(id="doctor", title="平台体检", description_zh="查看整体运行面与推荐的下一步检查方向", category="基础命令", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["doctor"], detail="适合第一次进入系统时快速了解平台健康状态。", handler_name="doctor"),
    CommandSpec(id="inspect", title="平台巡检", description_zh="查看关键资产、部署路径与文档入口", category="基础命令", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["inspect"], detail="适合快速查看平台关键文件和入口资产。", handler_name="inspect"),
    CommandSpec(id="history", title="最近历史", description_zh="查看最近执行过的命令、状态与摘要", category="基础命令", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["history"], detail="适合回顾最近跑过什么命令、是否成功。", handler_name="history"),
    CommandSpec(id="workflow", title="工作流总览", description_zh="列出 workflow 资产与推荐入口", category="基础命令", maturity="repository-validated", risk_level="read_only", entry_type="command", command=["workflow"], detail="适合查看有哪些 workflow / demo / diagnosis 路径。", handler_name="workflow"),
    CommandSpec(id="report", title="报告总览", description_zh="查看 benchmark/report 资产与最新摘要入口", category="基础命令", maturity="repository-validated", risk_level="read_only", entry_type="command", command=["report"], detail="适合定位最新 benchmark 和 markdown 报告。", handler_name="report"),
    CommandSpec(id="settings", title="设置说明", description_zh="只读展示当前部署路径、关键目录和交互策略", category="基础命令", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["settings"], detail="适合在不改配置的情况下理解当前系统设置边界。", handler_name="settings"),
    CommandSpec(id="help", title="帮助", description_zh="查看 Hermes 风格命令目录与说明", category="基础命令", maturity="repository-validated", risk_level="read_only", entry_type="command", command=["help"], detail="适合快速了解平台能力表面与命令分组。", handler_name="help"),
    CommandSpec(id="status", title="平台状态", description_zh="查看项目根路径、部署路径、依赖可用性与入口状态", category="基础命令", maturity="repository-validated", risk_level="read_only", entry_type="command", command=["status"], detail="适合确认当前运行环境与部署状态。", handler_name="status"),
    CommandSpec(id="quality-gate", title="完整质量门", description_zh="运行仓库验证、测试、报告与平台质量门", category="基础命令", maturity="repository-validated", risk_level="low_risk_local", entry_type="command", command=["quality"], detail="适合在改动后做完整验证与报告生成。", handler_name="quality", execution_mode="heavyweight", interactive_policy="cli_only", next_action_templates=[NextAction(kind="command", label="在 CLI 中执行完整质量门", command=["quality"], detail="请使用 --no-ui quality")]),
    CommandSpec(id="quick-env-collect", title="环境采集", description_zh="检查当前 ROS_DISTRO、RMW、setup 与核心命令可用性", category="ROS2 采集", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["collect", "env"], detail="适合第一次进入项目时先确认 ROS 基础环境是否正确。", handler_name="collect_env"),
    CommandSpec(id="collect-workspace", title="工作区采集", description_zh="检查 src、包结构、launch/config/urdf/xacro 与工作区完整性", category="ROS2 采集", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["collect", "workspace"], detail="适合确认当前工作区结构、包类型、配置资产是否齐全。", handler_name="collect_workspace"),
    CommandSpec(id="collect-graph", title="运行图采集", description_zh="收集 node/topic 运行图与关键 topic 信息", category="ROS2 采集", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["collect", "graph"], detail="适合现场快速采集 topic/node 证据。", handler_name="collect_graph"),
    CommandSpec(id="collect-tf", title="TF 采集", description_zh="收集 TF frame、缺失链、clock 线索", category="ROS2 采集", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["collect", "tf"], detail="适合排查 frame chain 与 sim time 问题。", handler_name="collect_tf"),
    CommandSpec(id="collect-controller", title="控制器采集", description_zh="收集 ros2_control 控制器状态与硬件接口", category="ROS2 采集", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["collect", "controller"], detail="适合确认 controller manager、interfaces、active/inactive 状态。", handler_name="collect_controller"),
    CommandSpec(id="diagnose-env", title="环境诊断", description_zh="基于环境快照输出环境侧诊断报告", category="ROS2 诊断", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["diagnose", "env"], detail="输出 ROS_DISTRO / setup / command availability 的结构化诊断。", handler_name="diagnose_env"),
    CommandSpec(id="diagnose-workspace", title="工作区诊断", description_zh="基于工作区快照输出结构与元数据诊断", category="ROS2 诊断", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["diagnose", "workspace"], detail="输出 package metadata / layout 问题与下一步建议。", handler_name="diagnose_workspace"),
    CommandSpec(id="diagnose-runtime", title="Runtime 图诊断", description_zh="检查 node/topic 结构和关键 topic 是否被正确消费", category="ROS2 诊断", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["diagnose", "runtime"], detail="适合现场查看 topic 是否孤立、关键传感器是否没有消费者。", handler_name="diagnose_runtime"),
    CommandSpec(id="diagnose-tf", title="TF 诊断", description_zh="输出 TF stale frame 与 missing chain 诊断", category="ROS2 诊断", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["diagnose", "tf"], detail="适合确认 TF tree 的关键链是否缺失。", handler_name="diagnose_tf"),
    CommandSpec(id="diagnose-controller", title="控制器诊断", description_zh="输出控制器激活与接口导出诊断", category="ROS2 诊断", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["diagnose", "controller"], detail="适合确认 controller activation 与 hardware interface 问题。", handler_name="diagnose_controller"),
    CommandSpec(id="inspect-workspace", title="工作区巡检", description_zh="以用户导向视图查看 workspace 结构、包数量与关键资产", category="ROS2 巡检", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["inspect", "workspace"], detail="适合快速看清当前工作区是不是完整、有哪些关键资产。", handler_name="inspect_workspace"),
    CommandSpec(id="inspect-graph", title="运行图巡检", description_zh="以用户导向视图查看 node/topic 规模与关键 topics", category="ROS2 巡检", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["inspect", "graph"], detail="适合快速理解当前 runtime graph 大体健康度。", handler_name="inspect_graph"),
    CommandSpec(id="inspect-tf", title="TF 巡检", description_zh="以用户导向视图查看 TF frame 数、缺链和 stale 线索", category="ROS2 巡检", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["inspect", "tf"], detail="适合快速看 TF 是否有明显异常。", handler_name="inspect_tf"),
    CommandSpec(id="inspect-controller", title="控制器巡检", description_zh="以用户导向视图查看 controller manager、控制器数量与状态", category="ROS2 巡检", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["inspect", "controller"], detail="适合快速看控制器层状态。", handler_name="inspect_controller"),
    CommandSpec(id="doctor-ros2", title="ROS2 体检", description_zh="综合 ROS2 环境与 workspace 给出高层体检摘要", category="ROS2 诊断", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["doctor", "ros2"], detail="适合第一次做整体验证时先跑。", handler_name="doctor_ros2"),
    CommandSpec(id="doctor-workspace", title="工作区体检", description_zh="聚焦工作区结构、元数据与建议动作", category="ROS2 诊断", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["doctor", "workspace"], detail="适合定位 workspace 层面问题。", handler_name="doctor_workspace"),
    CommandSpec(id="doctor-tf", title="TF 体检", description_zh="聚焦 TF stale / missing chain 风险并给出下一步动作", category="ROS2 诊断", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["doctor", "tf"], detail="适合排查 TF 链问题。", handler_name="doctor_tf"),
    CommandSpec(id="doctor-control", title="控制器体检", description_zh="聚焦 controller activation / interface 风险并给出下一步动作", category="ROS2 诊断", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["doctor", "control"], detail="适合排查 ros2_control 控制器问题。", handler_name="doctor_control"),
    CommandSpec(id="suggest-fix-runtime", title="运行图修复建议", description_zh="为 runtime graph 问题生成最小下一步修复建议", category="ROS2 诊断", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["suggest-fix", "runtime"], detail="适合在 diagnose runtime 后继续查看建议动作。", handler_name="suggest_fix_runtime"),
    CommandSpec(id="suggest-fix-tf", title="TF 修复建议", description_zh="为 TF stale / missing chain 生成下一步建议", category="ROS2 诊断", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["suggest-fix", "tf"], detail="适合在 diagnose tf 后继续查看建议动作。", handler_name="suggest_fix_tf"),
    CommandSpec(id="suggest-fix-controller", title="控制器修复建议", description_zh="为 controller activation / interface 问题生成下一步建议", category="ROS2 诊断", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["suggest-fix", "controller"], detail="适合在 diagnose controller 后继续查看建议动作。", handler_name="suggest_fix_controller"),
    CommandSpec(id="trace-failure", title="失败追踪", description_zh="从 fusion diagnosis 和 history 中追踪当前最值得先看的失败线索", category="ROS2 诊断", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["trace", "failure"], detail="适合把分散的诊断结果收敛成追踪入口。", handler_name="trace_failure"),
    CommandSpec(id="replay-evidence", title="证据回放", description_zh="查看 replay/evidence 资产是否存在以及从哪里进入", category="Workflow 与 Benchmark", maturity="repository-validated", risk_level="read_only", entry_type="command", command=["replay", "evidence"], detail="适合从 evidence pack/replay manifest 入口回放案例。", handler_name="replay_evidence"),
    CommandSpec(id="replay-workflow", title="工作流回放", description_zh="查看 workflow replay 入口和推荐案例", category="Workflow 与 Benchmark", maturity="repository-validated", risk_level="read_only", entry_type="command", command=["replay", "workflow"], detail="适合从 broken workflow 开始体验复演。", handler_name="replay_workflow"),
    CommandSpec(id="compare-snapshots", title="快照对比", description_zh="对比当前关键 collector 快照并给出差异摘要", category="ROS2 巡检", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["compare", "snapshots"], detail="适合比较环境、TF、controller 的高层差异。", handler_name="compare_snapshots"),
    CommandSpec(id="diagnose-fusion", title="融合诊断", description_zh="汇总多源证据并输出优先级原因与下一步探针", category="ROS2 诊断", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["diagnose", "fusion"], detail="适合在多个 collector 输出后做统一收敛。", handler_name="diagnose_fusion"),
    CommandSpec(id="benchmark-workflow", title="Workflow Benchmark", description_zh="运行工作流级 benchmark 资产与验证路径", category="Workflow 与 Benchmark", maturity="implemented prototype", risk_level="read_only", entry_type="command", command=["benchmark", "workflow"], detail="适合验证 collector + diagnoser + fusion 组合路径是否符合预期。", handler_name="benchmark_workflow", execution_mode="heavyweight", interactive_policy="cli_only", next_action_templates=[NextAction(kind="command", label="在 CLI 中运行 workflow benchmark", command=["benchmark", "workflow"], detail="请使用 --no-ui benchmark workflow")]),
    CommandSpec(id="benchmark-recovery", title="Recovery Benchmark", description_zh="查看恢复基准资产与首批案例入口", category="Workflow 与 Benchmark", maturity="early prototype", risk_level="read_only", entry_type="command", command=["benchmark", "recovery"], detail="适合查看 recovery protocol 与案例骨架。", handler_name="benchmark_recovery"),
    CommandSpec(id="runbook-list", title="Runbook 列表", description_zh="列出当前 runbook 与 broken workflow 入口", category="Workflow 与 Benchmark", maturity="repository-validated", risk_level="read_only", entry_type="command", command=["runbook", "list"], detail="适合快速查阅已有 runbook 与学习路径。", handler_name="runbook_list"),
    CommandSpec(id="validate-repo", title="仓库验证", description_zh="运行 repository validation 检查项目完整性", category="基础命令", maturity="repository-validated", risk_level="read_only", entry_type="command", command=["validate", "repo"], detail="适合在修改后确认仓库结构与关键资产仍完整。", handler_name="validate_repo", execution_mode="heavyweight", interactive_policy="cli_only", next_action_templates=[NextAction(kind="command", label="在 CLI 中执行仓库验证", command=["validate", "repo"], detail="请使用 --no-ui validate repo")]),
    CommandSpec(id="profile-install", title="Profile 安装", description_zh="安装 ros2-agent profile scaffold 到本地目标目录", category="基础命令", maturity="repository-validated", risk_level="low_risk_local", entry_type="command", command=["profile", "install"], detail="适合把 profile scaffold 安装到目标目录。", handler_name="profile_install", execution_mode="lightweight", interactive_policy="allowed_in_tui"),
    CommandSpec(id="profile-verify", title="Profile 验证", description_zh="验证已安装 profile 是否完整", category="基础命令", maturity="repository-validated", risk_level="read_only", entry_type="command", command=["profile", "verify"], detail="适合检查 profile 文件是否齐全。", handler_name="profile_verify"),
    CommandSpec(id="logs-deployment", title="部署日志", description_zh="查看体验增强与 TUI 部署执行日志入口", category="基础命令", maturity="repository-validated", risk_level="read_only", entry_type="command", command=["logs", "deployment"], detail="适合查看部署阶段的执行历史。", handler_name="logs_deployment"),
]


def list_capabilities() -> Dict[str, List[str]]:
    return {"collectors": COLLECTORS, "diagnosers": DIAGNOSERS}


def list_command_specs() -> List[CommandSpec]:
    return COMMAND_SPECS


def get_command_spec(command_parts: Sequence[str]) -> Optional[CommandSpec]:
    wanted = list(command_parts)
    for spec in COMMAND_SPECS:
        if spec.command == wanted:
            return spec
    return None


def spec_to_legacy_dict(spec: CommandSpec) -> Dict[str, object]:
    return {
        "id": spec.id,
        "title": spec.title,
        "description_zh": spec.description_zh,
        "category": spec.category,
        "maturity": spec.maturity,
        "risk_level": spec.risk_level,
        "entry_type": spec.entry_type,
        "command": spec.command,
        "detail": spec.detail,
        "execution_mode": spec.execution_mode,
        "interactive_policy": spec.interactive_policy,
        "next_actions": [action.command for action in spec.next_action_templates],
    }


def export_legacy_catalog() -> List[Dict[str, object]]:
    return [spec_to_legacy_dict(spec) for spec in COMMAND_SPECS]
