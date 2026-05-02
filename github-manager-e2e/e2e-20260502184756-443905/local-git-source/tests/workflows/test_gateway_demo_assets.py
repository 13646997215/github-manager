from pathlib import Path
import subprocess

REPO_ROOT = Path(__file__).resolve().parents[2]
DEMO_SCRIPT = REPO_ROOT / 'scripts' / 'validation' / 'run_gateway_demo_pipeline.sh'


def test_gateway_demo_assets_exist():
    assert Path('docs/03_workflows/gateway-cron-demo-workflow.md').exists()
    assert DEMO_SCRIPT.exists()
