#!/usr/bin/env bash
set -euo pipefail

TARGET_ROOT="${1:-$HOME/.hermes/profiles/ros2-agent}"
REQUIRED_FILES=(
  "SOUL.md"
  "AGENTS.md"
  "config.yaml"
  ".env.template"
  "CAPABILITIES.md"
  "skill_manifest.json"
  "INSTALL_MANIFEST.md"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [[ ! -f "$TARGET_ROOT/$file" ]]; then
    echo "missing required file: $TARGET_ROOT/$file"
    exit 1
  fi
done

REPO_ROOT_FILE="$TARGET_ROOT/repository-links/REPO_ROOT.txt"
if [[ ! -f "$REPO_ROOT_FILE" ]]; then
  echo "missing repository root record: $REPO_ROOT_FILE"
  exit 1
fi

REPO_ROOT="$(cat "$REPO_ROOT_FILE")"
if [[ ! -d "$REPO_ROOT" ]]; then
  echo "recorded repository root does not exist: $REPO_ROOT"
  exit 1
fi

CLI_ENTRY="$REPO_ROOT/tools/cli.py"
if [[ ! -f "$CLI_ENTRY" ]]; then
  echo "missing CLI entrypoint: $CLI_ENTRY"
  exit 1
fi

echo "running read-only smoke checks from repository root: $REPO_ROOT"
(
  cd "$REPO_ROOT"
  PYTHONPATH="$REPO_ROOT" python3 tools/cli.py --smoke-ui >/dev/null
  PYTHONPATH="$REPO_ROOT" python3 tools/cli.py --no-ui help >/dev/null
  PYTHONPATH="$REPO_ROOT" python3 tools/cli.py --no-ui status >/dev/null
)

echo "post-install validation passed for: $TARGET_ROOT"
