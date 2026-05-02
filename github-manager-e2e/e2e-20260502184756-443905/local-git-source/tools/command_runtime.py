"""Shared command execution runtime for Hermes-aligned ROS2-Agent."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Sequence

from tools.collectors.ros2_controller_collect import collect_controllers
from tools.collectors.ros2_env_collect import collect_environment
from tools.collectors.ros2_graph_collect import collect_runtime_graph
from tools.collectors.ros2_tf_collect import collect_tf
from tools.collectors.ros2_workspace_collect import collect_workspace
from tools.command_models import CommandResult, CommandSpec, CommandStatus, NextAction, status_to_exit_code
from tools.command_registry import get_command_spec, list_capabilities, list_command_specs
from tools.diagnosers.controller_diagnoser import diagnose_controller_snapshot
from tools.diagnosers.env_diagnoser import diagnose_environment_snapshot
from tools.diagnosers.fusion_diagnoser import fuse_runtime_evidence
from tools.diagnosers.runtime_graph_diagnoser import diagnose_runtime_graph_bundle
from tools.diagnosers.tf_diagnoser import diagnose_tf_snapshot
from tools.diagnosers.workspace_diagnoser import diagnose_workspace_snapshot
from tools.schemas.runtime_schema import (
    CollectionMetadata,
    ControllerSnapshot,
    ControllerStateSnapshot,
    EnvironmentSnapshot,
    RuntimeEvidenceBundle,
    TfSnapshot,
    TopicEndpointSnapshot,
    TopicSnapshot,
    WorkspacePackageSnapshot,
    WorkspaceSnapshot,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE_DIR = REPO_ROOT / ".artifacts" / "demo-profile"
DEPLOYMENT_ROOT = Path("/home/hanhan/Desktop/.ros2-agent")
DEPLOYMENT_LOG = REPO_ROOT / "docs" / "planning" / "EXECUTION_LOG_TUI_DEPLOYMENT.md"
RUNBOOK_DIR = REPO_ROOT / "docs" / "03_runbooks"
BROKEN_WORKFLOW_DIR = REPO_ROOT / "examples" / "broken_workflows"


class CommandNotImplementedError(RuntimeError):
    pass


class CommandExecutionError(RuntimeError):
    pass


def _result_from_spec(
    spec: CommandSpec,
    *,
    status: CommandStatus,
    summary: str,
    payload: object = None,
    highlights: List[str] | None = None,
    next_actions: List[NextAction] | None = None,
    raw_output: str | None = None,
    metadata: Dict[str, object] | None = None,
) -> CommandResult:
    return CommandResult(
        status=status,
        summary=summary,
        payload=payload,
        highlights=highlights or [],
        next_actions=next_actions if next_actions is not None else list(spec.next_action_templates),
        raw_output=raw_output,
        risk_level=spec.risk_level,
        exit_code=status_to_exit_code(status),
        command=list(spec.command),
        command_id=spec.id,
        execution_mode=spec.execution_mode,
        maturity=spec.maturity,
        metadata=metadata or {},
    )


def _status_payload() -> Dict[str, object]:
    deploy_entry = DEPLOYMENT_ROOT / "ros2-agent"
    deploy_python = DEPLOYMENT_ROOT / "venv" / "bin" / "python"
    return {
        "project_root": str(REPO_ROOT),
        "deployment_root": str(DEPLOYMENT_ROOT),
        "deployment_entry": str(deploy_entry),
        "deployment_entry_exists": deploy_entry.exists(),
        "deployment_python": str(deploy_python),
        "deployment_python_exists": deploy_python.exists(),
    }


def _read_json_if_present(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {"exists": False, "path": str(path)}
    try:
        return {"exists": True, "path": str(path), "content": json.loads(path.read_text(encoding="utf-8"))}
    except json.JSONDecodeError:
        return {"exists": True, "path": str(path), "content": path.read_text(encoding="utf-8")}


def _require_path(path: Path, kind: str) -> None:
    if not path.exists():
        raise CommandExecutionError(f"{kind} 不存在：{path}")


def _environment_snapshot_model() -> EnvironmentSnapshot:
    raw = collect_environment(workspace_path=str(REPO_ROOT))
    return EnvironmentSnapshot(
        metadata=CollectionMetadata(**raw["metadata"]),
        os_name=raw["os_name"],
        os_version=raw["os_version"],
        ros_distro=raw.get("ros_distro"),
        expected_ros_distro=raw["expected_ros_distro"],
        rmw_implementation=raw.get("rmw_implementation"),
        setup_bash_path=raw.get("setup_bash_path"),
        setup_bash_exists=raw["setup_bash_exists"],
        workspace_path=raw.get("workspace_path"),
        commands=[],
        underlay_paths=list(raw.get("underlay_paths", [])),
        overlay_paths=list(raw.get("overlay_paths", [])),
        failures=list(raw.get("failures", [])),
        repair_hints=list(raw.get("repair_hints", [])),
    )


def _workspace_snapshot_model() -> WorkspaceSnapshot:
    raw = collect_workspace(str(REPO_ROOT))
    packages = [WorkspacePackageSnapshot(**package) for package in raw.get("packages", [])]
    return WorkspaceSnapshot(
        metadata=CollectionMetadata(**raw["metadata"]),
        workspace_root=raw["workspace_root"],
        looks_like_ros2_workspace=raw["looks_like_ros2_workspace"],
        package_count=raw.get("package_count", 0),
        packages=packages,
        launch_files=list(raw.get("launch_files", [])),
        config_files=list(raw.get("config_files", [])),
        urdf_files=list(raw.get("urdf_files", [])),
        xacro_files=list(raw.get("xacro_files", [])),
        install_dir_exists=raw.get("install_dir_exists", False),
        build_dir_exists=raw.get("build_dir_exists", False),
        log_dir_exists=raw.get("log_dir_exists", False),
        metadata_issues=list(raw.get("metadata_issues", [])),
        recommended_next_step=raw.get("recommended_next_step", "review_workspace"),
    )


def _tf_snapshot_model() -> TfSnapshot:
    raw = collect_tf()
    return TfSnapshot(
        metadata=CollectionMetadata(**raw["metadata"]),
        frame_count=raw.get("frame_count", 0),
        stale_frames=list(raw.get("stale_frames", [])),
        missing_chains=list(raw.get("missing_chains", [])),
        frame_authorities=dict(raw.get("frame_authorities", {})),
        sim_time_enabled=raw.get("sim_time_enabled"),
        clock_topic_present=raw.get("clock_topic_present"),
    )


def _controller_snapshot_model() -> ControllerSnapshot:
    raw = collect_controllers()
    controllers = [ControllerStateSnapshot(**item) for item in raw.get("controllers", [])]
    return ControllerSnapshot(
        metadata=CollectionMetadata(**raw["metadata"]),
        controller_manager_available=raw.get("controller_manager_available", False),
        controllers=controllers,
        hardware_interfaces=list(raw.get("hardware_interfaces", [])),
        manager_namespace=raw.get("manager_namespace"),
    )


def _runtime_bundle_model() -> RuntimeEvidenceBundle:
    graph = collect_runtime_graph()
    topics = []
    for item in graph.get("topics", []):
        publishers = [TopicEndpointSnapshot(**endpoint) for endpoint in item.get("publishers", [])]
        subscribers = [TopicEndpointSnapshot(**endpoint) for endpoint in item.get("subscribers", [])]
        topics.append(
            TopicSnapshot(
                name=item["name"],
                publisher_count=item.get("publisher_count", 0),
                subscriber_count=item.get("subscriber_count", 0),
                category=item.get("category", "general"),
                message_type=item.get("message_type"),
                qos_profile=item.get("qos_profile"),
                sample_rate_hz=item.get("sample_rate_hz"),
                publishers=publishers,
                subscribers=subscribers,
            )
        )
    return RuntimeEvidenceBundle(
        environment=_environment_snapshot_model(),
        workspace=_workspace_snapshot_model(),
        topics=topics,
        tf=_tf_snapshot_model(),
        controller=_controller_snapshot_model(),
        bundle_warnings=list(graph.get("metadata", {}).get("warnings", [])),
    )


HISTORY_LOG = REPO_ROOT / "docs" / "planning" / "COMMAND_HISTORY.jsonl"
WORKFLOW_DOC_DIR = REPO_ROOT / "docs" / "03_workflows"
BENCHMARK_REPORT = REPO_ROOT / "benchmarks" / "reports" / "latest_benchmark_report.md"
MARKDOWN_REPORT = REPO_ROOT / "reports" / "latest_markdown_report.md"


def _append_history(result: CommandResult) -> None:
    HISTORY_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "command": result.command,
        "command_id": result.command_id,
        "status": result.status.value,
        "summary": result.summary,
        "exit_code": result.exit_code,
        "execution_mode": result.execution_mode,
    }
    with HISTORY_LOG.open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _read_recent_history(limit: int = 20) -> List[Dict[str, object]]:
    if not HISTORY_LOG.exists():
        return []
    lines = [line for line in HISTORY_LOG.read_text(encoding='utf-8').splitlines() if line.strip()]
    recent = lines[-limit:]
    parsed = []
    for line in reversed(recent):
        try:
            parsed.append(json.loads(line))
        except json.JSONDecodeError:
            parsed.append({"raw": line, "status": "corrupt"})
    return parsed


def _handle_doctor(spec: CommandSpec) -> CommandResult:
    status_payload = _status_payload()
    payload = {
        "deployment_entry_exists": status_payload["deployment_entry_exists"],
        "deployment_python_exists": status_payload["deployment_python_exists"],
        "history_log_exists": HISTORY_LOG.exists(),
        "workflow_docs": len(list(WORKFLOW_DOC_DIR.glob('*.md'))) if WORKFLOW_DOC_DIR.exists() else 0,
    }
    highlights = [
        f"deployment_entry_exists: {payload['deployment_entry_exists']}",
        f"deployment_python_exists: {payload['deployment_python_exists']}",
        f"workflow_docs: {payload['workflow_docs']}",
    ]
    next_actions = [
        NextAction(kind="command", label="查看平台状态", command=["status"], detail="先确认部署入口与运行环境"),
        NextAction(kind="command", label="运行环境采集", command=["collect", "env"], detail="确认 ROS 基础环境"),
    ]
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成平台体检。", payload=payload, highlights=highlights, next_actions=next_actions)


def _handle_inspect(spec: CommandSpec) -> CommandResult:
    payload = {
        "project_root": str(REPO_ROOT),
        "deployment_root": str(DEPLOYMENT_ROOT),
        "workflow_docs": sorted(str(path.relative_to(REPO_ROOT)) for path in WORKFLOW_DOC_DIR.glob('*.md')) if WORKFLOW_DOC_DIR.exists() else [],
        "capability_docs": [
            "docs/00_overview/current-capability-boundaries.md",
            "docs/00_overview/final-platform-capability-summary.md",
            "docs/01_architecture/capability_contract.md",
        ],
    }
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成平台巡检。", payload=payload)


def _handle_history(spec: CommandSpec) -> CommandResult:
    payload = {"entries": _read_recent_history()}
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已读取最近命令历史。", payload=payload, highlights=[f"recent_entries: {len(payload['entries'])}"])


def _handle_workflow(spec: CommandSpec) -> CommandResult:
    payload = {
        "workflow_docs": sorted(str(path.relative_to(REPO_ROOT)) for path in WORKFLOW_DOC_DIR.glob('*.md')) if WORKFLOW_DOC_DIR.exists() else [],
        "recommended_entry": "docs/03_workflows/fusion-diagnosis-workflow.md",
    }
    next_actions = [NextAction(kind="command", label="查看 runbook 列表", command=["runbook", "list"], detail="从 runbook 开始体验具体案例")]
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已列出 workflow 资产。", payload=payload, next_actions=next_actions)


def _handle_report(spec: CommandSpec) -> CommandResult:
    payload = {
        "benchmark_report_exists": BENCHMARK_REPORT.exists(),
        "benchmark_report": str(BENCHMARK_REPORT),
        "markdown_report_exists": MARKDOWN_REPORT.exists(),
        "markdown_report": str(MARKDOWN_REPORT),
    }
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已整理报告资产入口。", payload=payload)


def _handle_settings(spec: CommandSpec) -> CommandResult:
    payload = {
        "deployment_root": str(DEPLOYMENT_ROOT),
        "default_profile_dir": str(DEFAULT_PROFILE_DIR),
        "history_log": str(HISTORY_LOG),
        "tui_policy": {
            "left_click": "select_only",
            "mouse_wheel": "scroll_only",
            "enter": "execute",
        },
    }
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已展示当前只读设置说明。", payload=payload)

def _handle_help(spec: CommandSpec) -> CommandResult:
    grouped: Dict[str, List[CommandSpec]] = {}
    for item in list_command_specs():
        grouped.setdefault(item.category, []).append(item)
    lines = ["ROS2-Agent Hermes 对齐命令面", ""]
    for category, specs in grouped.items():
        lines.append(f"[{category}]")
        for item in specs:
            lines.append(f"- {' '.join(item.command)}")
            lines.append(f"  {item.title} | {item.description_zh}")
        lines.append("")
    summary = "已生成命令目录与说明。"
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary=summary, raw_output="\n".join(lines).strip(), highlights=[f"命令总数：{len(list_command_specs())}"])


def _handle_status(spec: CommandSpec) -> CommandResult:
    payload = _status_payload()
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已收集当前平台状态。", payload=payload, highlights=[f"部署入口存在：{payload['deployment_entry_exists']}", f"部署 Python 存在：{payload['deployment_python_exists']}"])


def _handle_quality(spec: CommandSpec) -> CommandResult:
    return _result_from_spec(spec, status=CommandStatus.BLOCKED, summary="quality 命令属于重量级验证流程，需在 TUI 外部运行。", raw_output="quality 命令需在 TUI 外部运行；请使用 --no-ui quality")


def _handle_collect_env(spec: CommandSpec) -> CommandResult:
    payload = collect_environment(workspace_path=str(REPO_ROOT))
    highlights = [f"ROS_DISTRO: {payload.get('ros_distro') or 'unset'}", f"failures: {len(payload.get('failures', []))}"]
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成环境采集。", payload=payload, highlights=highlights)


def _handle_collect_workspace(spec: CommandSpec) -> CommandResult:
    payload = collect_workspace(str(REPO_ROOT))
    highlights = [f"package_count: {payload.get('package_count', 0)}", f"looks_like_ros2_workspace: {payload.get('looks_like_ros2_workspace')}" ]
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成工作区采集。", payload=payload, highlights=highlights)


def _handle_collect_graph(spec: CommandSpec) -> CommandResult:
    payload = collect_runtime_graph()
    highlights = [f"nodes: {len(payload.get('nodes', []))}", f"topics: {len(payload.get('topics', []))}"]
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成运行图采集。", payload=payload, highlights=highlights)


def _handle_collect_tf(spec: CommandSpec) -> CommandResult:
    payload = collect_tf()
    highlights = [f"frame_count: {payload.get('frame_count', 0)}", f"stale_frames: {len(payload.get('stale_frames', []))}"]
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成 TF 采集。", payload=payload, highlights=highlights)


def _handle_collect_controller(spec: CommandSpec) -> CommandResult:
    payload = collect_controllers()
    highlights = [f"controllers: {len(payload.get('controllers', []))}", f"controller_manager_available: {payload.get('controller_manager_available')}" ]
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成控制器采集。", payload=payload, highlights=highlights)


def _handle_diagnose_env(spec: CommandSpec) -> CommandResult:
    payload = diagnose_environment_snapshot(_environment_snapshot_model())
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成环境诊断。", payload=payload)


def _handle_diagnose_workspace(spec: CommandSpec) -> CommandResult:
    payload = diagnose_workspace_snapshot(_workspace_snapshot_model())
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成工作区诊断。", payload=payload)


def _handle_diagnose_runtime(spec: CommandSpec) -> CommandResult:
    payload = diagnose_runtime_graph_bundle(_runtime_bundle_model())
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成 runtime 图诊断。", payload=payload)


def _handle_diagnose_tf(spec: CommandSpec) -> CommandResult:
    payload = diagnose_tf_snapshot(_tf_snapshot_model())
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成 TF 诊断。", payload=payload)


def _handle_diagnose_controller(spec: CommandSpec) -> CommandResult:
    payload = diagnose_controller_snapshot(_controller_snapshot_model())
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成控制器诊断。", payload=payload)


def _handle_diagnose_fusion(spec: CommandSpec) -> CommandResult:
    reports = [
        diagnose_environment_snapshot(_environment_snapshot_model()),
        diagnose_workspace_snapshot(_workspace_snapshot_model()),
        diagnose_runtime_graph_bundle(_runtime_bundle_model()),
        diagnose_tf_snapshot(_tf_snapshot_model()),
        diagnose_controller_snapshot(_controller_snapshot_model()),
    ]
    payload = fuse_runtime_evidence(bundle=None, diagnosis_reports=reports)
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成融合诊断。", payload=payload)


def _handle_benchmark_workflow(spec: CommandSpec) -> CommandResult:
    return _result_from_spec(spec, status=CommandStatus.BLOCKED, summary="workflow benchmark 属于重量级流程，需在 TUI 外部运行。", raw_output="benchmark workflow 需在 TUI 外部运行；请使用 --no-ui benchmark workflow")


def _handle_benchmark_recovery(spec: CommandSpec) -> CommandResult:
    payload = _read_json_if_present(REPO_ROOT / "benchmarks" / "recovery" / "replay_manifest.json")
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已读取 recovery benchmark 入口资产。", payload=payload)


def _handle_runbook_list(spec: CommandSpec) -> CommandResult:
    payload = {
        "runbooks": sorted(str(path.relative_to(REPO_ROOT)) for path in RUNBOOK_DIR.rglob("*.md")) if RUNBOOK_DIR.exists() else [],
        "broken_workflows": sorted(str(path.relative_to(REPO_ROOT)) for path in BROKEN_WORKFLOW_DIR.rglob("*")) if BROKEN_WORKFLOW_DIR.exists() else [],
    }
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已列出 runbook 与 broken workflow 资产。", payload=payload)


def _handle_validate_repo(spec: CommandSpec) -> CommandResult:
    return _result_from_spec(spec, status=CommandStatus.BLOCKED, summary="repository validation 属于重量级流程，需在 TUI 外部运行。", raw_output="validate repo 需在 TUI 外部运行；请使用 --no-ui validate repo")


def _handle_profile_install(spec: CommandSpec) -> CommandResult:
    target = DEFAULT_PROFILE_DIR
    target.mkdir(parents=True, exist_ok=True)
    profile_manifest = target / "profile_manifest.json"
    profile_manifest.write_text(
        json.dumps({"profile_name": "ros2-agent-demo", "project_root": str(REPO_ROOT), "installed_from": "tools.command_runtime profile install"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    payload = {"installed": True, "target": str(target), "manifest": str(profile_manifest)}
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成 demo profile 安装。", payload=payload)


def _handle_profile_verify(spec: CommandSpec) -> CommandResult:
    target = DEFAULT_PROFILE_DIR
    manifest = target / "profile_manifest.json"
    payload = {"profile_root": str(target), "exists": target.exists(), "manifest_exists": manifest.exists()}
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已检查 profile 安装状态。", payload=payload)


def _handle_logs_deployment(spec: CommandSpec) -> CommandResult:
    _require_path(DEPLOYMENT_LOG, "部署日志")
    raw_output = DEPLOYMENT_LOG.read_text(encoding="utf-8")
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已读取部署执行日志。", raw_output=raw_output)


def _highlights_from_diagnosis(payload: Dict[str, object]) -> List[str]:
    findings = payload.get("findings", []) if isinstance(payload, dict) else []
    causes = payload.get("candidate_causes", []) if isinstance(payload, dict) else []
    domain = payload.get("domain", "unknown") if isinstance(payload, dict) else "unknown"
    highlights = [f"domain: {domain}", f"findings: {len(findings)}", f"candidate_causes: {len(causes)}"]
    if causes:
        top = causes[0]
        if isinstance(top, dict) and top.get("cause"):
            highlights.append(f"top_cause: {top['cause']}")
    return highlights


def _next_actions_from_diagnosis(payload: Dict[str, object]) -> List[NextAction]:
    next_probe = payload.get("recommended_next_probe") if isinstance(payload, dict) else None
    if isinstance(next_probe, dict):
        action = next_probe.get("action", "review_diagnosis")
        reason = next_probe.get("reason")
    else:
        action = str(next_probe or "review_diagnosis")
        reason = None
    return [NextAction(kind="hint", label=action, detail=reason)]


def _render_snapshot_summary(title: str, items: List[str], extra: List[str] | None = None) -> str:
    lines = [title]
    lines.extend(f"- {item}" for item in items)
    if extra:
        lines.append("")
        lines.extend(extra)
    return "\n".join(lines)


def _handle_inspect_workspace(spec: CommandSpec) -> CommandResult:
    payload = collect_workspace(str(REPO_ROOT))
    items = [
        f"package_count: {payload.get('package_count', 0)}",
        f"looks_like_ros2_workspace: {payload.get('looks_like_ros2_workspace')}",
        f"launch_files: {len(payload.get('launch_files', []))}",
        f"config_files: {len(payload.get('config_files', []))}",
    ]
    raw_output = _render_snapshot_summary("工作区巡检摘要", items, [f"recommended_next_step: {payload.get('recommended_next_step', 'review_workspace')}"])
    next_actions = [NextAction(kind="command", label="进一步做工作区诊断", command=["diagnose", "workspace"], detail="查看 metadata / layout 问题")]
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成工作区巡检。", payload=payload, highlights=items, next_actions=next_actions, raw_output=raw_output)


def _handle_inspect_graph(spec: CommandSpec) -> CommandResult:
    payload = collect_runtime_graph()
    critical = [topic.get('name') for topic in payload.get('topics', []) if topic.get('category') == 'critical_sensor']
    items = [
        f"nodes: {len(payload.get('nodes', []))}",
        f"topics: {len(payload.get('topics', []))}",
        f"critical_sensor_topics: {len(critical)}",
    ]
    raw_output = _render_snapshot_summary("运行图巡检摘要", items, ["critical topics: " + (", ".join(critical) if critical else "none")])
    next_actions = [NextAction(kind="command", label="进一步做 runtime 图诊断", command=["diagnose", "runtime"], detail="查看 orphan topic / unconsumed sensor")]
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成运行图巡检。", payload=payload, highlights=items, next_actions=next_actions, raw_output=raw_output)


def _handle_inspect_tf(spec: CommandSpec) -> CommandResult:
    payload = collect_tf()
    items = [
        f"frame_count: {payload.get('frame_count', 0)}",
        f"stale_frames: {len(payload.get('stale_frames', []))}",
        f"missing_chains: {len(payload.get('missing_chains', []))}",
    ]
    raw_output = _render_snapshot_summary("TF 巡检摘要", items, ["missing chains: " + (", ".join(payload.get('missing_chains', [])) or 'none')])
    next_actions = [NextAction(kind="command", label="进一步做 TF 诊断", command=["diagnose", "tf"], detail="查看 stale frame / missing chain 风险")]
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成 TF 巡检。", payload=payload, highlights=items, next_actions=next_actions, raw_output=raw_output)


def _handle_inspect_controller(spec: CommandSpec) -> CommandResult:
    payload = collect_controllers()
    inactive = [item.get('name') for item in payload.get('controllers', []) if item.get('state') in {'inactive', 'unconfigured', 'failed'}]
    items = [
        f"controller_manager_available: {payload.get('controller_manager_available')}",
        f"controllers: {len(payload.get('controllers', []))}",
        f"inactive_or_failed: {len(inactive)}",
    ]
    raw_output = _render_snapshot_summary("控制器巡检摘要", items, ["inactive/failed: " + (", ".join(inactive) if inactive else 'none')])
    next_actions = [NextAction(kind="command", label="进一步做控制器诊断", command=["diagnose", "controller"], detail="查看 activation / interface 风险")]
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成控制器巡检。", payload=payload, highlights=items, next_actions=next_actions, raw_output=raw_output)


def _handle_doctor_ros2(spec: CommandSpec) -> CommandResult:
    env_payload = collect_environment(workspace_path=str(REPO_ROOT))
    ws_payload = collect_workspace(str(REPO_ROOT))
    highlights = [
        f"ROS_DISTRO: {env_payload.get('ros_distro') or 'unset'}",
        f"env_failures: {len(env_payload.get('failures', []))}",
        f"workspace_packages: {ws_payload.get('package_count', 0)}",
    ]
    payload = {"environment": env_payload, "workspace": ws_payload}
    next_actions = [NextAction(kind="command", label="做融合诊断", command=["diagnose", "fusion"], detail="进入更高层收敛")]
    raw_output = _render_snapshot_summary("ROS2 体检摘要", highlights)
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成 ROS2 体检。", payload=payload, highlights=highlights, next_actions=next_actions, raw_output=raw_output)


def _handle_doctor_workspace(spec: CommandSpec) -> CommandResult:
    payload = diagnose_workspace_snapshot(_workspace_snapshot_model())
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成工作区体检。", payload=payload, highlights=_highlights_from_diagnosis(payload), next_actions=_next_actions_from_diagnosis(payload))


def _handle_doctor_tf(spec: CommandSpec) -> CommandResult:
    payload = diagnose_tf_snapshot(_tf_snapshot_model())
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成 TF 体检。", payload=payload, highlights=_highlights_from_diagnosis(payload), next_actions=_next_actions_from_diagnosis(payload))


def _handle_doctor_control(spec: CommandSpec) -> CommandResult:
    payload = diagnose_controller_snapshot(_controller_snapshot_model())
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已完成控制器体检。", payload=payload, highlights=_highlights_from_diagnosis(payload), next_actions=_next_actions_from_diagnosis(payload))


def _handle_suggest_fix_runtime(spec: CommandSpec) -> CommandResult:
    payload = diagnose_runtime_graph_bundle(_runtime_bundle_model())
    next_actions = _next_actions_from_diagnosis(payload)
    next_actions.append(NextAction(kind="command", label="再次检查 runtime 图", command=["inspect", "graph"], detail="先确认 topic 和 consumer 分布"))
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已生成 runtime 图修复建议。", payload=payload, highlights=_highlights_from_diagnosis(payload), next_actions=next_actions)


def _handle_suggest_fix_tf(spec: CommandSpec) -> CommandResult:
    payload = diagnose_tf_snapshot(_tf_snapshot_model())
    next_actions = _next_actions_from_diagnosis(payload)
    next_actions.append(NextAction(kind="command", label="再次检查 TF", command=["inspect", "tf"], detail="先确认缺链和 stale frame"))
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已生成 TF 修复建议。", payload=payload, highlights=_highlights_from_diagnosis(payload), next_actions=next_actions)


def _handle_suggest_fix_controller(spec: CommandSpec) -> CommandResult:
    payload = diagnose_controller_snapshot(_controller_snapshot_model())
    next_actions = _next_actions_from_diagnosis(payload)
    next_actions.append(NextAction(kind="command", label="再次检查控制器", command=["inspect", "controller"], detail="先确认 inactive / interface 问题"))
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已生成控制器修复建议。", payload=payload, highlights=_highlights_from_diagnosis(payload), next_actions=next_actions)


def _handle_trace_failure(spec: CommandSpec) -> CommandResult:
    reports = [
        diagnose_environment_snapshot(_environment_snapshot_model()),
        diagnose_workspace_snapshot(_workspace_snapshot_model()),
        diagnose_runtime_graph_bundle(_runtime_bundle_model()),
        diagnose_tf_snapshot(_tf_snapshot_model()),
        diagnose_controller_snapshot(_controller_snapshot_model()),
    ]
    fusion_payload = fuse_runtime_evidence(bundle=None, diagnosis_reports=reports)
    history = _read_recent_history(limit=5)
    payload = {"fusion": fusion_payload, "recent_history": history}
    highlights = []
    top = fusion_payload.get('prioritized_candidates', []) if isinstance(fusion_payload, dict) else []
    if top:
        highlights.append(f"top_failure_cause: {top[0].get('cause')}")
    highlights.append(f"recent_history: {len(history)}")
    next_actions = [NextAction(kind="command", label="查看融合诊断", command=["diagnose", "fusion"], detail="先确认最高优先级原因")]
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary="已追踪当前主要失败线索。", payload=payload, highlights=highlights, next_actions=next_actions)


def _handle_replay_evidence(spec: CommandSpec) -> CommandResult:
    evidence_dir = REPO_ROOT / 'benchmarks' / 'reports' / 'evidence'
    payload = {
        'evidence_dir_exists': evidence_dir.exists(),
        'evidence_dir': str(evidence_dir),
        'files': sorted(str(path.relative_to(REPO_ROOT)) for path in evidence_dir.rglob('*') if path.is_file()) if evidence_dir.exists() else [],
        'replay_manifest_template': str(REPO_ROOT / 'benchmarks' / 'reports' / 'replay_manifest_template.json'),
    }
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary='已整理 evidence replay 入口。', payload=payload)


def _handle_replay_workflow(spec: CommandSpec) -> CommandResult:
    workflows = REPO_ROOT / 'benchmarks' / 'workflows'
    payload = {
        'workflow_root': str(workflows),
        'cases': sorted(str(path.relative_to(REPO_ROOT)) for path in workflows.iterdir()) if workflows.exists() else [],
    }
    next_actions = [NextAction(kind='command', label='查看 runbook 列表', command=['runbook', 'list'], detail='配合 runbook 一起复演')]
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary='已整理 workflow replay 入口。', payload=payload, next_actions=next_actions)


def _handle_compare_snapshots(spec: CommandSpec) -> CommandResult:
    env_payload = collect_environment(workspace_path=str(REPO_ROOT))
    tf_payload = collect_tf()
    controller_payload = collect_controllers()
    payload = {
        'environment_failures': len(env_payload.get('failures', [])),
        'tf_missing_chains': len(tf_payload.get('missing_chains', [])),
        'tf_stale_frames': len(tf_payload.get('stale_frames', [])),
        'inactive_or_failed_controllers': len([item for item in controller_payload.get('controllers', []) if item.get('state') in {'inactive', 'unconfigured', 'failed'}]),
    }
    highlights = [f"environment_failures: {payload['environment_failures']}", f"tf_missing_chains: {payload['tf_missing_chains']}", f"inactive_or_failed_controllers: {payload['inactive_or_failed_controllers']}"]
    return _result_from_spec(spec, status=CommandStatus.SUCCESS, summary='已生成关键快照对比摘要。', payload=payload, highlights=highlights)

HANDLERS = {
    "doctor": _handle_doctor,
    "inspect": _handle_inspect,
    "history": _handle_history,
    "workflow": _handle_workflow,
    "report": _handle_report,
    "settings": _handle_settings,
    "inspect_workspace": _handle_inspect_workspace,
    "inspect_graph": _handle_inspect_graph,
    "inspect_tf": _handle_inspect_tf,
    "inspect_controller": _handle_inspect_controller,
    "doctor_ros2": _handle_doctor_ros2,
    "doctor_workspace": _handle_doctor_workspace,
    "doctor_tf": _handle_doctor_tf,
    "doctor_control": _handle_doctor_control,
    "suggest_fix_runtime": _handle_suggest_fix_runtime,
    "suggest_fix_tf": _handle_suggest_fix_tf,
    "suggest_fix_controller": _handle_suggest_fix_controller,
    "trace_failure": _handle_trace_failure,
    "replay_evidence": _handle_replay_evidence,
    "replay_workflow": _handle_replay_workflow,
    "compare_snapshots": _handle_compare_snapshots,
    "help": _handle_help,
    "status": _handle_status,
    "quality": _handle_quality,
    "collect_env": _handle_collect_env,
    "collect_workspace": _handle_collect_workspace,
    "collect_graph": _handle_collect_graph,
    "collect_tf": _handle_collect_tf,
    "collect_controller": _handle_collect_controller,
    "diagnose_env": _handle_diagnose_env,
    "diagnose_workspace": _handle_diagnose_workspace,
    "diagnose_runtime": _handle_diagnose_runtime,
    "diagnose_tf": _handle_diagnose_tf,
    "diagnose_controller": _handle_diagnose_controller,
    "diagnose_fusion": _handle_diagnose_fusion,
    "benchmark_workflow": _handle_benchmark_workflow,
    "benchmark_recovery": _handle_benchmark_recovery,
    "runbook_list": _handle_runbook_list,
    "validate_repo": _handle_validate_repo,
    "profile_install": _handle_profile_install,
    "profile_verify": _handle_profile_verify,
    "logs_deployment": _handle_logs_deployment,
}


def execute_command(command_parts: Sequence[str]) -> CommandResult:
    parts = list(command_parts) if command_parts else ["capabilities"]
    if parts == ["capabilities"]:
        payload = list_capabilities()
        result = CommandResult(status=CommandStatus.SUCCESS, summary="已列出 collectors 与 diagnosers。", payload=payload, exit_code=0, command=parts, command_id="capabilities")
        _append_history(result)
        return result

    spec = get_command_spec(parts)
    if spec is None:
        result = CommandResult(status=CommandStatus.NOT_IMPLEMENTED, summary=f"暂未实现该命令执行入口： {parts}", raw_output=f"暂未实现该命令执行入口： {parts}", exit_code=1, command=parts)
        _append_history(result)
        return result

    handler = HANDLERS.get(spec.handler_name)
    if handler is None:
        return _result_from_spec(spec, status=CommandStatus.NOT_IMPLEMENTED, summary=f"命令处理器缺失：{spec.handler_name}", raw_output=f"命令处理器缺失：{spec.handler_name}")

    try:
        result = handler(spec)
        _append_history(result)
        return result
    except CommandExecutionError as exc:
        return _result_from_spec(spec, status=CommandStatus.ERROR, summary=str(exc), raw_output=str(exc))
    except Exception as exc:
        return _result_from_spec(spec, status=CommandStatus.ERROR, summary=f"命令执行异常：{exc}", raw_output=f"命令执行异常：{exc}")


def result_to_payload(result: CommandResult) -> Dict[str, object]:
    payload = result.to_dict()
    if payload.get("status") is not None:
        payload["status"] = result.status.value
    return payload


def result_to_json(result: CommandResult) -> str:
    return json.dumps(result_to_payload(result), ensure_ascii=False, indent=2)


def result_to_text(result: CommandResult) -> str:
    if result.raw_output:
        return result.raw_output

    lines = [result.summary]
    if result.highlights:
        lines.append("")
        lines.append("highlights:")
        lines.extend(f"- {item}" for item in result.highlights)
    if result.next_actions:
        lines.append("")
        lines.append("next_actions:")
        for action in result.next_actions:
            command = f" ({' '.join(action.command)})" if action.command else ""
            detail = f" - {action.detail}" if action.detail else ""
            lines.append(f"- {action.label}{command}{detail}")
    if result.payload is not None:
        lines.append("")
        lines.append("payload:")
        lines.append(json.dumps(result.payload, ensure_ascii=False, indent=2))
    return "\n".join(lines)
