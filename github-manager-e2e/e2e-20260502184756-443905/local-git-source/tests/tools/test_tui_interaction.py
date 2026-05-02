import subprocess
import sys
from pathlib import Path

import importlib.util
import pytest

TEXTUAL_SPEC = importlib.util.find_spec('textual')
TEXTUAL_INSTALLED = TEXTUAL_SPEC is not None
if TEXTUAL_INSTALLED:
    from tools.cli import Ros2AgentTUI
else:
    Ros2AgentTUI = None

pytestmark = pytest.mark.skipif(not TEXTUAL_INSTALLED, reason='textual not installed')

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.asyncio
async def test_tui_enter_executes_selected_command(monkeypatch):
    called = {}

    def fake_execute(command_parts):
        called['command'] = list(command_parts)
        return 0

    monkeypatch.setattr('tools.cli.execute_catalog_command', fake_execute)
    app = Ros2AgentTUI(smoke_test=False)

    async with app.run_test() as pilot:
        app.selected_index = 0
        app._refresh_views()
        await pilot.press('enter')
        await pilot.pause()

    assert called['command'] == app.catalog[0].command


@pytest.mark.asyncio
async def test_tui_click_only_selects_item(monkeypatch):
    called = {}

    def fake_execute(command_parts):
        called['command'] = list(command_parts)
        return 0

    monkeypatch.setattr('tools.cli.execute_catalog_command', fake_execute)
    app = Ros2AgentTUI(smoke_test=False)

    async with app.run_test() as pilot:
        second_widget = app.menu_widgets[1] if app.menu_widgets else None
        await pilot.pause()
        if second_widget is None:
            second_widget = app.menu_widgets[1]
        await pilot.click('.launcher-item:nth-of-type(2)')
        await pilot.pause()

    assert app.selected_index == 1
    assert 'command' not in called


@pytest.mark.asyncio
async def test_tui_mouse_scroll_does_not_change_selected_index():
    app = Ros2AgentTUI(smoke_test=False)

    async with app.run_test() as pilot:
        app.selected_index = 0
        app._refresh_views()
        before = app.selected_index
        if app.menu_scroll is not None:
            app.menu_scroll.scroll_down(animate=False)
        await pilot.pause()
        assert app.selected_index == before
