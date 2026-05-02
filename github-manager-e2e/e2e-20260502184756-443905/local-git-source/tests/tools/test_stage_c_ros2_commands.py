from tools.command_runtime import execute_command


def test_stage_c_inspect_commands_have_user_facing_output():
    for command in (["inspect", "workspace"], ["inspect", "graph"], ["inspect", "tf"], ["inspect", "controller"]):
        result = execute_command(command)
        assert result.status.value == "success"
        assert result.summary
        assert result.highlights
        assert result.next_actions


def test_stage_c_doctor_commands_have_user_facing_output():
    for command in (["doctor", "ros2"], ["doctor", "workspace"], ["doctor", "tf"], ["doctor", "control"]):
        result = execute_command(command)
        assert result.status.value == "success"
        assert result.summary
        assert result.highlights


def test_stage_c_suggest_fix_and_trace_commands_have_next_actions():
    for command in (["suggest-fix", "runtime"], ["suggest-fix", "tf"], ["suggest-fix", "controller"], ["trace", "failure"]):
        result = execute_command(command)
        assert result.status.value == "success"
        assert result.next_actions


def test_stage_c_replay_and_compare_commands_work():
    for command in (["replay", "evidence"], ["replay", "workflow"], ["compare", "snapshots"]):
        result = execute_command(command)
        assert result.status.value == "success"
        assert result.summary
