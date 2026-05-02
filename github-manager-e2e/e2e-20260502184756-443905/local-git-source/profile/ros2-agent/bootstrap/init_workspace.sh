#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${1:-$HOME/ros2_ws}"
mkdir -p "$WORKSPACE/src"
mkdir -p "$WORKSPACE/docs"

cat > "$WORKSPACE/README.md" <<EOF
# ROS2 Workspace Bootstrapped by ROS2-Agent

This workspace was created as a simulation-safe starter workspace.

Suggested next commands:
- source /opt/ros/humble/setup.bash
- cd $(printf '%q' "$WORKSPACE")
- colcon list || true

Repository-backed ROS2-Agent validation hints:
- Use the ROS2-Agent repository tools to audit environment and workspace state.
- Keep packages inside src/.
EOF

cat > "$WORKSPACE/.gitignore" <<'EOF'
build/
install/
log/
EOF

cat > "$WORKSPACE/docs/bootstrap_notes.md" <<EOF
# Bootstrap Notes

- Verify underlay/overlay sourcing order before build or launch.
- Prefer running workspace collector before broad modifications.
- Use ROS2-Agent runbooks for broken workflow reproduction and recovery validation.
EOF

echo "ROS2-Agent bootstrap workspace prepared at: $WORKSPACE"
echo "Created: $WORKSPACE/src"
echo "Created: $WORKSPACE/README.md"
echo "Created: $WORKSPACE/.gitignore"
echo "Created: $WORKSPACE/docs/bootstrap_notes.md"
echo "You can now run ROS2-Agent environment and workspace audit tools against this path."
