import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, '-m', 'tools.cli', *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def test_cli_help_like_render_contains_categories():
    result = run_cli('--dump-menu-json')
    assert '基础命令' in result.stdout
    assert 'ROS2 采集' in result.stdout
    assert 'ROS2 诊断' in result.stdout


def test_cli_no_ui_capabilities_json_works():
    result = run_cli('--no-ui', 'capabilities')
    assert 'collectors' in result.stdout
    assert 'diagnosers' in result.stdout


def test_cli_tui_text_mode_flag_renders_text_launcher():
    result = run_cli('--text-ui')
    assert 'ROS2-Agent 终端交互入口' in result.stdout
    assert '基础命令' in result.stdout
    assert 'ROS2 巡检' in result.stdout


def test_cli_smoke_mode_runs_and_exits():
    result = run_cli('--smoke-ui')
    assert 'ROS2-Agent TUI smoke test ok' in result.stdout


def test_cli_command_surface_supports_core_subcommands():
    result = run_cli('--no-ui', 'help')
    assert 'collect env' in result.stdout
    assert 'diagnose fusion' in result.stdout
    assert 'runbook list' in result.stdout
    assert 'profile verify' in result.stdout
    assert 'logs deployment' in result.stdout
    assert 'doctor' in result.stdout
    assert 'history' in result.stdout
    assert 'settings' in result.stdout


def test_cli_status_command_returns_json():
    result = run_cli('--no-ui', 'status')
    payload = json.loads(result.stdout)
    assert 'project_root' in payload
    assert 'deployment_root' in payload


def test_cli_diagnose_fusion_returns_prioritized_candidates_shape():
    result = run_cli('--no-ui', 'diagnose', 'fusion')
    payload = json.loads(result.stdout)
    assert 'prioritized_candidates' in payload
    assert 'recommended_next_probe' in payload
