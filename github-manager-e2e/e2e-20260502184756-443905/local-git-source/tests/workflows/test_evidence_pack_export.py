import json
from pathlib import Path

from scripts.validation.export_evidence_pack import export_evidence_pack


def test_evidence_pack_export(tmp_path: Path):
    output_path = tmp_path / "evidence.json"
    result = export_evidence_pack(str(output_path), {"case": "demo", "status": "ok"})
    assert Path(result).exists()
    payload = json.loads(Path(result).read_text(encoding="utf-8"))
    assert payload["case"] == "demo"
