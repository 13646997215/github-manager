#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GitHub Manager Pro 精美鼠标 TUI 选择器。

模式：
  menu                         输出菜单编号
  choose <title> [items_file]  选择列表，输出选中项
  confirm <prompt> <Y|N>       确认弹窗，输出 yes/no
  files <start_dir>            输出选择的绝对路径，每行一个
"""
import curses
import os
import sys
from pathlib import Path

ACCENT = 6
SUCCESS = 2
WARN = 3
MUTED = 8

MENU_ITEMS = [
    ("1", "上传文件", "选择本地文件/目录并上传"),
    ("2", "浏览仓库", "查看远程仓库文件"),
    ("3", "下载文件", "下载远程文件或目录"),
    ("4", "删除文件", "删除远程文件或目录"),
    ("5", "更新文件", "用本地文件覆盖远程文件"),
    ("6", "同步文件夹", "push/pull 双向同步并生成报告"),
    ("7", "仓库管理", "创建/查看/克隆/重命名/转移/删除仓库"),
    ("8", "账号/设置", "查看路径、切换登录账号、PAT 设置"),
    ("9", "关于", "产品说明"),
    ("10", "审计日志", "查看最近关键操作"),
    ("11", "生成发布包", "构建 release 目录"),
    ("12", "退出", "关闭程序"),
]

EXCLUDES = {'.git', 'release', 'reports', 'hermes.log'}


def init_colors():
    if not curses.has_colors():
        return
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(ACCENT, curses.COLOR_CYAN, -1)
    curses.init_pair(SUCCESS, curses.COLOR_GREEN, -1)
    curses.init_pair(WARN, curses.COLOR_YELLOW, -1)
    curses.init_pair(MUTED, curses.COLOR_BLUE, -1)


def cp(pair, bold=False):
    attr = curses.color_pair(pair) if curses.has_colors() else 0
    return attr | (curses.A_BOLD if bold else 0)


def safe_add(stdscr, y, x, text, attr=0):
    h, w = stdscr.getmaxyx()
    if y < 0 or y >= h or x >= w:
        return
    try:
        stdscr.addnstr(y, x, text, max(0, w - x - 1), attr)
    except curses.error:
        pass


def draw_frame(stdscr, title, subtitle):
    h, w = stdscr.getmaxyx()
    stdscr.erase()
    try:
        stdscr.border()
    except curses.error:
        pass
    logo = [
        "   ____ _ _   _   _       _       __  __                                   ",
        "  / ___(_) |_| | | |_   _| |__   |  \/  | __ _ _ __   __ _  __ _  ___ _ __ ",
        " | |  _| | __| |_| | | | | '_ \\  | |\/| |/ _` | '_ \\ / _` |/ _` |/ _ \\ '__|",
        " | |_| | | |_|  _  | |_| | |_) | | |  | | (_| | | | | (_| | (_| |  __/ |   ",
        "  \\____|_|\\__|_| |_|\\__,_|_.__/  |_|  |_|\\__,_|_| |_|\\__,_|\\__, |\\___|_|   ",
        "                                                              |___/        ",
    ]
    if h >= 24 and w >= 92:
        for i, line in enumerate(logo, start=1):
            safe_add(stdscr, i, 3, line, cp(ACCENT, True))
        base_y = 7
    else:
        safe_add(stdscr, 1, 3, " GitHub Manager Pro ", cp(ACCENT, True))
        base_y = 2
    safe_add(stdscr, base_y, 3, "精美中文终端工作台", cp(MUTED))
    safe_add(stdscr, base_y + 1, 3, f"当前位置：{title}", cp(SUCCESS, True))
    safe_add(stdscr, base_y + 2, 3, subtitle, cp(MUTED))
    if w > 4:
        safe_add(stdscr, base_y + 3, 2, "─" * (w - 4), cp(MUTED))
    return base_y + 5


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def visible_window(selected, total, height, offset):
    if selected < offset:
        offset = selected
    if selected >= offset + height:
        offset = selected - height + 1
    return clamp(offset, 0, max(0, total - height))


def mouse_event_to_delta():
    try:
        _id, x, y, z, bstate = curses.getmouse()
    except curses.error:
        return None
    if hasattr(curses, 'BUTTON4_PRESSED') and bstate & curses.BUTTON4_PRESSED:
        return ('scroll', -1, x, y)
    if hasattr(curses, 'BUTTON5_PRESSED') and bstate & curses.BUTTON5_PRESSED:
        return ('scroll', 1, x, y)
    # Some terminals encode wheel in high bits; keep a best-effort fallback.
    if bstate & 0x10000:
        return ('scroll', -1, x, y)
    if bstate & 0x200000:
        return ('scroll', 1, x, y)
    if bstate & curses.BUTTON1_CLICKED or bstate & curses.BUTTON1_PRESSED:
        return ('click', 0, x, y)
    return None


def setup_curses(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.timeout(200)
    # 开启鼠标与滚轮事件。1003/1006 可让 GNOME Terminal 发送更完整的鼠标移动/滚轮序列。
    print('\033[?1000h\033[?1002h\033[?1003h\033[?1006h', end='', flush=True)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    init_colors()


def teardown_mouse():
    print('\033[?1006l\033[?1003l\033[?1002l\033[?1000l', end='', flush=True)


def menu_ui(stdscr):
    setup_curses(stdscr)
    selected = 0
    offset = 0
    try:
        while True:
            h, w = stdscr.getmaxyx()
            list_top = draw_frame(stdscr, "功能选择", "↑↓ 或鼠标滚轮滑动 · 鼠标点击高亮 · Enter 确认 · q 退出")
            list_h = max(8, min(18, h - list_top - 4))
            offset = visible_window(selected, len(MENU_ITEMS), list_h, offset)
            for row in range(list_h):
                idx = offset + row
                if idx >= len(MENU_ITEMS):
                    break
                num, label, desc = MENU_ITEMS[idx]
                y = list_top + row
                marker = "▶" if idx == selected else " "
                attr = cp(ACCENT, True) if idx == selected else 0
                safe_add(stdscr, y, 4, f"{marker} {int(num):02d}  {label:<10}  {desc}", attr)
            safe_add(stdscr, h - 3, 4, "所有功能入口都在这里；支持数字快捷键 1-12，不会再开局直接进入文件选择。", cp(WARN))
            stdscr.refresh()
            ch = stdscr.getch()
            if ch in (ord('q'), ord('Q'), 27):
                return "12"
            if ord('1') <= ch <= ord('9'):
                return str(ch - ord('0'))
            if ch == ord('0'):
                return "10"
            if ch in (ord('x'), ord('X')):
                return "11"
            if ch in (ord('e'), ord('E')):
                return "12"
            if ch in (curses.KEY_UP, ord('k')):
                selected = clamp(selected - 1, 0, len(MENU_ITEMS) - 1)
            elif ch in (curses.KEY_DOWN, ord('j')):
                selected = clamp(selected + 1, 0, len(MENU_ITEMS) - 1)
            elif ch in (curses.KEY_NPAGE,):
                selected = clamp(selected + list_h, 0, len(MENU_ITEMS) - 1)
            elif ch in (curses.KEY_PPAGE,):
                selected = clamp(selected - list_h, 0, len(MENU_ITEMS) - 1)
            elif ch in (10, 13, curses.KEY_ENTER):
                return MENU_ITEMS[selected][0]
            elif ch == curses.KEY_MOUSE:
                ev = mouse_event_to_delta()
                if not ev:
                    continue
                kind, delta, x, y = ev
                if kind == 'scroll':
                    selected = clamp(selected + delta, 0, len(MENU_ITEMS) - 1)
                elif kind == 'click' and list_top <= y < list_top + list_h:
                    idx = offset + (y - list_top)
                    if 0 <= idx < len(MENU_ITEMS):
                        selected = idx
                        return MENU_ITEMS[selected][0]
    finally:
        teardown_mouse()


def choose_ui(stdscr, title, items):
    setup_curses(stdscr)
    selected = 0
    offset = 0
    try:
        while True:
            h, w = stdscr.getmaxyx()
            list_top = draw_frame(stdscr, title, "↑↓ 或鼠标滚轮滑动 · 鼠标点击高亮 · Enter 确认 · q 取消")
            list_h = max(8, h - list_top - 4)
            offset = visible_window(selected, len(items), list_h, offset)
            for row in range(list_h):
                idx = offset + row
                if idx >= len(items):
                    break
                marker = "▶" if idx == selected else " "
                attr = cp(ACCENT, True) if idx == selected else 0
                safe_add(stdscr, list_top + row, 4, f"{marker} {idx+1:02d}  {items[idx]}", attr)
            stdscr.refresh()
            ch = stdscr.getch()
            if ch in (ord('q'), ord('Q'), 27):
                raise SystemExit(2)
            if ch in (curses.KEY_UP, ord('k')):
                selected = clamp(selected - 1, 0, len(items) - 1)
            elif ch in (curses.KEY_DOWN, ord('j')):
                selected = clamp(selected + 1, 0, len(items) - 1)
            elif ch in (curses.KEY_NPAGE,):
                selected = clamp(selected + list_h, 0, len(items) - 1)
            elif ch in (curses.KEY_PPAGE,):
                selected = clamp(selected - list_h, 0, len(items) - 1)
            elif ch in (10, 13, curses.KEY_ENTER):
                return items[selected]
            elif ch == curses.KEY_MOUSE:
                ev = mouse_event_to_delta()
                if ev:
                    kind, delta, x, y = ev
                    if kind == 'scroll':
                        selected = clamp(selected + delta, 0, len(items) - 1)
                    elif kind == 'click' and list_top <= y < list_top + list_h:
                        idx = offset + (y - list_top)
                        if 0 <= idx < len(items):
                            selected = idx
    finally:
        teardown_mouse()


def confirm_ui(stdscr, prompt, default):
    setup_curses(stdscr)
    selected = 0 if default.upper() == 'Y' else 1
    opts = [('yes', '确认继续'), ('no', '取消返回')]
    try:
        while True:
            list_top = draw_frame(stdscr, "确认操作", "←→/↑↓/鼠标滚轮切换 · Enter确认 · y/n 快捷键")
            safe_add(stdscr, list_top, 4, prompt, cp(WARN, True))
            for i, (_, label) in enumerate(opts):
                marker = "▶" if i == selected else " "
                attr = cp(ACCENT, True) if i == selected else 0
                safe_add(stdscr, list_top + 2 + i, 6, f"{marker} {label}", attr)
            stdscr.refresh()
            ch = stdscr.getch()
            if ch in (ord('y'), ord('Y')):
                return 'yes'
            if ch in (ord('n'), ord('N'), ord('q'), ord('Q'), 27):
                return 'no'
            if ch in (curses.KEY_UP, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_RIGHT, ord('j'), ord('k')):
                selected = 1 - selected
            elif ch in (10, 13, curses.KEY_ENTER):
                return opts[selected][0]
            elif ch == curses.KEY_MOUSE:
                ev = mouse_event_to_delta()
                if ev:
                    kind, delta, x, y = ev
                    if kind == 'scroll':
                        selected = 1 - selected
                    elif kind == 'click' and list_top + 2 <= y <= list_top + 3:
                        selected = y - (list_top + 2)
                        return opts[selected][0]
    finally:
        teardown_mouse()


def list_entries(cur):
    try:
        entries = []
        for p in Path(cur).iterdir():
            if p.name in EXCLUDES:
                continue
            entries.append(p)
        entries.sort(key=lambda p: (not p.is_dir(), p.name.lower()))
        return entries
    except Exception:
        return []


def preview_lines(path, max_lines):
    p = Path(path)
    lines = []
    try:
        if p.is_dir():
            lines.append(f"目录: {p}")
            lines.append("")
            for i, child in enumerate(list_entries(p)):
                if i >= max_lines - 3:
                    lines.append("...")
                    break
                kind = "目录" if child.is_dir() else "文件"
                lines.append(f"{kind:>2}  {child.name}")
        elif p.is_file():
            size = p.stat().st_size
            lines.append(f"文件: {p.name}")
            lines.append(f"大小: {size} B")
            lines.append("")
            with p.open('r', encoding='utf-8', errors='replace') as f:
                for _, line in zip(range(max_lines - 4), f):
                    lines.append(line.rstrip('\n'))
        else:
            lines.append(str(p))
    except Exception as e:
        lines.append(f"无法预览: {e}")
    return lines


def file_ui(stdscr, start_dir):
    setup_curses(stdscr)
    base = Path(start_dir).expanduser().resolve()
    cur = base
    selected_idx = 0
    offset = 0
    chosen = set()
    try:
        while True:
            entries = list_entries(cur)
            if selected_idx >= len(entries):
                selected_idx = max(0, len(entries) - 1)
            h, w = stdscr.getmaxyx()
            list_top = draw_frame(stdscr, "本地文件选择", "↑↓/鼠标滚轮滑动 · 点击高亮 · Enter进入目录/勾选文件 · Space勾选 · d完成 · u上级 · h回家")
            list_top += 2
            list_h = max(8, h - list_top - 5)
            left_w = max(42, int(w * 0.52))
            offset = visible_window(selected_idx, len(entries), list_h, offset)
            safe_add(stdscr, list_top - 2, 3, f"当前目录: {cur}", cp(SUCCESS, True))
            safe_add(stdscr, list_top - 1, 3, f"已选择: {len(chosen)} 项", cp(WARN))
            # vertical divider
            for y in range(list_top, h - 3):
                safe_add(stdscr, y, left_w, "│", cp(MUTED))
            for row in range(list_h):
                idx = offset + row
                if idx >= len(entries):
                    break
                p = entries[idx]
                mark = "●" if str(p) in chosen else " "
                kind = "目录" if p.is_dir() else "文件"
                marker = "▶" if idx == selected_idx else " "
                attr = cp(ACCENT, True) if idx == selected_idx else 0
                name = p.name + ("/" if p.is_dir() else "")
                safe_add(stdscr, list_top + row, 3, f"{marker} {mark} {idx+1:03d} {kind:<2} {name}", attr)
            if entries:
                p = entries[selected_idx]
                for i, line in enumerate(preview_lines(p, list_h)):
                    safe_add(stdscr, list_top + i, left_w + 2, line, cp(MUTED) if i > 1 else cp(SUCCESS, True))
            else:
                safe_add(stdscr, list_top, 3, "空目录或无权限读取", cp(WARN))
            safe_add(stdscr, h - 3, 3, "快捷键: Space勾选当前项 | Enter目录=进入/文件=勾选 | a勾选目录本身 | d完成 | q取消", cp(MUTED))
            stdscr.refresh()
            ch = stdscr.getch()
            if ch in (ord('q'), ord('Q'), 27):
                raise SystemExit(2)
            if ch in (curses.KEY_UP, ord('k')):
                selected_idx = clamp(selected_idx - 1, 0, max(0, len(entries) - 1))
            elif ch in (curses.KEY_DOWN, ord('j')):
                selected_idx = clamp(selected_idx + 1, 0, max(0, len(entries) - 1))
            elif ch == curses.KEY_NPAGE:
                selected_idx = clamp(selected_idx + list_h, 0, max(0, len(entries) - 1))
            elif ch == curses.KEY_PPAGE:
                selected_idx = clamp(selected_idx - list_h, 0, max(0, len(entries) - 1))
            elif ch in (ord('u'), ord('U')):
                if cur != base and cur != cur.parent:
                    cur = cur.parent; selected_idx = 0; offset = 0
            elif ch in (ord('h'), ord('H')):
                cur = base; selected_idx = 0; offset = 0
            elif ch in (ord('d'), ord('D')):
                if chosen:
                    return "\n".join(sorted(chosen))
            elif ch in (ord(' '), ord('a'), ord('A')) and entries:
                p = str(entries[selected_idx])
                if p in chosen: chosen.remove(p)
                else: chosen.add(p)
            elif ch in (10, 13, curses.KEY_ENTER) and entries:
                p = entries[selected_idx]
                if p.is_dir():
                    cur = p.resolve(); selected_idx = 0; offset = 0
                else:
                    sp = str(p)
                    if sp in chosen: chosen.remove(sp)
                    else: chosen.add(sp)
            elif ch == curses.KEY_MOUSE:
                ev = mouse_event_to_delta()
                if ev:
                    kind, delta, x, y = ev
                    if kind == 'scroll':
                        selected_idx = clamp(selected_idx + delta, 0, max(0, len(entries) - 1))
                    elif kind == 'click' and list_top <= y < list_top + list_h and x < left_w:
                        idx = offset + (y - list_top)
                        if 0 <= idx < len(entries): selected_idx = idx
    finally:
        teardown_mouse()


def main():
    if len(sys.argv) < 2:
        print("usage: ghm-tui.py <menu|choose|files>", file=sys.stderr)
        return 2
    mode = sys.argv[1]
    try:
        if mode == 'menu':
            out = curses.wrapper(menu_ui)
        elif mode == 'choose':
            title = sys.argv[2] if len(sys.argv) > 2 else '选择'
            if len(sys.argv) > 3 and sys.argv[3] != '-':
                items = Path(sys.argv[3]).read_text(encoding='utf-8', errors='replace').splitlines()
            else:
                items = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
            items = [item for item in items if item]
            if not items:
                return 2
            out = curses.wrapper(lambda stdscr: choose_ui(stdscr, title, items))
        elif mode == 'confirm':
            prompt = sys.argv[2] if len(sys.argv) > 2 else '确认继续？'
            default = sys.argv[3] if len(sys.argv) > 3 else 'Y'
            out = curses.wrapper(lambda stdscr: confirm_ui(stdscr, prompt, default))
        elif mode == 'files':
            start = sys.argv[2] if len(sys.argv) > 2 else str(Path.home())
            out = curses.wrapper(lambda stdscr: file_ui(stdscr, start))
        else:
            return 2
        if out:
            output_file = os.environ.get('GHM_TUI_OUTPUT_FILE')
            if output_file:
                Path(output_file).write_text(str(out) + "\n", encoding='utf-8')
            else:
                print(out)
        return 0
    finally:
        teardown_mouse()

if __name__ == '__main__':
    raise SystemExit(main())
