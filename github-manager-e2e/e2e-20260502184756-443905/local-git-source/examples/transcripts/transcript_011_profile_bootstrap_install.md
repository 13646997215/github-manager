# Transcript 011 — Profile Bootstrap Install

## User intent
Install the ROS2-Agent profile scaffold and verify the repository-backed install contract.

## Commands
```bash
bash profile/ros2-agent/bootstrap/install_profile.sh /tmp/ros2-agent-profile-demo
ls /tmp/ros2-agent-profile-demo
cat /tmp/ros2-agent-profile-demo/INSTALL_MANIFEST.md
```

## Expected outcome
- Profile files exist in the target directory.
- INSTALL_MANIFEST.md clearly points back to the repository assets.
- The install story is transparent and verifiable for GitHub users.
