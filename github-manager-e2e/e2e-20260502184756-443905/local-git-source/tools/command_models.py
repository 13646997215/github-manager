"""Unified command models for Hermes-aligned ROS2-Agent runtime."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class CommandStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    BLOCKED = "blocked"
    NOT_IMPLEMENTED = "not_implemented"


@dataclass
class NextAction:
    kind: str
    label: str
    command: List[str] = field(default_factory=list)
    detail: Optional[str] = None


@dataclass
class CommandSpec:
    id: str
    command: List[str]
    title: str
    description_zh: str
    category: str
    maturity: str
    risk_level: str
    entry_type: str
    detail: str
    handler_name: str
    execution_mode: str = "lightweight"
    interactive_policy: str = "allowed_in_tui"
    next_action_templates: List[NextAction] = field(default_factory=list)


@dataclass
class CommandResult:
    status: CommandStatus
    summary: str
    payload: Any = None
    highlights: List[str] = field(default_factory=list)
    next_actions: List[NextAction] = field(default_factory=list)
    raw_output: Optional[str] = None
    risk_level: str = "read_only"
    exit_code: int = 0
    command: List[str] = field(default_factory=list)
    command_id: Optional[str] = None
    execution_mode: str = "lightweight"
    maturity: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def status_to_exit_code(status: CommandStatus) -> int:
    if status is CommandStatus.SUCCESS:
        return 0
    if status is CommandStatus.BLOCKED:
        return 2
    return 1
