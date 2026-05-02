"""Compatibility facade for ROS2-Agent command registry."""

from __future__ import annotations

from typing import Dict, List

from tools.command_registry import export_legacy_catalog, list_capabilities as _list_capabilities


def list_capabilities() -> Dict[str, List[str]]:
    return _list_capabilities()


def get_command_catalog() -> List[Dict[str, object]]:
    return export_legacy_catalog()
