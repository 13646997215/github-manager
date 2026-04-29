#!/usr/bin/env bash
set -euo pipefail

INSTALL_DEPS=(gh git jq curl python3)
OPTIONAL_DEPS=(fzf whiptail rsync util-linux)

print_help() {
  cat <<'EOF'
用法: ./install-deps.sh [all|required|optional]

说明:
  all       安装必需依赖 + 推荐可选依赖
  required  仅安装必需依赖
  optional  仅安装可选依赖

依赖说明:
  必需: gh git jq curl python3
  可选: fzf whiptail rsync util-linux(script)
EOF
}

main() {
  local mode="${1:-all}"
  local deps=()
  case "$mode" in
    all) deps=("${INSTALL_DEPS[@]}" "${OPTIONAL_DEPS[@]}") ;;
    required) deps=("${INSTALL_DEPS[@]}") ;;
    optional) deps=("${OPTIONAL_DEPS[@]}") ;;
    help|--help|-h)
      print_help
      exit 0
      ;;
    *)
      print_help
      exit 1
      ;;
  esac

  sudo apt update
  sudo apt install -y "${deps[@]}"
}

main "$@"
