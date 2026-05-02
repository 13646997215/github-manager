from pathlib import Path
import subprocess

REPO_ROOT = Path(__file__).resolve().parents[2]
INIT_SCRIPT = REPO_ROOT / 'profile' / 'ros2-agent' / 'bootstrap' / 'init_workspace.sh'


def test_init_workspace_creates_expected_layout(tmp_path: Path):
    target = tmp_path / 'demo_ws'
    subprocess.run(['bash', str(INIT_SCRIPT), str(target)], check=True)
    assert (target / 'src').is_dir()
    assert (target / 'README.md').exists()
    assert (target / '.gitignore').exists()
