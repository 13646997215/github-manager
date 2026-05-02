from tools.command_registry import export_legacy_catalog, get_command_spec, list_command_specs


def test_command_registry_resolves_known_command():
    spec = get_command_spec(["collect", "env"])
    assert spec is not None
    assert spec.handler_name == "collect_env"
    assert spec.execution_mode == "lightweight"


def test_command_registry_contains_stage_b_core_commands():
    assert get_command_spec(["doctor"]) is not None
    assert get_command_spec(["history"]) is not None
    assert get_command_spec(["settings"]) is not None
    assert get_command_spec(["inspect", "workspace"]) is not None
    assert get_command_spec(["suggest-fix", "tf"]) is not None
    assert get_command_spec(["compare", "snapshots"]) is not None


def test_command_registry_exports_legacy_catalog():
    catalog = export_legacy_catalog()
    assert catalog
    first = catalog[0]
    assert "title" in first
    assert "command" in first
    assert "execution_mode" in first


def test_command_specs_surface_is_large_enough():
    specs = list_command_specs()
    assert len(specs) >= 20
