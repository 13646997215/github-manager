from pathlib import Path


def test_capability_contract_refs_exist():
    assert Path("docs/01_architecture/capability_contract.md").exists()
    assert Path("profile/ros2-agent/CAPABILITIES.md").exists()
    content = Path("profile/ros2-agent/CAPABILITIES.md").read_text(encoding="utf-8")
    assert "统一 command runtime" in content
    assert "collect / diagnose / inspect / doctor / suggest-fix / trace / replay / compare" in content
