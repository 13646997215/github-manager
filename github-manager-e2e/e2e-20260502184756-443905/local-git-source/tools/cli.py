"""Unified CLI and TUI launcher helpers for ROS2-Agent platform surface."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.command_registry import list_capabilities
from tools.command_renderers import result_to_text
from tools.command_runtime import execute_command, result_to_payload
from tools.registry import get_command_catalog

try:
    from textual.app import App, ComposeResult
    from textual.binding import Binding
    from textual.containers import Container, Horizontal, Vertical, VerticalScroll
    from textual.reactive import reactive
    from textual.widgets import Footer, Header, Input, Static

    TEXTUAL_AVAILABLE = True
except Exception:
    TEXTUAL_AVAILABLE = False

LOGO = r"""
   ____   ___  ____ ___         _                    _
  |  _ \ / _ \/ ___|_ _|  __ _| |__   ___ _ __   __| |
  | |_) | | | \___ \| |  / _` | '_ \ / _ \ '_ \ / _` |
  |  _ <| |_| |___) | | | (_| | | | |  __/ | | | (_| |
  |_| \_\\___/|____/___| \__, |_| |_|\___|_| |_|\__,_|
                         |___/
"""

GUIDE_TEXT = "↑/↓ 选择，Enter 执行，鼠标滚轮仅滚动窗口，鼠标左键点击仅选中，H 查看帮助，Q 退出"
CATEGORY_ORDER = ["基础命令", "ROS2 采集", "ROS2 巡检", "ROS2 诊断", "Workflow 与 Benchmark"]
ACCENT_HEX = "#8ecbff"
STATUS_HEX = "#6fd3ff"
HELP_TEXT = "帮助：鼠标左键点击只会选中命令，不会执行；鼠标滚轮只负责滚动窗口；真正执行命令需要按 Enter。"
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE_DIR = REPO_ROOT / ".artifacts" / "demo-profile"
DEPLOYMENT_ROOT = Path("/home/hanhan/Desktop/.ros2-agent")
DEPLOYMENT_LOG = REPO_ROOT / "docs" / "planning" / "EXECUTION_LOG_TUI_DEPLOYMENT.md"
TUI_DEBUG_LOG = REPO_ROOT / "docs" / "planning" / "TUI_RUNTIME_DEBUG_LOG.md"
RUNBOOK_DIR = REPO_ROOT / "docs" / "03_runbooks"
BROKEN_WORKFLOW_DIR = REPO_ROOT / "examples" / "broken_workflows"


@dataclass
class CatalogItem:
    id: str
    title: str
    description_zh: str
    category: str
    maturity: str
    risk_level: str
    entry_type: str
    command: List[str]
    detail: str
    execution_mode: str = "lightweight"
    interactive_policy: str = "allowed_in_tui"
    next_actions: List[List[str]] | None = None


class CommandNotImplementedError(RuntimeError):
    pass


class CommandExecutionError(RuntimeError):
    pass


def _catalog_items() -> List[CatalogItem]:
    return [CatalogItem(**item) for item in get_command_catalog()]


def render_capability_listing() -> str:
    return json.dumps(list_capabilities(), ensure_ascii=False)


def render_menu_json() -> str:
    return json.dumps(get_command_catalog(), ensure_ascii=False, indent=2)


def render_command_help() -> str:
    lines = ["ROS2-Agent 专属完整命令面", ""]
    grouped: Dict[str, List[CatalogItem]] = {}
    for item in _catalog_items():
        grouped.setdefault(item.category, []).append(item)

    for category in CATEGORY_ORDER:
        if category not in grouped:
            continue
        lines.append(f"[{category}]")
        for item in grouped[category]:
            command = " ".join(item.command)
            lines.append(f"- {command}")
            lines.append(f"  {item.title} | {item.description_zh}")
        lines.append("")
    lines.append("内置别名：help, status, quality")
    return "\n".join(lines).strip()


def render_launcher_text(selected_index: int = 0) -> str:
    catalog = _catalog_items()
    lines: List[str] = []
    lines.append(LOGO)
    lines.append("ROS2-Agent 终端交互入口（高级 TUI 不可用时的文本回退模式）")
    lines.append(f"中文向导：{GUIDE_TEXT}")
    lines.append("")

    grouped: Dict[str, List[CatalogItem]] = {}
    for item in catalog:
        grouped.setdefault(item.category, []).append(item)

    flat_index = 0
    for category in CATEGORY_ORDER:
        if category not in grouped:
            continue
        lines.append(f"[{category}]")
        for item in grouped[category]:
            marker = ">" if flat_index == selected_index else " "
            lines.append(f" {marker} {item.title} | {item.description_zh} | {item.risk_level} | {item.maturity}")
            flat_index += 1
        lines.append("")
    lines.append("提示：部署完成后若环境可用，直接运行 `ros2-agent` 将优先进入高级 TUI。")
    return "\n".join(lines)


def _print_json(payload: object) -> int:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def run_catalog_command_capture(command_parts: Sequence[str]) -> tuple[int, str]:
    result = execute_command(command_parts)
    return result.exit_code, result_to_text(result)


def append_tui_debug_log(event: str, details: Dict[str, object]) -> None:
    TUI_DEBUG_LOG.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().isoformat(timespec='seconds')
    lines = [f"\n## {timestamp} | {event}"]
    for key, value in details.items():
        lines.append(f"- {key}: {value}")
    with TUI_DEBUG_LOG.open('a', encoding='utf-8') as handle:
        handle.write("\n".join(lines) + "\n")


def execute_catalog_command(command_parts: Sequence[str]) -> int:
    result = execute_command(command_parts)
    json_commands = {
        ('status',),
        ('capabilities',),
        ('diagnose', 'fusion'),
    }
    if tuple(result.command) in json_commands:
        output = json.dumps(result.payload, ensure_ascii=False, indent=2)
    else:
        output = result_to_text(result)
    if output:
        print(output)
    return result.exit_code


def _render_command_output(command_parts: Sequence[str]) -> str:
    result = execute_command(command_parts)
    json_commands = {
        ('status',),
        ('capabilities',),
        ('diagnose', 'fusion'),
    }
    if tuple(result.command) in json_commands:
        return json.dumps(result.payload, ensure_ascii=False, indent=2)
    return result_to_text(result)

if TEXTUAL_AVAILABLE:
    class LauncherItemView(Static):
        def __init__(self, item: CatalogItem, index: int, selected: bool = False) -> None:
            self.item = item
            self.index = index
            self.selected = selected
            super().__init__(self._render_text(), classes='launcher-item')

        def _render_text(self) -> str:
            marker = '▶' if self.selected else '  '
            return f"{marker} {self.item.title}\n   {self.item.description_zh}\n   风险: {self.item.risk_level} | 成熟度: {self.item.maturity}"

        def set_selected(self, selected: bool) -> None:
            self.selected = selected
            self.update(self._render_text())

        def on_click(self) -> None:
            self.app.select_from_index(self.index)


    class Ros2AgentTUI(App[int]):
        CSS = f"""
        Screen {{
            background: #07111d;
            color: #dff3ff;
        }}
        #root {{
            layout: vertical;
        }}
        #banner {{
            color: {ACCENT_HEX};
            padding: 1 2;
            border: round {ACCENT_HEX};
            background: #0b1828;
        }}
        #guide {{
            color: #d7ecff;
            padding: 0 2 1 2;
        }}
        #body {{
            height: 1fr;
        }}
        #menu-pane {{
            width: 2fr;
            border: round #6caee0;
            padding: 1;
            background: #0b1624;
            scrollbar-size: 1 1;
            scrollbar-color: {ACCENT_HEX};
        }}
        #detail-pane {{
            width: 1fr;
            border: round #6caee0;
            padding: 1;
            background: #0d1929;
        }}
        .category-label {{
            color: {ACCENT_HEX};
            text-style: bold;
            padding-top: 1;
        }}
        .launcher-item {{
            padding: 0 0 1 0;
        }}
        .launcher-item.-selected {{
            background: #16314d;
            border-left: wide {ACCENT_HEX};
        }}
        #status {{
            color: {STATUS_HEX};
            padding: 1 2;
            border-top: solid #6caee0;
            background: #08131f;
        }}
        """

        BINDINGS = [
            Binding('q', 'quit', '退出'),
            Binding('up', 'move_up', '上移'),
            Binding('down', 'move_down', '下移'),
            Binding('enter', 'run_selected', '执行'),
            Binding('h', 'show_help', '帮助'),
            Binding('tab', 'cycle_output_mode', '切换输出视图'),
            Binding('/', 'focus_search', '搜索'),
            Binding('e', 'show_recent_errors', '最近错误'),
            Binding('r', 'show_recent_history', '最近历史'),
        ]

        selected_index = reactive(0)

        def __init__(self, smoke_test: bool = False) -> None:
            super().__init__()
            self.catalog = _catalog_items()
            self.filtered_catalog: List[CatalogItem] = list(self.catalog)
            self.menu_widgets: List[LauncherItemView] = []
            self.menu_scroll: VerticalScroll | None = None
            self.smoke_test = smoke_test
            self.output_mode = 'summary'
            self.last_result_payload: Dict[str, object] | None = None
            self.search_query = ''

        def compose(self) -> ComposeResult:
            yield Header(show_clock=True)
            with Vertical(id='root'):
                yield Static(LOGO + '\nROS2-Agent 高级 TUI 旗舰版', id='banner')
                yield Static(f'中文向导：{GUIDE_TEXT}', id='guide')
                yield Input(placeholder='输入 / 后搜索命令标题、分类、描述或子命令', id='search-box')
                with Horizontal(id='body'):
                    with VerticalScroll(id='menu-pane') as menu_scroll:
                        self.menu_scroll = menu_scroll
                        current_category = None
                        for index, item in enumerate(self.filtered_catalog):
                            if item.category != current_category:
                                current_category = item.category
                                yield Static(f'[{current_category}]', classes='category-label')
                            widget = LauncherItemView(item=item, index=index, selected=index == self.selected_index)
                            self.menu_widgets.append(widget)
                            yield widget
                    with VerticalScroll(id='detail-pane'):
                        yield Static(self._detail_text(), id='detail-text')
                    with VerticalScroll(id='output-pane'):
                        yield Static('执行输出会显示在这里。', id='output-text')
                yield Static(self._status_text(), id='status')
            yield Footer()

        def on_mount(self) -> None:
            self._refresh_views()
            if self.smoke_test:
                self.call_later(self.exit, 0)

        def _detail_text(self) -> str:
            item = self.filtered_catalog[self.selected_index]
            command = 'ros2-agent --no-ui ' + ' '.join(item.command)
            return (
                f'命令：{item.title}\n\n'
                f'说明：{item.description_zh}\n\n'
                f'详情：{item.detail}\n\n'
                f'风险级别：{item.risk_level}\n'
                f'成熟度：{item.maturity}\n\n'
                f'执行方式：{command}'
            )

        def _filter_catalog(self, query: str) -> None:
            normalized = query.strip().lower()
            if not normalized:
                self.filtered_catalog = list(self.catalog)
            else:
                self.filtered_catalog = [
                    item for item in self.catalog
                    if normalized in item.title.lower()
                    or normalized in item.description_zh.lower()
                    or normalized in item.category.lower()
                    or normalized in ' '.join(item.command).lower()
                ]
            if not self.filtered_catalog:
                self.filtered_catalog = list(self.catalog)
            self.selected_index = min(self.selected_index, len(self.filtered_catalog) - 1) if self.filtered_catalog else 0

        def _history_entries(self, limit: int = 8) -> List[Dict[str, object]]:
            history_path = REPO_ROOT / 'docs' / 'planning' / 'COMMAND_HISTORY.jsonl'
            if not history_path.exists():
                return []
            lines = [line for line in history_path.read_text(encoding='utf-8').splitlines() if line.strip()]
            parsed: List[Dict[str, object]] = []
            for line in reversed(lines[-limit:]):
                try:
                    parsed.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
            return parsed

        def _recent_errors(self, limit: int = 8) -> List[Dict[str, object]]:
            return [entry for entry in self._history_entries(limit=40) if entry.get('status') in {'error', 'blocked', 'not_implemented'}][:limit]

        def _format_result_for_mode(self, payload: Dict[str, object] | None) -> str:
            if not payload:
                return '执行输出会显示在这里。'
            mode = self.output_mode
            if mode == 'summary':
                lines = [str(payload.get('summary', ''))]
                highlights = payload.get('highlights') or []
                if highlights:
                    lines.append('')
                    lines.append('highlights:')
                    lines.extend(f'- {item}' for item in highlights)
                return '\n'.join(lines).strip() or '无摘要'
            if mode == 'next_actions':
                actions = payload.get('next_actions') or []
                if not actions:
                    return '暂无下一步建议。'
                lines = ['next_actions:']
                for action in actions:
                    command = ' '.join(action.get('command', [])) if isinstance(action, dict) else ''
                    detail = action.get('detail') if isinstance(action, dict) else ''
                    suffix = f' ({command})' if command else ''
                    extra = f' - {detail}' if detail else ''
                    label = action.get('label', 'next') if isinstance(action, dict) else 'next'
                    lines.append(f'- {label}{suffix}{extra}')
                return '\n'.join(lines)
            if mode == 'raw':
                raw_output = payload.get('raw_output')
                if raw_output:
                    return str(raw_output)
                return json.dumps(payload.get('payload'), ensure_ascii=False, indent=2) if payload.get('payload') is not None else '无原始输出'
            return json.dumps(payload.get('payload'), ensure_ascii=False, indent=2) if payload.get('payload') is not None else '无 payload 数据'

        def _render_output_panel(self) -> str:
            mode_title = {
                'summary': '结果摘要视图',
                'next_actions': '下一步建议视图',
                'payload': '结构化结果视图',
                'raw': '原始输出视图',
            }.get(self.output_mode, '输出视图')
            body = self._format_result_for_mode(self.last_result_payload)
            return f'{mode_title}\n\n{body}'

        def _status_text(self) -> str:
            item = self.filtered_catalog[self.selected_index]
            return f"当前选择：{item.title} | 搜索：{self.search_query or '(无)'} | 输出视图：{self.output_mode} | / 搜索 | R 历史 | E 错误 | Enter 执行 | Tab 切换结果视图 | H 帮助 | Q 退出"

        def _refresh_views(self) -> None:
            search_box = self.query_one('#search-box', Input)
            if search_box.value != self.search_query:
                search_box.value = self.search_query
            for idx, widget in enumerate(self.menu_widgets):
                widget.set_selected(idx == self.selected_index)
                if idx == self.selected_index:
                    widget.add_class('-selected')
                else:
                    widget.remove_class('-selected')
            self.query_one('#detail-text', Static).update(self._detail_text())
            self.query_one('#output-text', Static).update(self._render_output_panel())
            self.query_one('#status', Static).update(self._status_text())

        def _step_selection(self, delta: int) -> None:
            if not self.filtered_catalog:
                return
            self.selected_index = (self.selected_index + delta) % len(self.filtered_catalog)
            self._refresh_views()
            if self.menu_scroll is not None and self.menu_widgets:
                self.call_after_refresh(lambda: self.menu_scroll.scroll_to_widget(self.menu_widgets[self.selected_index], animate=False, center=True))

        def select_from_index(self, index: int) -> None:
            self.selected_index = index
            append_tui_debug_log('select_from_index', {
                'selected_index': index,
                'command': ' '.join(self.filtered_catalog[index].command),
            })
            self._refresh_views()

        def action_move_up(self) -> None:
            self._step_selection(-1)

        def action_move_down(self) -> None:
            self._step_selection(1)

        def action_show_help(self) -> None:
            self.query_one('#status', Static).update(HELP_TEXT + ' | Tab 可在摘要/建议/payload/原始输出之间切换')

        def action_cycle_output_mode(self) -> None:
            modes = ['summary', 'next_actions', 'payload', 'raw']
            current = modes.index(self.output_mode) if self.output_mode in modes else 0
            self.output_mode = modes[(current + 1) % len(modes)]
            self._refresh_views()

        def action_focus_search(self) -> None:
            self.query_one('#search-box', Input).focus()

        def action_show_recent_history(self) -> None:
            entries = self._history_entries()
            lines = ['最近历史:']
            if not entries:
                lines.append('- 暂无历史')
            else:
                for entry in entries:
                    command = ' '.join(entry.get('command', []))
                    lines.append(f"- {entry.get('status')} | {command} | {entry.get('summary')}")
            self.last_result_payload = {
                'summary': '已显示最近历史。',
                'highlights': [f'recent_entries: {len(entries)}'],
                'next_actions': [],
                'payload': {'entries': entries},
                'raw_output': '\n'.join(lines),
            }
            self.output_mode = 'raw'
            self._refresh_views()

        def action_show_recent_errors(self) -> None:
            entries = self._recent_errors()
            lines = ['最近错误/阻塞:']
            if not entries:
                lines.append('- 暂无最近错误')
            else:
                for entry in entries:
                    command = ' '.join(entry.get('command', []))
                    lines.append(f"- {entry.get('status')} | {command} | {entry.get('summary')}")
            self.last_result_payload = {
                'summary': '已显示最近错误。',
                'highlights': [f'recent_errors: {len(entries)}'],
                'next_actions': [],
                'payload': {'entries': entries},
                'raw_output': '\n'.join(lines),
            }
            self.output_mode = 'raw'
            self._refresh_views()

        def on_input_changed(self, event: Input.Changed) -> None:
            if event.input.id != 'search-box':
                return
            self.search_query = event.value
            self._filter_catalog(self.search_query)
            self.refresh(recompose=True)

        def action_run_selected(self) -> None:
            item = self.filtered_catalog[self.selected_index]
            append_tui_debug_log('action_run_selected_enter', {
                'selected_index': self.selected_index,
                'title': item.title,
                'command': ' '.join(item.command),
            })
            long_hint = '（重量级命令，建议在 TUI 外执行）' if item.execution_mode == 'heavyweight' else '（轻量命令）'
            self.query_one('#status', Static).update(f"正在执行：{item.title} {long_hint}")
            self.call_after_refresh(self._execute_selected_after_refresh)

        def _execute_selected_after_refresh(self) -> None:
            item = self.filtered_catalog[self.selected_index]
            append_tui_debug_log('action_run_selected_execute', {
                'selected_index': self.selected_index,
                'title': item.title,
                'command': ' '.join(item.command),
            })
            result = execute_command(item.command)
            self.last_result_payload = result_to_payload(result)
            if result.execution_mode == 'heavyweight' or result.exit_code != 0:
                highlights = list(self.last_result_payload.get('highlights', [])) if self.last_result_payload else []
                highlights.extend([
                    f'exit_code: {result.exit_code}',
                    f'execution_mode: {result.execution_mode}',
                ])
                if self.last_result_payload is not None:
                    self.last_result_payload['highlights'] = highlights
            self.query_one('#output-text', Static).update(self._render_output_panel())
            self.query_one('#status', Static).update(
                f"执行完成：{item.title} | exit_code={result.exit_code} | mode={result.execution_mode} | 结果已显示在右侧输出面板"
            )
            append_tui_debug_log('action_run_selected_exit', {
                'selected_index': self.selected_index,
                'title': item.title,
                'command': ' '.join(item.command),
                'exit_code': result.exit_code,
                'output_preview': (self.last_result_payload.get('summary', '') if self.last_result_payload else '')[:240],
            })


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog='ros2-agent', add_help=True)
    parser.add_argument('--dump-menu-json', action='store_true')
    parser.add_argument('--no-ui', action='store_true')
    parser.add_argument('--text-ui', action='store_true')
    parser.add_argument('--smoke-ui', action='store_true')
    parser.add_argument('command', nargs='*')
    args = parser.parse_args(argv)

    if args.dump_menu_json:
        print(render_menu_json())
        return 0

    if args.no_ui:
        return execute_catalog_command(args.command)

    if args.text_ui:
        print(render_launcher_text())
        return 0

    if args.smoke_ui:
        if TEXTUAL_AVAILABLE:
            app = Ros2AgentTUI(smoke_test=True)
            app.run()
            print('ROS2-Agent TUI smoke test ok')
            return 0
        print('ROS2-Agent TUI smoke test ok (text fallback)')
        return 0

    if not args.command:
        if TEXTUAL_AVAILABLE:
            app = Ros2AgentTUI()
            return int(app.run() or 0)
        print(render_launcher_text())
        return 0

    return execute_catalog_command(args.command)


if __name__ == '__main__':
    raise SystemExit(main())
