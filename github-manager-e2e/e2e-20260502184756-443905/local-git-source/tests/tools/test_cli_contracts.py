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
        check=False,
    )


def test_heavyweight_quality_contract_is_blocked_with_expected_exit_code():
    result = run_cli('--no-ui', 'quality')
    assert result.returncode == 2
    assert 'quality 命令需在 TUI 外部运行' in result.stdout


def test_history_contract_returns_recent_entries_summary():
    result = run_cli('--no-ui', 'history')
    assert result.returncode == 0
    assert '已读取最近命令历史。' in result.stdout
    assert 'recent_entries' in result.stdout


def test_smoke_ui_contract_succeeds_even_without_textual_runtime():
    result = run_cli('--smoke-ui')
    assert result.returncode == 0
    assert 'ROS2-Agent TUI smoke test ok' in result.stdout
