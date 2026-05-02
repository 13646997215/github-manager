import json

from tools.command_models import CommandResult, CommandStatus, NextAction, status_to_exit_code


def test_status_to_exit_code_mapping():
    assert status_to_exit_code(CommandStatus.SUCCESS) == 0
    assert status_to_exit_code(CommandStatus.BLOCKED) == 2
    assert status_to_exit_code(CommandStatus.ERROR) == 1
    assert status_to_exit_code(CommandStatus.NOT_IMPLEMENTED) == 1


def test_command_result_to_dict_is_json_serializable():
    result = CommandResult(
        status=CommandStatus.SUCCESS,
        summary="ok",
        next_actions=[NextAction(kind="command", label="next", command=["help"])],
    )
    payload = result.to_dict()
    assert payload["summary"] == "ok"
    json.dumps(payload)
