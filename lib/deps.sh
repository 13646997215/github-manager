#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/env.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/common.sh"

declare -A GHM_REQUIRED=(
  [gh]="GitHub CLI（认证+API）"
  [git]="Git 操作"
  [jq]="JSON 处理"
  [curl]="HTTP 请求"
)

declare -A GHM_OPTIONAL=(
  [fzf]="模糊搜索选择"
  [whiptail]="终端菜单"
  [rsync]="高效同步"
)

check_dependencies() {
  if [[ -n "${GITHUB_MANAGER_DEPS_CHECKED:-}" ]]; then
    return 0
  fi
  export GITHUB_MANAGER_DEPS_CHECKED=1
  local missing=()
  local cmd
  for cmd in "${!GHM_REQUIRED[@]}"; do
    if command -v "$cmd" >/dev/null 2>&1; then
      success "依赖可用: $cmd"
    else
      error "缺少依赖: $cmd (${GHM_REQUIRED[$cmd]})"
      missing+=("$cmd")
    fi
  done

  for cmd in "${!GHM_OPTIONAL[@]}"; do
    if command -v "$cmd" >/dev/null 2>&1; then
      info "可选依赖可用: $cmd"
    else
      warn "可选依赖缺失: $cmd (${GHM_OPTIONAL[$cmd]})"
    fi
  done

  if [[ ${#missing[@]} -gt 0 ]]; then
    print_install_instructions >&2
    die "缺少必需依赖：$(join_by ', ' "${missing[@]}")"
  fi
}

print_install_instructions() {
  cat <<'EOF'
请安装以下依赖后重试：
  sudo apt update
  sudo apt install -y gh git jq curl fzf whiptail rsync
EOF
}
