"""Benchmark scoring helpers for ROS2-Agent Phase-2.

This module provides lightweight, transparent scoring utilities so benchmark
artifacts can evolve beyond markdown-only descriptions.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Tuple


@dataclass
class ScoreBreakdown:
    passed: bool
    score: float
    max_score: float
    matched: List[str]
    missing: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def score_required_strings(text: str, required: List[str], max_score: float = 1.0) -> Dict[str, Any]:
    matched = [item for item in required if item in text]
    missing = [item for item in required if item not in text]
    score = max_score if not required else max_score * (len(matched) / len(required))
    result = ScoreBreakdown(
        passed=len(missing) == 0,
        score=round(score, 4),
        max_score=max_score,
        matched=matched,
        missing=missing,
    )
    return result.to_dict()


def score_key_value_presence(result: Dict[str, Any], required_keys: List[str], max_score: float = 1.0) -> Dict[str, Any]:
    matched = [key for key in required_keys if key in result]
    missing = [key for key in required_keys if key not in result]
    score = max_score if not required_keys else max_score * (len(matched) / len(required_keys))
    breakdown = ScoreBreakdown(
        passed=len(missing) == 0,
        score=round(score, 4),
        max_score=max_score,
        matched=matched,
        missing=missing,
    )
    return breakdown.to_dict()


def score_expected_value(result: Dict[str, Any], key: str, expected: Any, max_score: float = 1.0) -> Dict[str, Any]:
    matched = []
    missing = []
    if result.get(key) == expected:
        matched.append(f"{key}={expected}")
        score = max_score
        passed = True
    else:
        missing.append(f"{key}={expected}")
        score = 0.0
        passed = False
    return ScoreBreakdown(
        passed=passed,
        score=round(score, 4),
        max_score=max_score,
        matched=matched,
        missing=missing,
    ).to_dict()


def score_next_actions(actions: List[str], required_actions: List[str], max_score: float = 1.0) -> Dict[str, Any]:
    matched = [item for item in required_actions if item in actions]
    missing = [item for item in required_actions if item not in actions]
    score = max_score if not required_actions else max_score * (len(matched) / len(required_actions))
    return ScoreBreakdown(
        passed=len(missing) == 0,
        score=round(score, 4),
        max_score=max_score,
        matched=matched,
        missing=missing,
    ).to_dict()


def score_list_subset(items: List[str], required_items: List[str], max_score: float = 1.0) -> Dict[str, Any]:
    matched = [item for item in required_items if item in items]
    missing = [item for item in required_items if item not in items]
    score = max_score if not required_items else max_score * (len(matched) / len(required_items))
    return ScoreBreakdown(
        passed=len(missing) == 0,
        score=round(score, 4),
        max_score=max_score,
        matched=matched,
        missing=missing,
    ).to_dict()


def score_weighted_sections(sections: List[Tuple[str, float, bool]]) -> Dict[str, Any]:
    total_weight = sum(weight for _, weight, _ in sections)
    achieved = sum(weight for _, weight, passed in sections if passed)
    score = 0.0 if total_weight == 0 else achieved / total_weight
    matched = [name for name, _, passed in sections if passed]
    missing = [name for name, _, passed in sections if not passed]
    return ScoreBreakdown(
        passed=len(missing) == 0,
        score=round(score, 4),
        max_score=1.0,
        matched=matched,
        missing=missing,
    ).to_dict()
