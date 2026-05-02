"""Diagnosis schema for phase-2 evidence-driven diagnosers."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class RiskLevel(str, Enum):
    READ_ONLY = "read_only"
    LOW_RISK_LOCAL = "low_risk_local"
    NEEDS_CONFIRMATION = "needs_confirmation"


@dataclass
class DiagnosisFinding:
    summary: str
    severity: str
    evidence_refs: List[str] = field(default_factory=list)
    uncertainty_gaps: List[str] = field(default_factory=list)


@dataclass
class CandidateCause:
    cause: str
    confidence: str
    evidence_refs: List[str] = field(default_factory=list)
    blocking_factors: List[str] = field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.READ_ONLY


@dataclass
class ProbeRecommendation:
    action: str
    reason: str
    risk_level: RiskLevel = RiskLevel.READ_ONLY


@dataclass
class RecoveryHint:
    action: str
    rationale: str
    risk_level: RiskLevel = RiskLevel.NEEDS_CONFIRMATION


@dataclass
class DiagnosisReport:
    domain: str
    findings: List[DiagnosisFinding] = field(default_factory=list)
    candidate_causes: List[CandidateCause] = field(default_factory=list)
    recommended_next_probe: Optional[ProbeRecommendation] = None
    recovery_hints: List[RecoveryHint] = field(default_factory=list)



def snapshot_to_dict(snapshot: Any) -> Dict[str, Any]:
    result = asdict(snapshot)
    return result
