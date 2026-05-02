import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_SCRIPT = REPO_ROOT / 'tools' / 'cli.py'


def run_script_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CLI_SCRIPT), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_script_cli_smoke_ui_runs_without_pythonpath_env():
    result = run_script_cli('--smoke-ui')
    assert result.returncode == 0
    assert 'ROS2-Agent TUI smoke test ok' in result.stdout


def test_script_cli_history_runs_without_pythonpath_env():
    result = run_script_cli('--no-ui', 'history')
    assert result.returncode == 0
    assert '已读取最近命令历史。' in result.stdout


def test_script_cli_quality_contract_is_blocked_without_pythonpath_env():
    result = run_script_cli('--no-ui', 'quality')
    assert result.returncode == 2
    assert 'quality 命令需在 TUI 外部运行' in result.stdout


def test_script_cli_status_json_runs_without_pythonpath_env():
    result = run_script_cli('--no-ui', 'status')
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert 'project_root' in payload
    assert 'deployment_root' in payload
