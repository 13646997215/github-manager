from pathlib import Path


def test_launcher_docs_exist():
    assert Path('docs/03_workflows/launcher-ui-workflow.md').exists()
    assert Path('assets/branding/ros2-agent-logo-lightblue.txt').exists()
    content = Path('docs/03_workflows/launcher-ui-workflow.md').read_text(encoding='utf-8')
    assert 'summary / next_actions / payload / raw' in content
