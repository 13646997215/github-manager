#!/usr/bin/env bash
set -euo pipefail

# shellcheck disable=SC1091
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/repos.sh"

ui_tty() { [[ -r /dev/tty && -w /dev/tty ]]; }
is_interactive_tty() { ui_tty; }
ui_target() { ui_tty && printf '%s' /dev/tty || printf '%s' /dev/stdout; }
ui_out() { ui_tty && printf '%b' "$*" > /dev/tty || printf '%b' "$*"; }
ui_line() { ui_out "$*\n"; }
ui_read() {
  local p="$1" d="${2:-}" a
  if [[ -n "$d" ]]; then
    ui_out "${MUTED}${p}${NC} ${SURFACE}[${d}]${NC} "
  else
    ui_out "${MUTED}${p}${NC} "
  fi
  ui_tty && read -r a < /dev/tty || read -r a || a=""
  printf '%s\n' "${a:-$d}"
}
ui_pause() { local _; ui_out "\n${SURFACE}按 Enter 继续${NC}"; ui_tty && read -r _ < /dev/tty || read -r _ || true; }
ui_clear() { [[ -n "${GITHUB_MANAGER_NO_CLEAR:-}" ]] || ui_out '\033[2J\033[H'; }
ui_rule() { ui_line "${SURFACE}────────────────────────────────────────────────────────────────────────────────────────────────────────${NC}"; }
ui_micro_guide() { ui_line "${SURFACE}提示:${NC} ${MUTED}$1${NC}"; }

ui_header() {
  local section="${1:-主页}"
  ui_clear
  if [[ "${ASCII_UI:-false}" == "true" ]]; then
    cat > "$(ui_target)" <<EOF
${ACCENT}+------------------------------------------------------------------------------------------------------+${NC}
${ACCENT}| GitHub Manager Pro                                                                                  |${NC}
${ACCENT}+------------------------------------------------------------------------------------------------------+${NC}
${BOLD}${FG}  $section${NC}  ${MUTED}文件 / 仓库 / 同步 / 账号${NC}
${SURFACE}  操作:${NC} ${MUTED}↑↓/鼠标滚轮选择 · Enter确认 · Tab多选 · Esc/q取消${NC}
EOF
  else
    cat > "$(ui_target)" <<EOF
${ACCENT}  ______ _ _   _    _       _       __  ___                                  ${NC}
${ACCENT} / ____/(_) | | |  | |     | |     /  |/  /___ _____  ____ _____ ____  _____ ${NC}
${ACCENT}/ / __ / /| |_| |  | | ___ | |__  / /|_/ / __ \`/ __ \/ __ \`/ __ \`/ _ \/ ___/${NC}
${ACCENT}\ \_\ \/ / |  _  |  | |/ _ \| '_ \/ /  / / /_/ / / / / /_/ / /_/ /  __/ /    ${NC}
${ACCENT} \____/_/  |_| |_|  |_|\___/|_.__/_/  /_/\__,_/_/ /_/\__,_/\__, /\___/_/     ${NC}
${ACCENT}                                                            /____/           ${NC}
${SURFACE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}
${BOLD}${FG}  GitHub Manager Pro${NC}  ${MUTED}精美中文终端工作台 · 当前：${section}${NC}
${SURFACE}  操作:${NC} ${MUTED}↑↓/鼠标滚轮选择 · Enter确认 · Tab多选 · Esc/q取消${NC}
EOF
  fi
}
menu_header() { ui_header "$1"; ui_rule; }

tui_available() { [[ "${GITHUB_MANAGER_USE_TUI:-1}" != "0" ]] && command -v python3 >/dev/null 2>&1 && [[ -x "$PROJECT_ROOT/bin/ghm-tui.py" ]] && ui_tty; }
fzf_available() { command -v fzf >/dev/null 2>&1 && [[ "${GITHUB_MANAGER_USE_FZF:-1}" != "0" ]] && ui_tty; }
fzf_common_opts() {
  local opts=(
    --layout=reverse
    --border=rounded
    --height="${GITHUB_MANAGER_FZF_HEIGHT:-24}"
    --min-height=18
    --margin="${GITHUB_MANAGER_FZF_MARGIN:-1,2}"
    --padding="${GITHUB_MANAGER_FZF_PADDING:-1,2}"
    --cycle
    --ansi
    --info=inline
    --pointer='▶'
    --marker='●'
    --prompt='  选择 > '
    --bind='esc:abort,ctrl-c:abort'
  )
  printf '%s\n' "${opts[@]}"
}

choose_fzf() {
  local prompt="$1"; shift
  local items=("$@") selected
  fzf_available || return 1
  local opts=()
  mapfile -t opts < <(fzf_common_opts)
  selected="$(printf '%s\n' "${items[@]}" | fzf "${opts[@]}" --header=" $prompt · ↑↓/滚轮选择 · Enter确认 · Esc取消 " < /dev/tty)" || return 1
  [[ -n "$selected" ]] || return 1
  printf '%s\n' "$selected"
}

choose_from_list() {
  local prompt="$1" selected=""; shift; local items=("$@")
  [[ ${#items[@]} -gt 0 ]] || die "没有可选项：$prompt"
  is_interactive_tty || die "未选择：$prompt"
  if tui_available; then
    local tui_out items_file
    tui_out="$(mktemp "$TMP_ROOT/tui-choose.XXXXXX")"
    items_file="$(mktemp "$TMP_ROOT/tui-choose-items.XXXXXX")"
    printf '%s\n' "${items[@]}" > "$items_file"
    if GHM_TUI_OUTPUT_FILE="$tui_out" "$PROJECT_ROOT/bin/ghm-tui.py" choose "$prompt" "$items_file" < /dev/tty > /dev/tty; then
      selected="$(cat "$tui_out")"
      rm -f "$tui_out" "$items_file"
      printf '%s\n' "$selected"
      return 0
    fi
    rm -f "$tui_out" "$items_file"
  fi
  if selected="$(choose_fzf "$prompt" "${items[@]}")"; then
    printf '%s\n' "$selected"
    return 0
  fi
  while true; do
    menu_header "$prompt"
    local idx=1 item
    for item in "${items[@]}"; do printf '%b\n' "  ${ACCENT}$(printf '%02d' "$idx")${NC}  ${FG}${item}${NC}" > /dev/tty; idx=$((idx+1)); done
    local choice; choice="$(ui_read '请输入编号')"
    case "$choice" in q|Q) die "已取消：$prompt";; ''|*[!0-9]*) warn "请输入有效编号"; ui_pause;; *) if ((choice>=1 && choice<=${#items[@]})); then selected="${items[$((choice-1))]}"; break; else warn "编号超出范围"; ui_pause; fi;; esac
  done
  printf '%s\n' "$selected"
}

select_branch() { local repo="$1" d; d="$(get_repo_default_branch "$repo")"; d="${d:-$DEFAULT_BRANCH}"; ui_read "分支" "$d"; }
select_commit_message() { ui_read "提交说明" "${1:-$DEFAULT_COMMIT_MESSAGE}"; }
select_remote_path() { ui_read "远程目录（留空=仓库根目录）" "${1:-}"; }

choose_input_method() {
  local title="${1:-选择输入方式}"
  choose_from_list "$title" "选择器" "手动输入" "取消"
}

prompt_manual_or_browse_repo() {
  local method
  method="$(choose_input_method '选择仓库方式')"
  case "$method" in
    选择器) select_repo_interactive ;;
    手动输入)
      local repo
      repo="$(prompt_tty '请输入仓库名 owner/repo')"
      validate_repo_name_or_die "$repo"
      printf '%s\n' "$repo"
      ;;
    取消) die '已取消：选择仓库方式' ;;
  esac
}

select_remote_entries() {
  local repo="$1"
  local base_path="${2:-}"
  local branch="${3:-$DEFAULT_BRANCH}"
  list_remote_files "$repo" "$base_path" "$branch"
}

validate_repo_name_or_die() {
  local repo="$1"
  [[ "$repo" =~ ^[^/[:space:]]+/[^/[:space:]]+$ ]] || die "仓库名格式不正确，请输入 owner/repo，例如 13646997215/github-manager"
}

validate_local_path_or_die() {
  local path="$1"
  local mode="${2:-any}"
  [[ -n "$path" ]] || die "本地路径不能为空"
  [[ -e "$path" ]] || die "本地路径不存在：$path"
  if [[ "$mode" == "file" && ! -f "$path" ]]; then
    die "需要选择文件，但当前不是文件：$path"
  fi
  if [[ "$mode" == "dir" && ! -d "$path" ]]; then
    die "需要选择目录，但当前不是目录：$path"
  fi
}

validate_remote_path_or_die() {
  local repo="$1"
  local branch="$2"
  local path="$3"
  local allow_empty="${4:-false}"
  if [[ -z "$path" ]]; then
    [[ "$allow_empty" == "true" ]] && return 0
    die "远程路径不能为空"
  fi
  list_remote_files "$repo" "$path" "$branch" >/dev/null 2>&1 || die "远程路径不存在或无法访问：${path}"
}

select_remote_path_interactive() {
  local repo="$1"
  local branch="${2:-$DEFAULT_BRANCH}"
  local mode="${3:-any}"
  local allow_empty="${4:-false}"
  local current="$(normalize_remote_path "${5:-}")"
  while true; do
    ui_header "远程路径向导"
    ui_micro_guide "当前仓库: $repo  | 分支: ${branch:-$DEFAULT_BRANCH}  | 当前目录: ${current:-/}"
    ui_micro_guide "下载/删除可选文件或目录；更新只允许选文件；同步优先选目录。也可以切到手动输入。"
    ui_rule
    local action
    action="$(choose_from_list "远程路径选择" "浏览当前目录" "手动输入路径" "返回仓库根目录" "取消")"
    case "$action" in
      浏览当前目录)
        local entries raw type path size sha download_url items=() labels=()
        raw="$(select_remote_entries "$repo" "$current" "$branch" || true)"
        if [[ -z "$raw" ]]; then
          warn "当前远程目录为空：${current:-/}"
          if [[ "$allow_empty" == "true" ]]; then
            if confirm "目录为空，是否直接使用当前目录 ${current:-/} ?" Y; then
              printf '%s\n' "$current"
              return 0
            fi
          fi
          continue
        fi
        while IFS=$'\t' read -r type path size sha download_url; do
          [[ -n "$path" ]] || continue
          if [[ "$mode" == "file" && "$type" != "file" ]]; then
            continue
          fi
          items+=("$path")
          if [[ "$type" == "dir" ]]; then
            labels+=("DIR  $path")
          else
            labels+=("FILE $path")
          fi
        done <<< "$raw"
        if [[ ${#items[@]} -eq 0 ]]; then
          warn "当前目录下没有可用的${mode/file/文件}${mode/dir/目录}"
          continue
        fi
        if [[ "$allow_empty" == "true" ]]; then
          labels+=("[使用当前目录] ${current:-/}")
          items+=("__CURRENT_DIR__")
        fi
        local chosen label idx=0 selected_path=""
        chosen="$(choose_from_list '选择远程路径' "${labels[@]}")"
        for label in "${labels[@]}"; do
          if [[ "$label" == "$chosen" ]]; then
            selected_path="${items[$idx]}"
            break
          fi
          idx=$((idx + 1))
        done
        [[ -n "$selected_path" ]] || continue
        if [[ "$selected_path" == "__CURRENT_DIR__" ]]; then
          printf '%s\n' "$current"
          return 0
        fi
        if [[ "$chosen" == DIR* ]]; then
          if [[ "$mode" == "dir" || "$mode" == "any" ]]; then
            if confirm "使用目录 $selected_path ? 选否将继续进入该目录浏览。" N; then
              printf '%s\n' "$selected_path"
              return 0
            fi
          fi
          current="$selected_path"
          continue
        fi
        printf '%s\n' "$selected_path"
        return 0
        ;;
      手动输入路径)
        local manual
        manual="$(prompt_tty '请输入远程路径（留空为根目录）' "$current")"
        manual="$(normalize_remote_path "$manual")"
        if [[ -z "$manual" && "$allow_empty" != "true" ]]; then
          warn "路径不能为空；如果你想用仓库根目录，请选择“返回仓库根目录”"
          continue
        fi
        validate_remote_path_or_die "$repo" "$branch" "$manual" "$allow_empty"
        printf '%s\n' "$manual"
        return 0
        ;;
      返回仓库根目录)
        printf '\n'
        return 0
        ;;
      取消)
        die '已取消：远程路径选择'
        ;;
    esac
  done
}

select_local_path_single() {
  local start_dir="${1:-$HOME}"
  local mode="${2:-any}"
  local method
  ui_header "本地路径向导"
  ui_micro_guide "你可以直接用选择器浏览本地文件，也可以切换到手动输入。下载通常选目录，更新通常选文件，同步通常选目录。"
  ui_rule
  method="$(choose_input_method '选择本地路径方式')"
  case "$method" in
    选择器)
      local selected first
      selected="$(select_local_paths "$start_dir")"
      first="${selected%%$'\n'*}"
      validate_local_path_or_die "$first" "$mode"
      printf '%s\n' "$first"
      ;;
    手动输入)
      local input
      input="$(prompt_tty '请输入本地路径' "$start_dir")"
      validate_local_path_or_die "$input" "$mode"
      printf '%s\n' "$input"
      ;;
    取消)
      die '已取消：选择本地路径方式'
      ;;
  esac
}

render_selected_paths() {
  local f="$1" n=1 l
  [[ -s "$f" ]] || { ui_line "  ${SURFACE}暂未选择${NC}"; return; }
  while IFS= read -r l; do printf '%b\n' "  ${SUCCESS}●${NC} ${SURFACE}$(printf '%02d' "$n")${NC} ${l}" > /dev/tty; n=$((n+1)); done < "$f"
}

list_browser_entries() {
  find "$1" -maxdepth 1 -mindepth 1 \
    ! -name '.git' ! -name 'release' ! -name 'reports' ! -name 'hermes.log' ! -name '→ 临时克隆仓库*' \
    -printf '%y\t%f\t%p\n' 2>/dev/null | sort -k1,1r -k2,2f
}

toggle_selected_path() {
  local selected_file="$1" target="$2"
  if grep -Fxq "$target" "$selected_file" 2>/dev/null; then
    grep -Fxv "$target" "$selected_file" > "$selected_file.tmp" || true
    mv "$selected_file.tmp" "$selected_file"
  else
    printf '%s\n' "$target" >> "$selected_file"
  fi
}

preview_path() {
  local path="$1"
  if [[ -d "$path" ]]; then
    printf '目录: %s\n\n' "$path"
    find "$path" -maxdepth 2 -mindepth 1 -printf '%y  %p\n' 2>/dev/null | sed -n '1,80p'
  elif [[ -f "$path" ]]; then
    printf '文件: %s\n大小: ' "$path"
    du -h "$path" 2>/dev/null | awk '{print $1}'
    printf '\n'
    sed -n '1,120p' "$path" 2>/dev/null || file "$path" 2>/dev/null || true
  else
    printf '无法读取: %s\n' "$path"
  fi
}

select_local_paths_fzf() {
  local base_dir="$1" selected_file="$2" current="$base_dir"
  local entries_file rows_file picked line idx typ name path picked_idx row row_count selected_count action
  while true; do
    entries_file="$(mktemp "$TMP_ROOT/browser-entries.XXXXXX")"
    rows_file="$(mktemp "$TMP_ROOT/browser-rows.XXXXXX")"
    list_browser_entries "$current" > "$entries_file"
    idx=1
    while IFS=$'\t' read -r typ name path; do
      local kind="文件" mark=" " size=""
      [[ "$typ" == d ]] && kind="目录"
      grep -Fxq "$path" "$selected_file" 2>/dev/null && mark="●"
      if [[ "$typ" == f ]]; then size="$(du -h "$path" 2>/dev/null | awk '{print $1}')"; else size="--"; fi
      printf '%03d\t%s\t%s\t%-4s\t%-8s\t%s\t%s\n' "$idx" "$path" "$mark" "$kind" "$size" "$name" "$path" >> "$rows_file"
      idx=$((idx+1))
    done < "$entries_file"
    row_count=$((idx-1))
    selected_count="$(wc -l < "$selected_file" 2>/dev/null || printf '0')"
    local opts=()
    mapfile -t opts < <(fzf_common_opts)
    picked="$(cut -f1,3,4,5,6 "$rows_file" | fzf "${opts[@]}" --multi \
      --height="${GITHUB_MANAGER_FILE_PICKER_HEIGHT:-26}" \
      --header=" 当前目录: $current | 已选: $selected_count | ↑↓/鼠标滚轮滚动 | Tab多选 | Enter进入目录/选择文件 | Alt-a选目录 | Alt-u上级 | Alt-h回家 | Alt-d完成 " \
      --prompt='  文件 > ' \
      --preview="bash -c 'p=\$(awk -F\\\"\\t\\\" -v n={1} \\\"\\$1==n{print \\\$2; exit}\\\" \"$rows_file\"); if [ -d \"\$p\" ]; then printf \"目录: %s\\n\\n\" \"\$p\"; find \"\$p\" -maxdepth 2 -mindepth 1 -printf \"%y  %p\\n\" 2>/dev/null | sed -n \"1,80p\"; elif [ -f \"\$p\" ]; then printf \"文件: %s\\n大小: \" \"\$p\"; du -h \"\$p\" 2>/dev/null | awk '\''{print \\\$1}'\''; printf \"\\n\"; sed -n \"1,120p\" \"\$p\" 2>/dev/null || file \"\$p\"; fi'" \
      --preview-window='right:52%:wrap:border-left' \
      --bind="alt-u:become(echo __UP__)" \
      --bind="alt-h:become(echo __HOME__)" \
      --bind="alt-d:become(echo __DONE__)" \
      --bind="alt-a:become(echo __SELECT_DIR__ {1})" \
      < /dev/tty)"
    action=$?
    rm -f "$entries_file"
    if [[ $action -ne 0 ]]; then rm -f "$rows_file"; return 1; fi
    case "$picked" in
      __UP__)
        [[ "$current" != "$base_dir" && "$current" != / ]] && current="$(dirname "$current")"
        rm -f "$rows_file"; continue ;;
      __HOME__)
        current="$base_dir"; rm -f "$rows_file"; continue ;;
      __DONE__)
        rm -f "$rows_file"; [[ -s "$selected_file" ]] && return 0 || { warn "还没有选择任何项目"; ui_pause; continue; } ;;
      __SELECT_DIR__*)
        picked_idx="${picked##* }"; row="$(awk -F'\t' -v n="$picked_idx" '$1==n{print; exit}' "$rows_file")"; path="$(cut -f2 <<< "$row")"; [[ -n "$path" ]] && toggle_selected_path "$selected_file" "$path"; rm -f "$rows_file"; continue ;;
    esac
    [[ -n "$picked" ]] || { rm -f "$rows_file"; continue; }
    while IFS= read -r line; do
      picked_idx="${line%%$'\t'*}"
      row="$(awk -F'\t' -v n="$picked_idx" '$1==n{print; exit}' "$rows_file")"
      typ="$(cut -f4 <<< "$row" | xargs)"
      path="$(cut -f2 <<< "$row")"
      if [[ "$typ" == "目录" && "$(printf '%s\n' "$picked" | wc -l)" -eq 1 ]]; then
        current="$path"
      elif [[ -n "$path" ]]; then
        toggle_selected_path "$selected_file" "$path"
      fi
    done <<< "$picked"
    rm -f "$rows_file"
  done
}

select_local_paths() {
  local base_dir="${1:-$HOME}" current selected_file
  base_dir="$(cd "$base_dir" && pwd)"
  current="$base_dir"
  is_interactive_tty || die "非交互环境请直接传入文件/目录路径"
  selected_file="$(mktemp "$TMP_ROOT/selected-paths.XXXXXX")"
  if tui_available; then
    local tui_out
    tui_out="$(mktemp "$TMP_ROOT/tui-files.XXXXXX")"
    if GHM_TUI_OUTPUT_FILE="$tui_out" "$PROJECT_ROOT/bin/ghm-tui.py" files "$base_dir" < /dev/tty > /dev/tty; then
      cat "$tui_out"
      rm -f "$tui_out" "$selected_file"
      return 0
    fi
    rm -f "$tui_out"
  fi
  if fzf_available; then
    if select_local_paths_fzf "$base_dir" "$selected_file"; then
      cat "$selected_file"; rm -f "$selected_file"; return 0
    fi
  fi
  while true; do
    ui_header "本地文件选择器"
    ui_micro_guide "初始目录为 $base_dir。数字进入目录/选择文件，s数字选择目录，u上级，h回初始目录，m手动路径，d完成，q取消。"
    ui_rule
    ui_line "${BOLD}${FG}当前目录:${NC} ${current}"
    ui_line "${BOLD}${FG}已选择:${NC}"; render_selected_paths "$selected_file"; ui_rule
    local entries_file idx typ name path mark input row target num
    entries_file="$(mktemp "$TMP_ROOT/browser-entries.XXXXXX")"
    list_browser_entries "$current" > "$entries_file"
    idx=1
    if [[ ! -s "$entries_file" ]]; then
      ui_line "  ${SURFACE}空目录或无权限读取${NC}"
    else
      while IFS=$'\t' read -r typ name path; do
        local icon="目录"
        [[ "$typ" == f ]] && icon="文件"
        mark=" "; grep -Fxq "$path" "$selected_file" 2>/dev/null && mark="●"
        printf '%b\n' "  ${ACCENT}$(printf '%02d' "$idx")${NC}  ${SURFACE}${icon}${NC} ${SUCCESS}${mark}${NC} ${FG}${name}${NC}" > /dev/tty
        idx=$((idx+1))
      done < "$entries_file"
    fi
    input="$(ui_read '操作')"
    case "$input" in
      q|Q) rm -f "$entries_file" "$selected_file"; die "已取消文件选择";;
      d|D) rm -f "$entries_file"; [[ -s "$selected_file" ]] || { warn "还没有选择任何项目"; ui_pause; continue; }; cat "$selected_file"; rm -f "$selected_file"; return 0;;
      u|U) [[ "$current" != "$base_dir" && "$current" != / ]] && current="$(dirname "$current")" || { warn "已经在起始目录"; ui_pause; };;
      h|H) current="$base_dir";;
      m|M) local manual abs; manual="$(ui_read '请输入路径')"; [[ -n "$manual" ]] || continue; [[ "$manual" = /* ]] && abs="$manual" || abs="$current/$manual"; [[ -e "$abs" ]] || { warn "路径不存在：$abs"; ui_pause; continue; }; abs="$(cd "$(dirname "$abs")" && pwd)/$(basename "$abs")"; toggle_selected_path "$selected_file" "$abs";;
      s[0-9]*|S[0-9]*) num="${input:1}"; row="$(sed -n "${num}p" "$entries_file")"; [[ -n "$row" ]] || { warn "编号不存在"; ui_pause; continue; }; target="$(cut -f3 <<< "$row")"; toggle_selected_path "$selected_file" "$target";;
      ''|*[!0-9]*) warn "未知操作：$input"; ui_pause;;
      *) row="$(sed -n "${input}p" "$entries_file")"; [[ -n "$row" ]] || { warn "编号不存在"; ui_pause; continue; }; typ="$(cut -f1 <<< "$row")"; target="$(cut -f3 <<< "$row")"; if [[ "$typ" == d ]]; then current="$target"; else toggle_selected_path "$selected_file" "$target"; fi;;
    esac
    rm -f "$entries_file"
  done
}

confirm_summary() {
  ui_header "确认上传"
  ui_line "  仓库:     $1"
  ui_line "  分支:     $2"
  ui_line "  远程目录: ${3:-/}"
  ui_line "  提交说明: $4"
  ui_rule
  ui_line "$5"
  confirm "确认继续？" Y
}

main_menu() {
  local choice selected
  menu_header "主页"
  ui_line "${SURFACE}提示:${NC} ${MUTED}上传会先确认；同步建议先 dry-run；删除/仓库删除属于危险操作，会再次确认。${NC}"
  ui_line ""
  local labels=("上传文件" "浏览仓库" "下载文件" "删除文件" "更新文件" "同步文件夹" "仓库管理" "账号/设置" "关于" "审计日志" "生成发布包" "退出")
  local descs=("选择本地文件/目录并上传" "查看远程仓库文件" "下载远程文件或目录" "删除远程文件或目录" "用本地文件覆盖远程文件" "push/pull 双向同步并生成报告" "创建/查看/克隆/重命名/转移/删除仓库" "查看路径、切换登录账号、PAT 设置" "产品说明" "查看最近关键操作" "构建 release 目录" "关闭程序")
  if tui_available; then
    local tui_out
    tui_out="$(mktemp "$TMP_ROOT/tui-menu.XXXXXX")"
    if GHM_TUI_OUTPUT_FILE="$tui_out" "$PROJECT_ROOT/bin/ghm-tui.py" menu < /dev/tty > /dev/tty; then
      selected="$(cat "$tui_out")"
      rm -f "$tui_out"
      printf '%s\n' "$selected"
      return 0
    fi
    rm -f "$tui_out"
  fi
  if fzf_available; then
    local rows=() i opts=()
    mapfile -t opts < <(fzf_common_opts)
    for i in "${!labels[@]}"; do rows+=("$(printf '%02d  %-12s  %s' "$((i+1))" "${labels[$i]}" "${descs[$i]}")"); done
    selected="$(printf '%s\n' "${rows[@]}" | fzf "${opts[@]}" --height=22 --header=' GitHub Manager Pro · ↑↓/鼠标滚轮选择 · Enter确认 · Esc退出 ' --prompt='  功能 > ' < /dev/tty || true)"
    if [[ -z "$selected" ]]; then
      printf '12\n'
      return 0
    fi
    printf '%s\n' "$((10#${selected%% *}))"
    return 0
  fi
  local i idx=1
  for i in "${!labels[@]}"; do printf '%b\n' "  ${ACCENT}$(printf '%02d' "$idx")${NC}  ${BOLD}${FG}$(printf '%-12s' "${labels[$i]}")${NC} ${MUTED}${descs[$i]}${NC}" > "$(ui_target)"; idx=$((idx+1)); done
  ui_line ""; choice="$(ui_read '请输入编号')"
  case "$choice" in \?) ui_header "快速指南"; ui_micro_guide "上传：选文件 -> 选仓库 -> 选分支 -> 填远程目录 -> 确认。"; ui_micro_guide "浏览：选仓库，远程目录留空就是根目录。"; ui_micro_guide "同步：先 dry-run 看报告，再执行 push/pull。"; ui_pause; main_menu;; 1|2|3|4|5|6|7|8|9|10|11|12) printf '%s\n' "$choice";; q|Q) printf '12\n';; *) die '未选择：请选择功能';; esac
}
