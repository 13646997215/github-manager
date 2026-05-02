import json

from tools.cli import render_capability_listing


def test_cli_renders_capability_listing_as_json_string():
    output = render_capability_listing()
    payload = json.loads(output)
    assert "collectors" in payload
    assert "diagnosers" in payload
