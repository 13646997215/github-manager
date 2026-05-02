import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INSTALL_SCRIPT = REPO_ROOT / 'profile' / 'ros2-agent' / 'bootstrap' / 'install_profile.sh'
POST_INSTALL_SCRIPT = REPO_ROOT / 'profile' / 'ros2-agent' / 'bootstrap' / 'post_install_validate.sh'


def test_post_install_validate_passes_for_fresh_install(tmp_path: Path):
    target = tmp_path / 'installed-profile'
    subprocess.run(['bash', str(INSTALL_SCRIPT), str(target)], check=True)
    subprocess.run(['bash', str(POST_INSTALL_SCRIPT), str(target)], check=True)
