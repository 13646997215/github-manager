from pathlib import Path
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
DEPLOY_PYTHON = Path('/home/hanhan/Desktop/.ros2-agent/venv/bin/python')


def run_deploy_cli(*args: str) -> subprocess.CompletedProcess:
    env = dict(**__import__('os').environ)
    env['PYTHONPATH'] = str(REPO_ROOT)
    return subprocess.run(
        [str(DEPLOY_PYTHON), '-m', 'tools.cli', *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
        env=env,
    )


def test_deployed_textual_smoke_ui_runs():
    result = run_deploy_cli('--smoke-ui')
    assert 'ROS2-Agent TUI smoke test ok' in result.stdout


def test_deployed_text_ui_fallback_still_available():
    result = run_deploy_cli('--text-ui')
    assert 'ROS2-Agent 终端交互入口' in result.stdout


def test_deployed_help_lists_command_surface():
    result = run_deploy_cli('--no-ui', 'help')
    assert 'collect env' in result.stdout
    assert 'quality' in result.stdout
    assert 'inspect workspace' in result.stdout
    assert 'suggest-fix tf' in result.stdout


def test_deployed_status_runs():
    result = run_deploy_cli('--no-ui', 'status')
    assert 'deployment_root' in result.stdout
