#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}/github-manager"
CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/github-manager"
LOG_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/github-manager"
TMP_ROOT="${TMPDIR:-/tmp}/github-manager"
AUDIT_LOG_FILE="$LOG_DIR/audit.log"
REPORT_DIR="$PROJECT_ROOT/reports"
RELEASE_DIR="$PROJECT_ROOT/release"
FIRST_RUN_MARKER="$CONFIG_HOME/.first_run_completed"
APP_VERSION="2.0.0-defense"
APP_NAME="GitHub Manager Pro"

mkdir -p "$CONFIG_HOME" "$CACHE_DIR" "$LOG_DIR" "$TMP_ROOT" "$REPORT_DIR" "$RELEASE_DIR"

DEFAULT_BRANCH="main"
DEFAULT_COMMIT_MESSAGE="Upload via github-manager"
REPO_CACHE_TTL="${REPO_CACHE_TTL:-300}"
API_TIMEOUT="${API_TIMEOUT:-30}"
MAX_FILE_SIZE_WARN_MB="100"

CONFIG_FILE="$PROJECT_ROOT/config/config.yaml"
ENV_FILE="$PROJECT_ROOT/.env"
LOG_FILE="$LOG_DIR/github-manager.log"

COLOR=true
if [[ -n "${NO_COLOR:-}" || "${TERM:-}" == "dumb" ]]; then
  COLOR=false
elif [[ -n "${FORCE_COLOR:-}" || -n "${GITHUB_MANAGER_DESKTOP:-}" ]]; then
  COLOR=true
elif [[ ! -t 1 ]]; then
  COLOR=false
fi

ASCII_UI=false
if [[ -n "${GITHUB_MANAGER_ASCII:-}" || "${LANG:-}" == "C" || "${LC_ALL:-}" == "C" || "${TERM:-}" == "dumb" ]]; then
  ASCII_UI=true
fi

if $COLOR; then
  RED=$'\033[38;5;203m'
  GREEN=$'\033[38;5;120m'
  YELLOW=$'\033[38;5;222m'
  BLUE=$'\033[38;5;111m'
  MAGENTA=$'\033[38;5;183m'
  CYAN=$'\033[38;5;116m'
  BOLD=$'\033[1m'
  DIM=$'\033[2m'
  NC=$'\033[0m'
else
  RED=''; GREEN=''; YELLOW=''; BLUE=''; MAGENTA=''; CYAN=''; BOLD=''; DIM=''; NC=''
fi
FG="$CYAN"
MUTED="$DIM"
if $COLOR; then
  SURFACE=$'\033[38;5;238m'
else
  SURFACE=''
fi
ACCENT="$MAGENTA"
SUCCESS="$GREEN"
WARN="$YELLOW"
INFO="$BLUE"
ERROR_COLOR="$RED"

load_project_config() {
  local yaml_file="$CONFIG_FILE"
  if [[ -f "$yaml_file" ]]; then
    local line key value
    while IFS= read -r line; do
      [[ "$line" =~ ^[[:space:]]*# ]] && continue
      [[ ! "$line" =~ : ]] && continue
      key="${line%%:*}"
      value="${line#*:}"
      key="$(echo "$key" | tr '.' '_' | tr '[:lower:]' '[:upper:]' | xargs)"
      value="$(echo "$value" | sed 's/^ *//; s/ *$//' | sed 's/^"//; s/"$//' | sed "s/^'//; s/'$//")"
      case "$key" in
        DEFAULT_BRANCH) DEFAULT_BRANCH="$value" ;;
        DEFAULT_COMMIT_MESSAGE) DEFAULT_COMMIT_MESSAGE="$value" ;;
        DEFAULT_REPOSITORY) DEFAULT_REPOSITORY="$value" ;;
        PREFERRED_UPLOAD_STRATEGY) PREFERRED_UPLOAD_STRATEGY="$value" ;;
        USE_COLORS) [[ "$value" == "false" ]] && COLOR=false ;;
      esac
    done < "$yaml_file"
  fi

  if [[ -f "$ENV_FILE" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    set +a
  fi
}

load_project_config
