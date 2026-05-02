from pathlib import Path


def test_console_script_registered_in_pyproject():
    text = Path('pyproject.toml').read_text(encoding='utf-8')
    assert 'ros2-agent = "tools.cli:main"' in text
