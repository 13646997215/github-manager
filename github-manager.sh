#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

show_help() {
  cat <<'EOF'
GitHub Manager Pro - 完整实用版

用法:
  ./github-manager.sh menu
  ./github-manager.sh quick-upload [paths...]
  ./github-manager.sh list <repo> [remote_path]
  ./github-manager.sh download <repo> <remote_path> <save_to>
  ./github-manager.sh delete <repo> <remote_path>
  ./github-manager.sh update <repo> <remote_path> <local_file>
  ./github-manager.sh sync <repo> <local_dir> [remote_path] [--mode push|pull]
  ./github-manager.sh repo <create|delete|info|clone|rename|transfer> ...
  ./github-manager.sh install [--local-bin PATH] [--with-desktop]
  ./github-manager.sh settings
  ./github-manager.sh about
  ./github-manager.sh audit
  ./github-manager.sh release
  ./github-manager.sh help

特性:
  - 拖拽文件到脚本或桌面快捷方式即可上传
  - 支持交互式仓库选择、分支选择、提交信息输入
  - 支持双向同步、冲突报告、审计日志、发布打包
EOF
}

if [[ "${1:-}" =~ ^(--help|-h|help)$ ]]; then
  show_help
  exit 0
fi

# shellcheck disable=SC1091
source "$ROOT_DIR/lib/common.sh"
# shellcheck disable=SC1091
source "$ROOT_DIR/lib/files.sh"

parse_common_flags() {
  PARSED_BRANCH=""
  PARSED_COMMIT_MESSAGE="$DEFAULT_COMMIT_MESSAGE"
  PARSED_LOCAL_BIN="$HOME/.local/bin"
  PARSED_WITH_DESKTOP="false"
  PARSED_DRY_RUN="false"
  PARSED_MODE="push"
  PARSED_REPORT_FILE=""
  PARSED_REPO=""
  PARSED_REMOTE_PATH=""
  PARSED_FORCE="false"
  PARSED_VISIBILITY="private"
  PARSED_HOMEPAGE=""
  PARSED_CLONE_AFTER_CREATE="false"
  PARSED_DISABLE_ISSUES="false"
  PARSED_DISABLE_WIKI="false"
  PARSED_TEAM=""
  PARSED_TREE="false"
  POSITIONAL=()

  while (($#)); do
    case "$1" in
      --repo)
        PARSED_REPO="${2:-}"
        shift 2
        ;;
      --remote-path)
        PARSED_REMOTE_PATH="${2:-}"
        shift 2
        ;;
      --branch)
        PARSED_BRANCH="${2:-}"
        shift 2
        ;;
      --message)
        PARSED_COMMIT_MESSAGE="${2:-}"
        shift 2
        ;;
      --local-bin)
        PARSED_LOCAL_BIN="${2:-}"
        shift 2
        ;;
      --with-desktop)
        PARSED_WITH_DESKTOP="true"
        shift
        ;;
      --dry-run)
        PARSED_DRY_RUN="true"
        shift
        ;;
      --mode)
        PARSED_MODE="${2:-}"
        shift 2
        ;;
      --report|--report-file)
        PARSED_REPORT_FILE="${2:-}"
        shift 2
        ;;
      --force|-f)
        PARSED_FORCE="true"
        shift
        ;;
      --public)
        PARSED_VISIBILITY="public"
        shift
        ;;
      --private)
        PARSED_VISIBILITY="private"
        shift
        ;;
      --homepage)
        PARSED_HOMEPAGE="${2:-}"
        shift 2
        ;;
      --clone)
        PARSED_CLONE_AFTER_CREATE="true"
        shift
        ;;
      --disable-issues)
        PARSED_DISABLE_ISSUES="true"
        shift
        ;;
      --disable-wiki)
        PARSED_DISABLE_WIKI="true"
        shift
        ;;
      --team)
        PARSED_TEAM="${2:-}"
        shift 2
        ;;
      --description)
        POSITIONAL+=("$1" "${2:-}")
        shift 2
        ;;
      --tree)
        PARSED_TREE="true"
        shift
        ;;
      --help|-h)
        POSITIONAL+=("$1")
        shift
        ;;
      --)
        shift
        while (($#)); do
          POSITIONAL+=("$1")
          shift
        done
        ;;
      --*)
        die "未知参数：$1"
        ;;
      *)
        POSITIONAL+=("$1")
        shift
        ;;
    esac
  done
}

repo_create() {
  local name="${1:-}"
  [[ -n "$name" ]] || die "仓库名不能为空"
  local description=""
  local idx=1
  while [[ $idx -lt ${#POSITIONAL[@]} ]]; do
    if [[ "${POSITIONAL[$idx]}" == "--description" ]]; then
      description="${POSITIONAL[$((idx + 1))]:-}"
      break
    fi
    idx=$((idx + 1))
  done
  local args=(repo create "$name" --confirm)
  if [[ "$PARSED_VISIBILITY" == "public" ]]; then
    args+=(--public)
  else
    args+=(--private)
  fi
  [[ -n "$description" ]] && args+=(--description "$description")
  [[ -n "$PARSED_HOMEPAGE" ]] && args+=(--homepage "$PARSED_HOMEPAGE")
  [[ "$PARSED_CLONE_AFTER_CREATE" == "true" ]] && args+=(--clone)
  [[ "$PARSED_DISABLE_ISSUES" == "true" ]] && args+=(--disable-issues)
  [[ "$PARSED_DISABLE_WIKI" == "true" ]] && args+=(--disable-wiki)
  [[ -n "$PARSED_TEAM" ]] && args+=(--team "$PARSED_TEAM")
  audit_log REPO_CREATE "$name visibility=$PARSED_VISIBILITY"
  gh "${args[@]}"
}

repo_delete() {
  local repo="$1"
  if [[ "$PARSED_FORCE" != "true" ]]; then
    confirm "危险操作：确认删除仓库 $repo ?" N || die "已取消删除"
  fi
  audit_log REPO_DELETE "$repo"
  gh repo delete "$repo" --yes
}

repo_info() {
  local repo="$1"
  [[ -n "$repo" ]] || die "用法: repo info <owner/repo>"
  audit_log REPO_INFO "$repo"
  gh repo view "$repo"
}

repo_clone() {
  local repo="$1"
  local target="${2:-}"
  [[ -n "$repo" ]] || die "用法: repo clone <owner/repo> [target]"
  audit_log REPO_CLONE "$repo -> ${target:-default}"
  if [[ -n "$target" ]]; then
    gh repo clone "$repo" "$target"
  else
    gh repo clone "$repo"
  fi
}

repo_rename() {
  local repo="$1"
  local new_name="$2"
  [[ -n "$repo" && -n "$new_name" ]] || die "用法: repo rename <owner/repo> <new-name>"
  gh api --method PATCH "repos/$repo" -f name="$new_name" >/dev/null
  success "仓库已重命名为 ${repo%/*}/$new_name"
  audit_log REPO_RENAME "$repo -> ${repo%/*}/$new_name"
}

repo_transfer() {
  local repo="$1"
  local new_owner="$2"
  local new_name="${3:-${repo##*/}}"
  [[ -n "$repo" && -n "$new_owner" ]] || die "用法: repo transfer <owner/repo> <new-owner> [new-name]"
  gh api --method POST "repos/$repo/transfer" -f new_owner="$new_owner" -f new_name="$new_name" >/dev/null
  success "已提交仓库转移请求：$repo -> $new_owner/$new_name"
  audit_log REPO_TRANSFER "$repo -> $new_owner/$new_name"
}

quick_upload_flow() {
  parse_common_flags "$@"
  if [[ "${POSITIONAL[0]:-}" =~ ^(--help|-h|help)$ ]]; then
    cat <<'EOF'
用法: upload [--repo owner/repo] [--remote-path PATH] [--branch BRANCH] [--message MSG] <file_or_dir>...
示例: ghm-upload --repo owner/repo --remote-path docs ./README.md
EOF
    return 0
  fi
  local paths=()
  local repo branch remote_path commit_message selected repo_input
  local path_count=0

  export GITHUB_MANAGER_QUIET=1

  if [[ ${#POSITIONAL[@]} -gt 0 ]]; then
    paths=("${POSITIONAL[@]}")
  else
    local selection
    selection="$(select_local_paths "$HOME")"
    mapfile -t paths < <(printf '%s\n' "$selection")
  fi

  if [[ ${#paths[@]} -eq 0 ]]; then
    die "未提供要上传的文件或目录"
  fi

  path_count=${#paths[@]}

  if [[ -n "$PARSED_REPO" ]]; then
    repo="$PARSED_REPO"
  else
    repo_input="$(select_repo_interactive)"
    repo="${repo_input%%$'\n'*}"
  fi
  branch="${PARSED_BRANCH:-$(get_repo_default_branch "$repo")}"
  branch="${branch:-$DEFAULT_BRANCH}"
  if [[ -z "$PARSED_BRANCH" && -t 0 && -t 1 ]]; then
    branch="$(select_branch "$repo")"
  fi
  remote_path="$PARSED_REMOTE_PATH"
  if [[ -z "$PARSED_REMOTE_PATH" && -t 0 && -t 1 ]]; then
    remote_path="$(select_remote_path)"
  fi
  commit_message="${PARSED_COMMIT_MESSAGE:-$DEFAULT_COMMIT_MESSAGE}"
  if [[ "$commit_message" == "$DEFAULT_COMMIT_MESSAGE" && -t 0 && -t 1 ]]; then
    commit_message="$(select_commit_message "$DEFAULT_COMMIT_MESSAGE")"
  fi

  log_operation_start QUICK_UPLOAD "$(build_audit_payload repo "$repo" branch "$branch" remote_path "${remote_path:-/}" local_path "$(join_by ';' "${paths[@]}")" file_count "$path_count" commit_message "$commit_message")" >/dev/null

  local formatted_paths=""
  for selected in "${paths[@]}"; do
    formatted_paths+="  - $selected"$'\n'
  done
  if [[ -t 0 && -t 1 ]]; then
    confirm_summary "$repo" "$branch" "$remote_path" "$commit_message" "$formatted_paths"
  fi

  upload_via_git "$repo" "$branch" "$remote_path" "$commit_message" "${paths[@]}"
  unset GITHUB_MANAGER_QUIET
  audit_log QUICK_UPLOAD "$repo branch=$branch remote=${remote_path:-/}"
  log_operation_end success "$(build_audit_payload repo "$repo" branch "$branch" remote_path "${remote_path:-/}" local_path "$(join_by ';' "${paths[@]}")" file_count "$path_count" commit_message "$commit_message")"
}

list_flow() {
  parse_common_flags "$@"
  if [[ "${POSITIONAL[0]:-}" =~ ^(--help|-h|help)$ ]]; then
    cat <<'EOF'
用法: list <repo> [remote_path] [--tree] [--branch BRANCH]
示例: ghm-list owner/repo docs --tree
EOF
    return 0
  fi
  local repo="${PARSED_REPO:-${POSITIONAL[0]:-}}"
  local remote_path="$PARSED_REMOTE_PATH"
  if [[ -z "$remote_path" ]]; then
    for arg in "${POSITIONAL[@]:1}"; do
      if [[ "$arg" != --* ]]; then
        remote_path="$arg"
        break
      fi
    done
  fi

  [[ -n "$repo" ]] || die "用法: list <repo> [remote_path]"
  branch="${PARSED_BRANCH:-$(get_repo_default_branch "$repo")}" 
  branch="${branch:-$DEFAULT_BRANCH}"

  if [[ "$PARSED_TREE" == "true" ]]; then
    print_tree_view "$repo" "$branch"
  else
    list_remote_files "$repo" "$remote_path" "$branch" | while IFS=$'\t' read -r type path size sha download_url; do
      if [[ "$type" == "dir" ]]; then
        printf '  %b\n' "${ACCENT:-}DIR ${NC:-} ${path}"
      else
        printf '  %b\n' "${FG:-}FILE${NC:-} ${path} ${SURFACE:-}$(bytes_to_human "$size")${NC:-}"
      fi
    done
  fi
  if [[ -t 0 && -t 1 ]]; then
    ui_pause 2>/dev/null || true
  fi
}

download_flow() {
  parse_common_flags "$@"
  if [[ "${POSITIONAL[0]:-}" =~ ^(--help|-h|help)$ ]]; then
    cat <<'EOF'
用法: download <repo> <remote_path> <save_to> [--branch BRANCH]
示例: ghm-download owner/repo docs/README.md ./downloads
EOF
    return 0
  fi
  local repo="${PARSED_REPO:-${POSITIONAL[0]:-}}"
  local remote_path="${PARSED_REMOTE_PATH:-${POSITIONAL[1]:-}}"
  local save_to="${POSITIONAL[2]:-}"
  [[ -n "$repo" && -n "$remote_path" && -n "$save_to" ]] || die "用法: download <repo> <remote_path> <save_to>"
  local branch="${PARSED_BRANCH:-$(get_repo_default_branch "$repo")}" 
  branch="${branch:-$DEFAULT_BRANCH}"
  log_operation_start DOWNLOAD "$(build_audit_payload repo "$repo" branch "$branch" remote_path "$remote_path" local_path "$save_to")" >/dev/null
  download_path "$repo" "$remote_path" "$save_to" "$branch"
  audit_log DOWNLOAD "$repo:$remote_path -> $save_to"
  log_operation_end success "$(build_audit_payload repo "$repo" branch "$branch" remote_path "$remote_path" local_path "$save_to")"
}

delete_flow() {
  parse_common_flags "$@"
  if [[ "${POSITIONAL[0]:-}" =~ ^(--help|-h|help)$ ]]; then
    cat <<'EOF'
用法: delete <repo> <remote_path> [--force] [--branch BRANCH] [--message MSG]
示例: ghm-delete owner/repo docs/old.txt --force
EOF
    return 0
  fi
  local repo="${PARSED_REPO:-${POSITIONAL[0]:-}}"
  local remote_path="${PARSED_REMOTE_PATH:-${POSITIONAL[1]:-}}"
  [[ -n "$repo" && -n "$remote_path" ]] || die "用法: delete <repo> <remote_path>"
  local branch="${PARSED_BRANCH:-$(get_repo_default_branch "$repo")}" 
  branch="${branch:-$DEFAULT_BRANCH}"
  log_operation_start DELETE "$(build_audit_payload repo "$repo" branch "$branch" remote_path "$remote_path" commit_message "$PARSED_COMMIT_MESSAGE" force "$PARSED_FORCE")" >/dev/null
  if [[ "$PARSED_FORCE" != "true" ]]; then
    if [[ ! -r /dev/tty || ! -w /dev/tty ]]; then
      die "删除是危险操作；非交互环境必须显式添加 --force"
    fi
    confirm "危险操作：确认删除 $repo:$remote_path ?" N || die "已取消删除"
  fi
  delete_remote_path_recursive "$repo" "$remote_path" "$branch" "$PARSED_COMMIT_MESSAGE"
  audit_log DELETE "$repo:$remote_path"
  log_operation_end success "$(build_audit_payload repo "$repo" branch "$branch" remote_path "$remote_path" commit_message "$PARSED_COMMIT_MESSAGE" force "$PARSED_FORCE")"
}

update_flow() {
  parse_common_flags "$@"
  if [[ "${POSITIONAL[0]:-}" =~ ^(--help|-h|help)$ ]]; then
    cat <<'EOF'
用法: update <repo> <remote_path> <local_file> [--branch BRANCH] [--message MSG]
示例: ghm-update owner/repo docs/README.md ./README.md
EOF
    return 0
  fi
  local repo="${PARSED_REPO:-${POSITIONAL[0]:-}}"
  local remote_path="${PARSED_REMOTE_PATH:-${POSITIONAL[1]:-}}"
  local local_file="${POSITIONAL[2]:-}"
  [[ -n "$repo" && -n "$remote_path" && -n "$local_file" ]] || die "用法: update <repo> <remote_path> <local_file>"
  local branch="${PARSED_BRANCH:-$(get_repo_default_branch "$repo")}" 
  branch="${branch:-$DEFAULT_BRANCH}"
  log_operation_start UPDATE "$(build_audit_payload repo "$repo" branch "$branch" remote_path "$remote_path" local_path "$local_file" commit_message "$PARSED_COMMIT_MESSAGE")" >/dev/null
  update_file_contents "$repo" "$remote_path" "$local_file" "$branch" "$PARSED_COMMIT_MESSAGE"
  audit_log UPDATE "$repo:$remote_path <- $local_file"
  log_operation_end success "$(build_audit_payload repo "$repo" branch "$branch" remote_path "$remote_path" local_path "$local_file" commit_message "$PARSED_COMMIT_MESSAGE")"
}

write_sync_report() {
  local file="$1"
  local repo="$2"
  local local_dir="$3"
  local remote_path="$4"
  local mode="$5"
  local report_content="$6"
  mkdir -p "$(dirname "$file")"
  cat > "$file" <<EOF
GitHub Manager Pro 同步报告
时间: $(date '+%F %T')
仓库: $repo
本地目录: $local_dir
远程路径: ${remote_path:-/}
模式: $mode

详情:
$report_content
EOF
  success "同步报告已导出：$file"
  audit_log SYNC_REPORT "$file"
}

sync_flow() {
  parse_common_flags "$@"
  if [[ "${POSITIONAL[0]:-}" =~ ^(--help|-h|help)$ ]]; then
    cat <<'EOF'
用法: sync <repo> <local_dir> [remote_path] [--mode push|pull] [--dry-run] [--report FILE]
示例: ghm-sync owner/repo ./local docs --mode push --dry-run --report ./reports/sync.txt
EOF
    return 0
  fi
  local repo="${PARSED_REPO:-${POSITIONAL[0]:-}}"
  local local_dir="${POSITIONAL[1]:-}"
  local remote_path="${PARSED_REMOTE_PATH:-${POSITIONAL[2]:-}}"
  [[ -n "$repo" && -n "$local_dir" ]] || die "用法: sync <repo> <local_dir> [remote_path] [--mode push|pull]"
  local branch="${PARSED_BRANCH:-$(get_repo_default_branch "$repo")}" 
  branch="${branch:-$DEFAULT_BRANCH}"
  local report_file="${PARSED_REPORT_FILE:-$REPORT_DIR/sync-$(date +%Y%m%d-%H%M%S).txt}"
  log_operation_start SYNC "$(build_audit_payload repo "$repo" branch "$branch" remote_path "${remote_path:-/}" local_path "$local_dir" mode "$PARSED_MODE" dry_run "$PARSED_DRY_RUN" report_file "$report_file")" >/dev/null
  local preview
  preview="$(compare_sync_state "$repo" "$local_dir" "$remote_path" "$branch")"
  if [[ -n "$preview" ]]; then
    write_sync_report "$report_file" "$repo" "$local_dir" "$remote_path" "$PARSED_MODE" "$preview"
  fi
  case "$PARSED_MODE" in
    push) sync_local_to_remote "$repo" "$local_dir" "$remote_path" "$branch" "$PARSED_DRY_RUN" ;;
    pull) sync_remote_to_local "$repo" "$local_dir" "$remote_path" "$branch" "$PARSED_DRY_RUN" ;;
    *) die "未知同步模式：$PARSED_MODE（可选 push/pull）" ;;
  esac
  audit_log SYNC "$repo mode=$PARSED_MODE local=$local_dir remote=${remote_path:-/}"
  log_operation_end success "$(build_audit_payload repo "$repo" branch "$branch" remote_path "${remote_path:-/}" local_path "$local_dir" mode "$PARSED_MODE" dry_run "$PARSED_DRY_RUN" report_file "$report_file")"
}

install_flow() {
  parse_common_flags "$@"
  local target_dir="$PARSED_LOCAL_BIN"
  log_operation_start INSTALL "$(build_audit_payload local_path "$target_dir" with_desktop "$PARSED_WITH_DESKTOP")" >/dev/null
  mkdir -p "$target_dir"
  local cmd
  for cmd in ghm-upload ghm-list ghm-download ghm-delete ghm-sync ghm-update ghm-repo; do
    ln -sf "$ROOT_DIR/bin/$cmd" "$target_dir/$cmd"
  done
  success "已安装命令到 $target_dir"
  if ! grep -q "$target_dir" <<< ":$PATH:"; then
    warn "当前 PATH 未包含 $target_dir，可添加：export PATH=\"$target_dir:\$PATH\""
  fi
  if [[ "$PARSED_WITH_DESKTOP" == "true" ]]; then
    mkdir -p "$HOME/.local/share/applications"
    if [[ -f "$ROOT_DIR/GitHubManager.desktop" ]]; then
      cp -f "$ROOT_DIR/GitHubManager.desktop" "$HOME/.local/share/applications/GitHubManager.desktop"
    elif [[ -f "$HOME/Desktop/GitHubManager.desktop" ]]; then
      cp -f "$HOME/Desktop/GitHubManager.desktop" "$HOME/.local/share/applications/GitHubManager.desktop"
    else
      die "未找到 GitHubManager.desktop，无法安装桌面入口"
    fi
    success "已复制应用菜单入口到 ~/.local/share/applications/GitHubManager.desktop"
  fi
  audit_log INSTALL "$target_dir with_desktop=$PARSED_WITH_DESKTOP"
  log_operation_end success "$(build_audit_payload local_path "$target_dir" with_desktop "$PARSED_WITH_DESKTOP")"
}

repo_flow() {
  local subcommand="${1:-}"
  if [[ "$subcommand" =~ ^(--help|-h|help|)$ ]]; then
    cat <<'EOF'
用法: repo <create|delete|info|clone|rename|transfer> ...
  ghm-repo create <name> [--public|--private] [--description MSG] [--homepage URL] [--disable-issues] [--disable-wiki] [--clone] [--team TEAM]
  ghm-repo delete <owner/repo> [--force]
  ghm-repo info <owner/repo>
  ghm-repo clone <owner/repo> [target]
  ghm-repo rename <owner/repo> <new-name>
  ghm-repo transfer <owner/repo> <new-owner> [new-name]
EOF
    return 0
  fi
  shift || true
  parse_common_flags "$@"
  case "$subcommand" in
    create) repo_create "${POSITIONAL[0]:-}" ;;
    delete) repo_delete "${POSITIONAL[0]:-}" ;;
    info) repo_info "${POSITIONAL[0]:-}" ;;
    clone) repo_clone "${POSITIONAL[0]:-}" "${POSITIONAL[1]:-}" ;;
    rename) repo_rename "${POSITIONAL[0]:-}" "${POSITIONAL[1]:-}" ;;
    transfer) repo_transfer "${POSITIONAL[0]:-}" "${POSITIONAL[1]:-}" "${POSITIONAL[2]:-}" ;;
    *) die "未知 repo 子命令：$subcommand" ;;
  esac
}

settings_flow() {
  local current_user="未登录"
  current_user="$(get_current_user 2>/dev/null || printf '未登录')"
  cat <<EOF
配置与账号信息:
  当前 GitHub 账号: $current_user
  项目配置: $CONFIG_FILE
  PAT 文件 : $CONFIG_HOME/token
  日志文件 : $LOG_FILE
  审计日志 : $AUDIT_LOG_FILE
  报告目录 : $REPORT_DIR
  发布目录 : $RELEASE_DIR
  桌面快捷方式: $HOME/Desktop/GitHubManager.desktop
  应用菜单入口: $HOME/.local/share/applications/GitHubManager.desktop
EOF
}

switch_github_account_flow() {
  local action
  action="$(choose_from_list '账号/认证管理' '查看当前账号' '切换 gh 登录账号' '重新登录 gh' '配置 Personal Access Token' '清除 PAT' '返回')"
  case "$action" in
    查看当前账号)
      gh auth status --hostname github.com || true
      ui_pause
      ;;
    '切换 gh 登录账号')
      warn "即将进入 GitHub CLI 账号切换流程。你可以选择已有账号，或登录新账号。"
      gh auth switch --hostname github.com || gh auth login --hostname github.com
      rm -f "$REPO_CACHE_FILE" 2>/dev/null || true
      success "账号切换完成，仓库缓存已清空，下次会自动刷新"
      audit_log AUTH_SWITCH "gh auth switch/login"
      ui_pause
      ;;
    '重新登录 gh')
      warn "即将重新登录 GitHub CLI。"
      gh auth login --hostname github.com
      rm -f "$REPO_CACHE_FILE" 2>/dev/null || true
      success "重新登录完成，仓库缓存已清空"
      audit_log AUTH_LOGIN "gh auth login"
      ui_pause
      ;;
    '配置 Personal Access Token')
      local token
      token="$(prompt_tty '请输入 PAT（输入时会显示，注意别让旁边人看到）')"
      configure_pat "$token"
      rm -f "$REPO_CACHE_FILE" 2>/dev/null || true
      ui_pause
      ;;
    '清除 PAT')
      rm -f "$CONFIG_HOME/token"
      success "已清除 PAT 文件：$CONFIG_HOME/token"
      audit_log AUTH_PAT_CLEAR "$CONFIG_HOME/token"
      ui_pause
      ;;
    返回)
      return 0
      ;;
  esac
}

settings_menu_flow() {
  local action
  action="$(choose_from_list '账号/设置' '查看当前账号与路径' '账号切换/登录' '刷新仓库缓存' '返回')"
  case "$action" in
    '查看当前账号与路径')
      settings_flow
      ui_pause
      ;;
    '账号切换/登录')
      switch_github_account_flow
      ;;
    '刷新仓库缓存')
      rm -f "$REPO_CACHE_FILE" 2>/dev/null || true
      refresh_repo_cache
      success "仓库列表已强制刷新"
      ui_pause
      ;;
    返回)
      return 0
      ;;
  esac
}

interactive_repo_menu() {
  local action repo target name desc new_name owner
  action="$(choose_from_list '仓库管理' 'info' 'clone' 'create' 'rename' 'transfer' 'delete' '返回')"
  case "$action" in
    info)
      read -r -p '仓库: ' repo
      repo_flow info "$repo"
      ;;
    clone)
      read -r -p '仓库: ' repo
      read -r -p '目标目录(可空): ' target
      repo_flow clone "$repo" "$target"
      ;;
    create)
      read -r -p '新仓库名: ' name
      read -r -p '描述(可空): ' desc
      repo_flow create "$name" --description "$desc"
      ;;
    rename)
      read -r -p '仓库: ' repo
      read -r -p '新名称: ' new_name
      repo_flow rename "$repo" "$new_name"
      ;;
    transfer)
      read -r -p '仓库: ' repo
      read -r -p '新 owner: ' owner
      read -r -p '新名称(可空): ' new_name
      repo_flow transfer "$repo" "$owner" "$new_name"
      ;;
    delete)
      read -r -p '仓库: ' repo
      repo_flow delete "$repo"
      ;;
    返回)
      return 0
      ;;
  esac
}

interactive_select_repo() {
  select_repo_interactive
}

interactive_prompt_repo() {
  local repo
  repo="$(prompt_manual_or_browse_repo)"
  printf '%s\n' "$repo"
}

prompt_tty() {
  local prompt="$1" default="${2:-}" ans
  if [[ -n "$default" ]]; then
    printf '%s [%s]: ' "$prompt" "$default" > /dev/tty
  else
    printf '%s: ' "$prompt" > /dev/tty
  fi
  read -r ans < /dev/tty || ans=""
  printf '%s\n' "${ans:-$default}"
}

interactive_loop() {
  export GITHUB_MANAGER_UI_HEADER_ACTIVE=1
  ensure_first_run_setup
  while true; do
    local choice_num
    choice_num="$(main_menu)"
    case "$choice_num" in
      1) quick_upload_flow ;;
      2)
        repo="$(interactive_prompt_repo)"
        ui_micro_guide "浏览仓库：先选仓库，再选远程目录；如果想看仓库根目录，直接选“返回仓库根目录”就行。"
        path="$(select_remote_path_interactive "$repo" "$(get_repo_default_branch "$repo")" any true)"
        list_flow "$repo" "$path"
        ;;
      3)
        repo="$(interactive_prompt_repo)"
        ui_micro_guide "下载向导：先选远程文件/目录，再选本地保存目录；两边都支持手动输入。"
        remote_path="$(select_remote_path_interactive "$repo" "$(get_repo_default_branch "$repo")" any false)"
        save_to="$(select_local_path_single "$PWD/downloads" dir)"
        download_flow "$repo" "$remote_path" "$save_to"
        ;;
      4)
        repo="$(interactive_prompt_repo)"
        ui_micro_guide "删除向导：建议优先用远程浏览器选择，避免手填路径删错位置。"
        remote_path="$(select_remote_path_interactive "$repo" "$(get_repo_default_branch "$repo")" any false)"
        delete_flow "$repo" "$remote_path"
        ;;
      5)
        repo="$(interactive_prompt_repo)"
        ui_micro_guide "更新向导：远程端只允许选文件，本地端也建议选择文件，避免覆盖错目标。"
        remote_path="$(select_remote_path_interactive "$repo" "$(get_repo_default_branch "$repo")" file false)"
        local_file="$(select_local_path_single "$HOME" file)"
        update_flow "$repo" "$remote_path" "$local_file"
        ;;
      6)
        repo="$(interactive_prompt_repo)"
        ui_micro_guide "同步向导：先选本地目录，再选远程目录，最后选 push 或 pull。正式执行前建议先 dry-run。"
        local_dir="$(select_local_path_single "$PWD" dir)"
        remote_path="$(select_remote_path_interactive "$repo" "$(get_repo_default_branch "$repo")" dir true)"
        mode="$(choose_from_list '同步模式' 'push' 'pull' '取消')"
        [[ "$mode" == '取消' ]] && die '已取消：同步模式'
        sync_flow "$repo" "$local_dir" "$remote_path" --mode "${mode:-push}"
        ;;
      7) interactive_repo_menu ;;
      8) settings_menu_flow ;;
      9) show_about; ui_pause ;;
      10) show_audit_log; ui_pause ;;
      11) create_release_bundle; ui_pause ;;
      12) break ;;
      *) warn '无效选择，请重试' ;;
    esac
  done
}

main() {
  local command="${1:-menu}"
  shift || true
  case "$command" in
    menu) interactive_loop ;;
    quick-upload|upload) quick_upload_flow "$@" ;;
    list) list_flow "$@" ;;
    download) download_flow "$@" ;;
    delete) delete_flow "$@" ;;
    update) update_flow "$@" ;;
    sync) sync_flow "$@" ;;
    repo) repo_flow "$@" ;;
    install) install_flow "$@" ;;
    settings) settings_flow ;;
    about) show_about ;;
    audit) show_audit_log ;;
    release) create_release_bundle ;;
    help|--help|-h) show_help ;;
    *)
      if [[ -e "$command" ]]; then
        quick_upload_flow "$command" "$@"
      else
        die "未知命令：$command"
      fi
      ;;
  esac
}

main "$@"
