#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROFILE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$PROFILE_DIR/../.." && pwd)"
TARGET_ROOT="${1:-$HOME/.hermes/profiles/ros2-agent}"

mkdir -p "$TARGET_ROOT"
mkdir -p "$TARGET_ROOT/docs"
mkdir -p "$TARGET_ROOT/repository-links"

cp "$PROFILE_DIR/SOUL.md" "$TARGET_ROOT/SOUL.md"
cp "$PROFILE_DIR/AGENTS.md" "$TARGET_ROOT/AGENTS.md"
cp "$PROFILE_DIR/config.template.yaml" "$TARGET_ROOT/config.yaml"
cp "$PROFILE_DIR/env.template" "$TARGET_ROOT/.env.template"
cp "$PROFILE_DIR/CAPABILITIES.md" "$TARGET_ROOT/CAPABILITIES.md"

python3 -m scripts.skills.export_skill_manifest >/dev/null
cp "$REPO_ROOT/profile/ros2-agent/skill_manifest.json" "$TARGET_ROOT/skill_manifest.json"

cat > "$TARGET_ROOT/README.md" <<EOF
# Installed ROS2-Agent Hermes Profile

This profile was installed from the ROS2-Agent repository.

Repository root:
$REPO_ROOT

Key installed files:
- SOUL.md
- AGENTS.md
- config.yaml
- .env.template
- CAPABILITIES.md
- skill_manifest.json
- INSTALL_MANIFEST.md

Repository-backed entrypoints:
- $REPO_ROOT/README.md
- $REPO_ROOT/docs/00_overview/quickstart.md
- $REPO_ROOT/docs/00_overview/developer-setup.md
- $REPO_ROOT/profile/ros2-agent/bootstrap/README.md
EOF

cat > "$TARGET_ROOT/INSTALL_MANIFEST.md" <<EOF
# ROS2-Agent Install Manifest

Installed profile path:
$TARGET_ROOT

Installed from repository:
$REPO_ROOT

Copied files:
- $TARGET_ROOT/SOUL.md
- $TARGET_ROOT/AGENTS.md
- $TARGET_ROOT/config.yaml
- $TARGET_ROOT/.env.template
- $TARGET_ROOT/CAPABILITIES.md
- $TARGET_ROOT/skill_manifest.json
- $TARGET_ROOT/README.md

Repository-backed assets to use together with this profile:
- $REPO_ROOT/skills/
- $REPO_ROOT/tools/
- $REPO_ROOT/examples/
- $REPO_ROOT/benchmarks/
- $REPO_ROOT/scripts/validation/

Recommended verification commands:
1. Review config and env template
2. Run repository validation from the repo root:
   PYTHONPATH=. python3 scripts/validation/validate_repo.py
3. Run layered TUI / CLI validation:
   PYTHONPATH=. bash scripts/validation/run_tui_layered_validation.sh
4. Run broader repository tests:
   PYTHONPATH=. python3 -m pytest tests/tools tests/workflows -q
5. Run post-install validation:
   bash profile/ros2-agent/bootstrap/post_install_validate.sh "$TARGET_ROOT"
6. Run full quality gate:
   bash scripts/validation/run_full_quality_gate.sh

Hermes launch hint:
- Start Hermes with this installed profile after configuring your provider credentials.
- Use the repository docs as the authoritative workflow reference for ROS2-Agent.
EOF

printf '%s
' "$REPO_ROOT" > "$TARGET_ROOT/repository-links/REPO_ROOT.txt"

echo "ROS2-Agent profile installed to: $TARGET_ROOT"
echo "Repository root recorded as: $REPO_ROOT"
echo "Review: $TARGET_ROOT/INSTALL_MANIFEST.md"
