# Contributing to ROS2-Agent

Thank you for contributing to ROS2-Agent.

ROS2-Agent is a repository-built expert platform for Ubuntu 22.04 + ROS2 Humble simulation development, diagnostics, validation, teaching, and workflow automation. Contributions should strengthen real engineering usefulness.

## Contribution priorities
- ROS2 Humble diagnostic tools with structured outputs
- reproducible broken-case fixtures for real ROS2 failures
- benchmark tasks and scoring improvements
- GitHub-ready onboarding and validation workflows
- educational assets that improve teaching and debugging quality
- simulation-safe automation patterns

## Development principles
1. Prefer structured facts over vague prose.
2. Every new capability should have tests, fixture coverage, validation integration, or benchmark coverage.
3. Keep all repository artifacts inside this workspace.
4. Do not add random one-off files at the repository root.
5. Preserve Ubuntu 22.04 + ROS2 Humble as the primary compatibility target unless policy docs expand it.

## Local setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install
```

## Validation before PR
```bash
PYTHONPATH=. python3 scripts/validation/validate_repo.py
PYTHONPATH=. python3 -m pytest tests/tools tests/workflows -q
bash scripts/validation/run_full_quality_gate.sh
pre-commit run --all-files
```

## Pull request expectations
- explain the engineering problem being solved
- list affected files and workflows
- include tests or explain why tests are not applicable
- describe validation actually run
- avoid scope creep
- update docs when behavior or platform positioning changes
- update benchmark/reporting assets when diagnosis capability changes
