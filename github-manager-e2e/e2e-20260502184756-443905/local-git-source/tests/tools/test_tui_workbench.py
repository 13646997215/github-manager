import importlib.util

import pytest

TEXTUAL_SPEC = importlib.util.find_spec('textual')
TEXTUAL_INSTALLED = TEXTUAL_SPEC is not None
if TEXTUAL_INSTALLED:
    from tools.cli import Ros2AgentTUI
else:
    Ros2AgentTUI = None

pytestmark = pytest.mark.skipif(not TEXTUAL_INSTALLED, reason='textual not installed')


@pytest.mark.asyncio
async def test_tui_output_mode_cycles_and_updates_status():
    app = Ros2AgentTUI(smoke_test=False)
    async with app.run_test() as pilot:
        await pilot.pause()
        before = app.output_mode
        await pilot.press('tab')
        await pilot.pause()
        assert app.output_mode != before
        assert app.output_mode in {'summary', 'next_actions', 'payload', 'raw'}


@pytest.mark.asyncio
async def test_tui_enter_executes_and_stores_result_payload():
    app = Ros2AgentTUI(smoke_test=False)
    async with app.run_test() as pilot:
        app.selected_index = 0
        app._refresh_views()
        await pilot.press('enter')
        await pilot.pause()
        assert app.last_result_payload is not None
        assert 'summary' in app.last_result_payload


@pytest.mark.asyncio
async def test_tui_search_filters_catalog_and_recent_panels_work():
    app = Ros2AgentTUI(smoke_test=False)
    async with app.run_test() as pilot:
        await pilot.pause()
        await pilot.press('/')
        await pilot.pause()
        search = app.query_one('#search-box')
        search.value = 'doctor'
        await pilot.pause()
        assert app.search_query == 'doctor'
        assert app.filtered_catalog
        assert all('doctor' in ' '.join(item.command) or 'doctor' in item.title.lower() for item in app.filtered_catalog)

        await pilot.press('r')
        await pilot.pause()
        assert app.last_result_payload is not None
        assert app.last_result_payload['summary'] == '已显示最近历史。'

        await pilot.press('e')
        await pilot.pause()
        assert app.last_result_payload['summary'] == '已显示最近错误。'
