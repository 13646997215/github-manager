"""Export structured evidence packs for workflow and recovery cases."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict



def export_evidence_pack(output_path: str, payload: Dict[str, Any]) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return str(path)


if __name__ == "__main__":
    sample = {
        "kind": "evidence_pack",
        "status": "demo",
        "note": "replace with collector/diagnoser outputs in real runs",
    }
    output = export_evidence_pack("benchmarks/reports/evidence/demo_evidence_pack.json", sample)
    print(output)
