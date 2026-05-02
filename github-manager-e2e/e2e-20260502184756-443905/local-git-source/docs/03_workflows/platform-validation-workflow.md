# Platform Validation Workflow

## Current validation layers

1. repository asset validation
2. tool tests
3. workflow tests
4. script-level smoke execution

## Current commands

```bash
python3 scripts/validation/validate_repo.py
python3 -m pytest tests/tools tests/workflows -q
bash scripts/validation/run_phase2_validation.sh
```

## Goal
Turn validation into a repeatable platform quality gate before every major milestone.
