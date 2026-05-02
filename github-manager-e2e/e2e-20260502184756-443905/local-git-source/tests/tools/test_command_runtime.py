from tools.command_runtime import execute_command, result_to_payload
from tools.command_models import CommandStatus


def test_command_runtime_help_success():
    result = execute_command(["help"])
    assert result.status == CommandStatus.SUCCESS
    assert result.summary
    assert result.raw_output


def test_command_runtime_stage_b_core_commands_success():
    assert execute_command(["doctor"]).status == CommandStatus.SUCCESS
    assert execute_command(["inspect"]).status == CommandStatus.SUCCESS
    assert execute_command(["workflow"]).status == CommandStatus.SUCCESS
    assert execute_command(["report"]).status == CommandStatus.SUCCESS
    assert execute_command(["settings"]).status == CommandStatus.SUCCESS
    assert execute_command(["inspect", "workspace"]).status == CommandStatus.SUCCESS
    assert execute_command(["doctor", "ros2"]).status == CommandStatus.SUCCESS


def test_command_runtime_quality_is_blocked():
    result = execute_command(["quality"])
    assert result.status == CommandStatus.BLOCKED
    assert result.exit_code == 2
    assert result.raw_output


def test_command_runtime_unknown_command_not_implemented():
    result = execute_command(["unknown"])
    assert result.status == CommandStatus.NOT_IMPLEMENTED
    assert result.exit_code == 1


def test_command_runtime_payload_is_serializable_shape():
    result = execute_command(["status"])
    payload = result_to_payload(result)
    assert payload["status"] == "success"
    assert payload["summary"]
