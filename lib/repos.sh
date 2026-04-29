#!/usr/bin/env bash
set -euo pipefail

# shellcheck disable=SC1091
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/auth.sh"

REPO_CACHE_FILE="$CACHE_DIR/repos.json"

repo_tui_available() { [[ "${GITHUB_MANAGER_USE_TUI:-1}" != "0" ]] && command -v python3 >/dev/null 2>&1 && [[ -x "$PROJECT_ROOT/bin/ghm-tui.py" && -r /dev/tty && -w /dev/tty ]]; }

cache_valid() {
  [[ -f "$REPO_CACHE_FILE" ]] || return 1
  local now mtime age
  now="$(date +%s)"
  mtime="$(stat -c %Y "$REPO_CACHE_FILE")"
  age=$((now - mtime))
  [[ "$age" -lt "$REPO_CACHE_TTL" ]]
}

fetch_repos_page() {
  local page="$1"
  if [[ "$AUTH_MODE" == "gh" ]] || is_gh_authenticated; then
    local limit=100 offset
    offset=$(((page - 1) * limit))
    gh repo list --limit "$((page * limit))" --json nameWithOwner,description,isPrivate,updatedAt,defaultBranchRef,viewerPermission | jq --argjson offset "$offset" --argjson limit "$limit" '.[ $offset : ($offset + $limit) ]'
  else
    run_gh_api "user/repos?per_page=100&page=$page&sort=updated" | jq '[.[] | {nameWithOwner: .full_name, description, isPrivate: .private, updatedAt, defaultBranchRef: {name: .default_branch}, viewerPermission: .permissions}]'
  fi
}

refresh_repo_cache() {
  ensure_auth >/dev/null
  local page=1 combined='[]' batch count
  while true; do
    batch="$(fetch_repos_page "$page")"
    count="$(jq 'length' <<< "$batch")"
    combined="$(jq -s 'add' <(printf '%s' "$combined") <(printf '%s' "$batch"))"
    [[ "$count" -lt 100 ]] && break
    page=$((page + 1))
  done
  printf '%s\n' "$combined" > "$REPO_CACHE_FILE"
  success "仓库缓存已刷新"
}

get_repos_json() { if ! cache_valid; then refresh_repo_cache; fi; cat "$REPO_CACHE_FILE"; }
list_repos() { get_repos_json | jq -r '.[] | [.nameWithOwner, (.defaultBranchRef.name // "main"), (if .isPrivate then "private" else "public" end), (.updatedAt // ""), (.description // "")] | @tsv'; }
repo_exists() { local repo="$1"; get_repos_json | jq -e --arg repo "$repo" '.[] | select(.nameWithOwner == $repo)' >/dev/null; }
get_repo_default_branch() { local repo="$1"; get_repos_json | jq -r --arg repo "$repo" '.[] | select(.nameWithOwner == $repo) | .defaultBranchRef.name // empty' | head -n 1; }

select_repo_interactive() {
  local repos selected
  repos="$(list_repos)"
  [[ -n "$repos" ]] || die "未获取到任何仓库"
  if [[ ! -r /dev/tty || ! -w /dev/tty ]]; then
    die "非交互环境不能自动选择仓库，请使用 --repo owner/repo"
  fi

  if repo_tui_available; then
    local tui_out items_file name branch visibility updated desc display
    tui_out="$(mktemp "$TMP_ROOT/tui-repo.XXXXXX")"
    items_file="$(mktemp "$TMP_ROOT/tui-repo-items.XXXXXX")"
    while IFS=$'\t' read -r name branch visibility updated desc; do
      display="$(printf '%-45s [%s/%s] %s' "$name" "$branch" "$visibility" "$desc")"
      printf '%s\n' "$display" >> "$items_file"
    done <<< "$repos"
    if GHM_TUI_OUTPUT_FILE="$tui_out" "$PROJECT_ROOT/bin/ghm-tui.py" choose "选择仓库" "$items_file" < /dev/tty > /dev/tty; then
      selected="$(cat "$tui_out" | awk '{print $1}')"
      rm -f "$tui_out" "$items_file"
      [[ -n "$selected" ]] || die "未选择仓库"
      printf '%s\n' "$selected"
      return 0
    fi
    rm -f "$tui_out" "$items_file"
  fi

  if [[ "${GITHUB_MANAGER_USE_FZF:-0}" != "0" ]] && command -v fzf >/dev/null 2>&1; then
    selected="$(printf '%s\n' "$repos" | awk -F'\t' '{printf "%-45s [%s/%s] %s\n", $1, $2, $3, $5}' | fzf --layout=reverse --border --height=80% --cycle --prompt='选择仓库 > ' < /dev/tty | awk '{print $1}')" || die "未选择仓库"
    [[ -n "$selected" ]] || die "未选择仓库"
    printf '%s\n' "$selected"
    return 0
  fi

  local options=() idx=1 name branch visibility updated desc
  printf '\n仓库列表：\n' > /dev/tty
  while IFS=$'\t' read -r name branch visibility updated desc; do
    printf '  %2s) %-42s [%s/%s] %s\n' "$idx" "$name" "$branch" "$visibility" "$desc" > /dev/tty
    options+=("$name")
    idx=$((idx + 1))
  done <<< "$repos"
  printf '请选择仓库编号: ' > /dev/tty
  read -r idx < /dev/tty || idx=""
  [[ "$idx" =~ ^[0-9]+$ ]] || die "未选择仓库"
  selected="${options[$((idx - 1))]:-}"
  [[ -n "$selected" ]] || die "未选择仓库"
  printf '%s\n' "$selected"
}
