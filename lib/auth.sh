#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/common.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/deps.sh"

AUTH_MODE=""
PAT_FILE="$CONFIG_HOME/token"

is_gh_authenticated() {
  command_exists gh && gh auth status --hostname github.com >/dev/null 2>&1
}

has_pat_token() {
  [[ -f "$PAT_FILE" && -s "$PAT_FILE" ]]
}

load_pat_token() {
  has_pat_token || return 1
  export GITHUB_TOKEN
  GITHUB_TOKEN="$(tr -d '\r\n' < "$PAT_FILE")"
  [[ -n "$GITHUB_TOKEN" ]] || return 1
  AUTH_MODE="pat"
  ensure_file_permissions "$PAT_FILE" 600
  return 0
}

ensure_auth() {
  check_dependencies

  if is_gh_authenticated; then
    AUTH_MODE="gh"
    success "检测到 GitHub CLI 已登录"
    return 0
  fi

  if load_pat_token; then
    success "检测到 PAT 认证配置"
    return 0
  fi

  error "未检测到可用认证方式"
  cat >&2 <<'EOF'
请任选一种方式完成认证：
1. GitHub CLI（推荐）
   gh auth login
2. Personal Access Token
   将 token 保存到 ~/.config/github-manager/token
EOF
  return 1
}

get_auth_header_args() {
  if [[ "$AUTH_MODE" == "gh" ]] || is_gh_authenticated; then
    return 0
  fi
  if [[ "$AUTH_MODE" == "pat" ]] || has_pat_token; then
    [[ -z "${GITHUB_TOKEN:-}" ]] && load_pat_token
    printf '%s\n' "-H" "Authorization: Bearer ${GITHUB_TOKEN}"
    return 0
  fi
  return 1
}

run_gh_api() {
  ensure_auth >/dev/null
  local endpoint="$1"
  shift || true

  if [[ "$AUTH_MODE" == "gh" ]]; then
    gh api "$endpoint" "$@"
  else
    local header_args=()
    mapfile -t header_args < <(get_auth_header_args)
    curl -fsSL --connect-timeout "$API_TIMEOUT" \
      -H "Accept: application/vnd.github+json" \
      "${header_args[@]}" \
      "$@" \
      "https://api.github.com/$endpoint"
  fi
}

get_current_user() {
  ensure_auth >/dev/null
  if [[ "$AUTH_MODE" == "gh" ]]; then
    gh api user --jq '.login'
  else
    local header_args=()
    mapfile -t header_args < <(get_auth_header_args)
    curl -fsSL --connect-timeout "$API_TIMEOUT" \
      -H "Accept: application/vnd.github+json" \
      "${header_args[@]}" \
      https://api.github.com/user | jq -r '.login'
  fi
}

configure_pat() {
  local token="${1:-}"
  [[ -n "$token" ]] || die "PAT 为空"
  safe_mkdir "$CONFIG_HOME"
  printf '%s' "$token" > "$PAT_FILE"
  ensure_file_permissions "$PAT_FILE" 600
  success "PAT 已保存到 $PAT_FILE"
}

logout_auth() {
  rm -f "$PAT_FILE"
  if command_exists gh; then
    gh auth logout --hostname github.com -u >/dev/null 2>&1 || true
  fi
  success "本地 PAT 已移除；gh 登录若存在也已尝试退出"
}
