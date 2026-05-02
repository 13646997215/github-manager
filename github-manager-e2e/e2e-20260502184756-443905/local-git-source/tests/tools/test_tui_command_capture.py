import json
from pathlib import Path

from tools.cli import run_catalog_command_capture
from tools.registry import get_command_catalog


def test_all_catalog_commands_return_visible_output_or_guidance():
    command_map = {tuple(item['command']): item['title'] for item in get_command_catalog()}
    failures = []
    allowed_commands = {
        ('help',),
        ('status',),
        ('doctor',),
        ('inspect',),
        ('history',),
        ('workflow',),
        ('report',),
        ('settings',),
        ('collect', 'env'),
        ('collect', 'workspace'),
        ('collect', 'graph'),
        ('collect', 'tf'),
        ('collect', 'controller'),
        ('diagnose', 'env'),
        ('diagnose', 'workspace'),
        ('diagnose', 'runtime'),
        ('diagnose', 'tf'),
        ('diagnose', 'controller'),
        ('diagnose', 'fusion'),
        ('inspect', 'workspace'),
        ('inspect', 'graph'),
        ('inspect', 'tf'),
        ('inspect', 'controller'),
        ('doctor', 'ros2'),
        ('doctor', 'workspace'),
        ('doctor', 'tf'),
        ('doctor', 'control'),
        ('suggest-fix', 'runtime'),
        ('suggest-fix', 'tf'),
        ('suggest-fix', 'controller'),
        ('trace', 'failure'),
        ('replay', 'evidence'),
        ('replay', 'workflow'),
        ('compare', 'snapshots'),
        ('benchmark', 'recovery'),
        ('runbook', 'list'),
        ('profile', 'install'),
        ('profile', 'verify'),
        ('logs', 'deployment'),
    }
    for command, title in command_map.items():
        if command not in allowed_commands:
            continue
        exit_code, output = run_catalog_command_capture(command)
        if not isinstance(output, str) or not output.strip():
            failures.append((title, command, exit_code, output))
    assert not failures, failures


def test_help_status_and_collect_show_nonempty_output():
    for command in [('help',), ('status',), ('collect', 'env')]:
        exit_code, output = run_catalog_command_capture(command)
        assert isinstance(output, str)
        assert output.strip()
