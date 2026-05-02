import json
from pathlib import Path

from tools.command_runtime import execute_command


HISTORY_LOG = Path('docs/planning/COMMAND_HISTORY.jsonl')


def test_doctor_command_returns_health_payload():
    result = execute_command(["doctor"])
    assert result.status.value == "success"
    payload = result.payload
    assert "deployment_entry_exists" in payload
    assert "workflow_docs" in payload


def test_history_command_returns_recent_entries():
    execute_command(["status"])
    result = execute_command(["history"])
    assert result.status.value == "success"
    assert "entries" in result.payload
    assert isinstance(result.payload["entries"], list)


def test_settings_command_returns_read_only_policy():
    result = execute_command(["settings"])
    payload = result.payload
    assert payload["tui_policy"]["enter"] == "execute"
    assert payload["tui_policy"]["left_click"] == "select_only"


def test_history_log_is_jsonl_when_created():
    execute_command(["status"])
    assert HISTORY_LOG.exists()
    line = HISTORY_LOG.read_text(encoding='utf-8').splitlines()[-1]
    json.loads(line)
