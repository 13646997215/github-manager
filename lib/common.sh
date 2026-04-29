#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/env.sh"

log() {
  local level="$1"; shift
  local message="$*"
  printf '%s [%s] %s\n' "$(date '+%F %T')" "$level" "$message" >> "$LOG_FILE"
}

audit_log() {
  local action="$1"; shift || true
  local detail="$*"
  printf '%s\t%s\t%s\n' "$(date '+%F %T')" "$action" "$detail" >> "$AUDIT_LOG_FILE"
}

json_log_escape() {
  python3 - <<'PY' "$1"
import json, sys
print(json.dumps(sys.argv[1], ensure_ascii=False))
PY
}

current_ts_iso() {
  date -Iseconds
}

log_operation_start() {
  local action="$1"; shift || true
  local op_id="${action,,}-$(date +%s)-$$-${RANDOM}"
  local start_epoch
  start_epoch="$(date +%s%3N 2>/dev/null || python3 - <<'PY'
import time
print(int(time.time() * 1000))
PY
)"
  export GHM_OP_ID="$op_id"
  export GHM_OP_ACTION="$action"
  export GHM_OP_START_MS="$start_epoch"
  log_operation_event start "$action" "$@"
  printf '%s\n' "$op_id"
}

log_operation_event() {
  local phase="$1"
  local action="$2"
  shift 2 || true
  local payload="${1:-}"
  local op_id="${GHM_OP_ID:-}"
  local ts_iso
  ts_iso="$(current_ts_iso)"
  printf '{"ts":"%s","phase":%s,"action":%s,"op_id":%s,%s}\n' \
    "$ts_iso" \
    "$(json_log_escape "$phase")" \
    "$(json_log_escape "$action")" \
    "$(json_log_escape "$op_id")" \
    "$payload" >> "$AUDIT_LOG_FILE"
}

log_operation_end() {
  local result="$1"
  shift || true
  local payload="${1:-}"
  local end_ms duration
  end_ms="$(date +%s%3N 2>/dev/null || python3 - <<'PY'
import time
print(int(time.time() * 1000))
PY
)"
  if [[ -n "${GHM_OP_START_MS:-}" ]]; then
    duration=$((end_ms - GHM_OP_START_MS))
  else
    duration=0
  fi
  local merged_payload
  merged_payload="\"result\":$(json_log_escape "$result"),\"duration_ms\":$duration"
  if [[ -n "$payload" ]]; then
    merged_payload+=",$payload"
  fi
  log_operation_event end "${GHM_OP_ACTION:-unknown}" "$merged_payload"
  unset GHM_OP_ID GHM_OP_ACTION GHM_OP_START_MS
}

build_audit_payload() {
  local first=1 piece out=""
  while (($#)); do
    local key="$1"
    local value="${2-}"
    shift 2 || true
    if [[ $first -eq 0 ]]; then
      out+="," 
    fi
    out+="\"$key\":"
    if [[ "$value" =~ ^-?[0-9]+$ ]]; then
      out+="$value"
    elif [[ "$value" == "true" || "$value" == "false" || "$value" == "null" ]]; then
      out+="$value"
    else
      out+="$(json_log_escape "$value")"
    fi
    first=0
  done
  printf '%s' "$out"
}

print_color() {
  local color="$1"; shift
  printf "%b%s%b\n" "$color" "$*" "$NC"
}

_status_icon() {
  local kind="$1"
  if [[ "${ASCII_UI:-false}" == "true" ]]; then
    case "$kind" in info) printf '[i]' ;; success) printf '[OK]' ;; warn) printf '[!]' ;; error) printf '[ERR]' ;; esac
  else
    case "$kind" in info) printf 'ℹ️ ' ;; success) printf '✅' ;; warn) printf '⚠️ ' ;; error) printf '❌' ;; esac
  fi
}
info() { print_color "$CYAN" "$(_status_icon info) $*" >&2; log INFO "$*"; }
success() { print_color "$GREEN" "$(_status_icon success) $*" >&2; log INFO "$*"; }
warn() { print_color "$YELLOW" "$(_status_icon warn) $*" >&2; log WARN "$*"; }
error() { print_color "$RED" "$(_status_icon error) $*" >&2; log ERROR "$*"; }

die() {
  error "$*"
  audit_log ERROR "$*"
  exit 1
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

require_command() {
  local cmd="$1"
  command_exists "$cmd" || die "缺少依赖：$cmd"
}

safe_mkdir() {
  mkdir -p "$1"
}

trim() {
  local value="$1"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

join_by() {
  local delimiter="$1"; shift || true
  local first=1
  for item in "$@"; do
    if [[ $first -eq 1 ]]; then
      printf '%s' "$item"
      first=0
    else
      printf '%s%s' "$delimiter" "$item"
    fi
  done
}

confirm() {
  local prompt="${1:-确认继续？}"
  local default="${2:-Y}"
  local answer
  if [[ "${GITHUB_MANAGER_USE_TUI:-1}" != "0" && -x "$PROJECT_ROOT/bin/ghm-tui.py" && -r /dev/tty && -w /dev/tty ]]; then
    local tui_out
    tui_out="$(mktemp "$TMP_ROOT/tui-confirm.XXXXXX")"
    if GHM_TUI_OUTPUT_FILE="$tui_out" "$PROJECT_ROOT/bin/ghm-tui.py" confirm "$prompt" "$default" < /dev/tty > /dev/tty; then
      answer="$(cat "$tui_out")"
      rm -f "$tui_out"
      [[ "$answer" == "yes" ]]
      return $?
    fi
    rm -f "$tui_out"
  fi
  if [[ "$default" == "Y" ]]; then
    read -r -p "$prompt [Y/n] " answer < /dev/tty || true
    answer="${answer:-Y}"
  else
    read -r -p "$prompt [y/N] " answer < /dev/tty || true
    answer="${answer:-N}"
  fi
  [[ "$answer" =~ ^[Yy]$ ]]
}

with_temp_dir() {
  local prefix="${1:-job}"
  mktemp -d "$TMP_ROOT/${prefix}.XXXXXX"
}

cleanup_dir() {
  local dir="$1"
  [[ -n "$dir" && -d "$dir" ]] && rm -rf "$dir"
}

json_escape() {
  jq -Rn --arg value "$1" '$value'
}

ensure_file_permissions() {
  local path="$1"
  local mode="$2"
  [[ -e "$path" ]] && chmod "$mode" "$path"
}

bytes_to_human() {
  local bytes="${1:-0}"
  python3 - <<'PY' "$bytes"
import sys
size = int(sys.argv[1])
units = ['B', 'KB', 'MB', 'GB', 'TB']
idx = 0
while size >= 1024 and idx < len(units) - 1:
    size /= 1024.0
    idx += 1
print(f"{size:.1f} {units[idx]}")
PY
}

calc_sha1() {
  local file="$1"
  sha1sum "$file" | awk '{print $1}'
}

base64_file() {
  local file="$1"
  base64 -w 0 "$file"
}

progress() {
  local message="$1"
  local output="→ $message"
  if [[ -n "${GITHUB_MANAGER_QUIET:-}" ]]; then
    log INFO "$message"
    return 0
  fi
  print_color "$BLUE" "$output"
  log INFO "$message"
}

print_banner() {
  local cols
  cols="$(tput cols 2>/dev/null || printf '100')"
  if [[ -n "${GITHUB_MANAGER_UI_HEADER_ACTIVE:-}" ]]; then
    return 0
  fi
  if [[ "$cols" =~ ^[0-9]+$ ]] && (( cols < 78 )); then
    cat <<EOF
+-- GitHub Manager Pro -------------------------+
|  清爽终端工作台                     |
|  v$APP_VERSION                                |
+-----------------------------------------------+
EOF
  else
    cat <<'EOF'
   ______ _ _   _    _       _       __  ___
  / ____/(_) | | |  | |     | |     /  |/  /
 / / __ / /| |_| |  | | ___ | |__  / /|_/ /___ _____  ____ _____ ____  _____
/ /_/ // / | __| |  | |/ _ \| '_ \/ /  / / __ `/ __ \/ __ `/ __ `/ _ \/ ___/
\____//_/  \__|_|  |_|\___/|_.__/_/  /_/ /_/ / / / / /_/ / /_/ /  __/ /
                                           \__,_/_/ /_/\__,_/\__, /\___/_/
                                                            /____/
EOF
    cat <<EOF
  ── 专业终端工作台 · v$APP_VERSION · Desktop Ready ──
EOF
  fi
}

ensure_first_run_setup() {
  if [[ ! -f "$FIRST_RUN_MARKER" ]]; then
    cat <<EOF
欢迎第一次使用 $APP_NAME

快速上手：
  1. 认证：确认已完成 gh auth login。
  2. 上传：主菜单 1 -> 多级文件选择器 -> 选仓库 -> 确认上传。
  3. 文件选择器：数字进入目录，s数字选择目录/文件，u返回上级，d完成。
  4. 同步：先用 dry-run 预览报告，再执行真实同步。
  5. 帮助：每个 bin/ghm-* 都支持 --help。
EOF
    printf '%s\n' "$(date '+%F %T')" > "$FIRST_RUN_MARKER"
    audit_log FIRST_RUN "首次启动向导已展示"
  fi
}

show_about() {
  cat <<EOF
$APP_NAME
版本: $APP_VERSION
定位: 舒适、规矩、可桌面双击使用的 GitHub 文件/仓库终端工作台

界面设计：
  - Claude Code 风格 ASCII 标题
  - 自适应终端宽度，小窗口自动使用紧凑标题
  - 主菜单内置操作指南，减少误操作
  - 多级文件选择器支持进入/返回/手动路径/多选

核心能力：
  - 快速上传、浏览、下载、删除、更新
  - push/pull 双向同步、冲突检测、报告导出
  - 仓库 create/info/clone/rename/transfer/delete
  - 桌面快捷方式、审计日志、release 打包

文档:
  - $PROJECT_ROOT/docs/README.md
  - $PROJECT_ROOT/docs/API.md

桌面双击说明：
  - 桌面启动默认启用内置 Python curses 精美 TUI，先显示完整功能选择。
  - 支持固定高度窗口、方向键、鼠标点击、鼠标滚轮滑动；异常终端可执行：GITHUB_MANAGER_USE_TUI=0 GITHUB_MANAGER_USE_FZF=0 ./github-manager.sh menu
EOF
}

show_audit_log() {
  if [[ ! -f "$AUDIT_LOG_FILE" ]]; then
    warn "还没有审计记录"
    return 0
  fi
  tail -n 40 "$AUDIT_LOG_FILE"
}

create_release_bundle() {
  mkdir -p "$RELEASE_DIR"
  cp -f "$PROJECT_ROOT/github-manager.sh" "$RELEASE_DIR/"
  cp -f "$PROJECT_ROOT/github-upload.sh" "$RELEASE_DIR/"
  if [[ -f "$PROJECT_ROOT/GitHubManager.desktop" ]]; then
    cp -f "$PROJECT_ROOT/GitHubManager.desktop" "$RELEASE_DIR/"
  elif [[ -f "$HOME/Desktop/GitHubManager.desktop" ]]; then
    cp -f "$HOME/Desktop/GitHubManager.desktop" "$RELEASE_DIR/"
  fi
  cp -rf "$PROJECT_ROOT/bin" "$PROJECT_ROOT/lib" "$PROJECT_ROOT/docs" "$PROJECT_ROOT/config" "$PROJECT_ROOT/assets" "$RELEASE_DIR/"
  success "已生成发布目录：$RELEASE_DIR"
  audit_log RELEASE "生成发布目录 $RELEASE_DIR"
}
