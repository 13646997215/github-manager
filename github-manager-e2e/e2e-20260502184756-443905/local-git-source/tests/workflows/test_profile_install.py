from pathlib import Path
import subprocess

REPO_ROOT = Path(__file__).resolve().parents[2]
INSTALL_SCRIPT = REPO_ROOT / 'profile' / 'ros2-agent' / 'bootstrap' / 'install_profile.sh'


def test_install_profile_creates_expected_files(tmp_path: Path):
    target = tmp_path / 'installed-profile'
    subprocess.run(['bash', str(INSTALL_SCRIPT), str(target)], check=True)
    assert (target / 'SOUL.md').exists()
    assert (target / 'AGENTS.md').exists()
    assert (target / 'config.yaml').exists()
    assert (target / '.env.template').exists()
    assert (target / 'INSTALL_MANIFEST.md').exists()
    manifest = (target / 'INSTALL_MANIFEST.md').read_text(encoding='utf-8')
    assert 'Repository-backed assets to use together with this profile' in manifest
