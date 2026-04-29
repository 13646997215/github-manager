#!/usr/bin/env bash
set -u

PROJECT_DIR="/home/hanhan/Desktop/github"
LOG_FILE="$HOME/.local/state/github-manager/desktop-launch.log"
mkdir -p "$(dirname "$LOG_FILE")"
printf '===== %s desktop launch =====\n' "$(date '+%F %T')" >> "$LOG_FILE"

cd "$PROJECT_DIR" || {
  rc=$?
  printf 'ERROR %s cd failed: %s exit=%s\n' "$(date '+%F %T')" "$PROJECT_DIR" "$rc" >> "$LOG_FILE"
  echo "GitHub Manager Pro 启动失败：无法进入项目目录 $PROJECT_DIR"
  echo "日志：$LOG_FILE"
  echo "按 Enter 退出..."
  read -r _ || true
  exit "$rc"
}

export TERM="${TERM:-xterm-256color}"
export COLORTERM="${COLORTERM:-truecolor}"
export GITHUB_MANAGER_DESKTOP=1
export FORCE_COLOR=1
# 桌面双击默认使用内置 Python curses TUI，真的支持鼠标滚轮；禁用 fzf 避免旧 fzf 的 --mouse 兼容问题。
export GITHUB_MANAGER_USE_FZF="${GITHUB_MANAGER_USE_FZF:-0}"
export GITHUB_MANAGER_FZF_HEIGHT="${GITHUB_MANAGER_FZF_HEIGHT:-24}"
export GITHUB_MANAGER_FILE_PICKER_HEIGHT="${GITHUB_MANAGER_FILE_PICKER_HEIGHT:-26}"
export GITHUB_MANAGER_LAUNCHER=desktop

printf '\033]0;GitHub Manager Pro\007' || true

run_menu() {
  "$PROJECT_DIR/github-manager.sh" menu
}

# 正常桌面双击：gnome-terminal 已经提供真实 TTY，直接运行最稳。
if [[ -t 0 && -t 1 ]]; then
  run_menu
  rc=$?
else
  # 测试/特殊启动：没有 TTY 时用 script 人造一个 PTY，避免 read/fzf 判断失效。
  if command -v script >/dev/null 2>&1; then
    script -qec "$PROJECT_DIR/github-manager.sh menu" /dev/null
    rc=$?
  else
    run_menu
    rc=$?
  fi
fi

if [[ "$rc" -ne 0 ]]; then
  printf 'ERROR %s exit=%s\n' "$(date '+%F %T')" "$rc" >> "$LOG_FILE"
  echo
  echo "GitHub Manager Pro 启动或运行异常，退出码：$rc"
  echo "日志：$LOG_FILE"
  echo "按 Enter 退出..."
  read -r _ || true
fi

exit "$rc"
