import json

from tools.registry import get_command_catalog, list_capabilities


def test_registry_lists_collectors_and_diagnosers():
    result = list_capabilities()
    assert "collectors" in result
    assert "diagnosers" in result
    assert "ros2_env_collect" in result["collectors"]
    assert "env_diagnoser" in result["diagnosers"]
    json.dumps(result)


def test_command_catalog_contains_ui_metadata():
    catalog = get_command_catalog()
    assert catalog
    first = catalog[0]
    assert 'title' in first
    assert 'description_zh' in first
    assert 'category' in first


def test_command_catalog_contains_tui_core_actions():
    ids = {item['id'] for item in get_command_catalog()}
    assert 'quick-env-collect' in ids
    assert 'quality-gate' in ids


def test_command_catalog_is_large_enough_for_full_surface():
    catalog = get_command_catalog()
    assert len(catalog) >= 18
