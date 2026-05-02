# README_EN

ROS2-Agent is currently a repository-backed, Hermes-aligned ROS2 engineering platform prototype.

It already includes:
- a unified command runtime shared by CLI and TUI
- Hermes-style foundation commands
- ROS2-specific collect / diagnose / inspect / doctor / suggest-fix / trace / replay / compare commands
- workflow / recovery benchmark and runbook assets
- platform-surface assets such as profile install validation, MCP readiness, and gateway demo materials
- a three-pane TUI workbench with four result views: summary / next_actions / payload / raw

Please read first:
- docs/00_overview/quickstart.md
- docs/00_overview/current-capability-boundaries.md
- docs/01_architecture/capability_contract.md
- docs/00_overview/final-platform-capability-summary.md
- docs/03_workflows/launcher-ui-workflow.md

## Direct experience
For the prepared local deployment, launch:

```bash
/home/hanhan/Desktop/.ros2-agent/ros2-agent
```

This entry uses the deployment venv and opens the advanced TUI workbench when Textual is available.

## What you can directly experience now
- left command catalog grouped into foundation / ROS2 collection / ROS2 inspection / ROS2 diagnosis / workflow-benchmark
- middle detail pane with purpose, maturity, risk level, and actual invocation
- right result pane with summary / next_actions / payload / raw views
- `/` to focus the search box and filter commands
- `R` to inspect recent command history
- `E` to inspect recent error / blocked / not_implemented entries
- `Enter` to execute the selected command
- `Tab` to switch result views
- `H` for help
- `Q` to quit

## Developer validation and dependency notes
If you are developing inside the repository rather than only using the deployed entrypoint, start with:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
PYTHONPATH=. bash scripts/validation/run_tui_layered_validation.sh
```

Layered validation behavior:
- layer 1: CLI contract tests, no Textual required
- layer 2: TUI smoke fallback, validating the no-Textual fallback path
- layer 3: Textual interaction tests, executed only when `textual` is installed; otherwise skipped by design

For the full interactive test layer, also install:
- `textual`
- `pytest-asyncio`

The repository script entry can now also be used directly:
```bash
python3 tools/cli.py --smoke-ui
python3 tools/cli.py --no-ui history
python3 tools/cli.py --no-ui quality
```

## Common commands
```bash
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui help
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui status
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui doctor
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui inspect workspace
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui collect env
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui diagnose fusion
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui suggest-fix tf
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui trace failure
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui runbook list
/home/hanhan/Desktop/.ros2-agent/ros2-agent --no-ui quality
```

## Platform boundary notes
Do not describe the current project as a production-grade field recovery platform.
A more accurate description is:
- a ROS2 engineering platform prototype with a unified command surface, structured diagnosis result layer, repo-backed evaluation assets, and a terminal workbench experience
- runtime diagnosis in real ROS2 environments is still an implemented prototype
- recovery benchmark / MCP / gateway / cron remain prototype / readiness / demo level rather than production automation

## Where to start
1. Run `/home/hanhan/Desktop/.ros2-agent/ros2-agent`
2. Start with `help`, `status`, and `doctor`
3. Then move to `inspect workspace`, `collect env`, and `diagnose fusion`
4. For scenario replay, continue with `runbook list` and `replay workflow`
