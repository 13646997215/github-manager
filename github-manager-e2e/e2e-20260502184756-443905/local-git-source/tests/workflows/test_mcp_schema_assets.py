from pathlib import Path


def test_mcp_schema_assets_exist():
    assert Path('mcp/README.md').exists()
    assert Path('mcp/contracts/collector_contract.md').exists()
    assert Path('mcp/contracts/diagnosis_contract.md').exists()
    assert Path('mcp/schemas/runtime_evidence.schema.json').exists()
    assert Path('mcp/schemas/diagnosis_report.schema.json').exists()
