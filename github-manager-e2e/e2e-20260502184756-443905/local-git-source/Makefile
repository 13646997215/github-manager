PYTHONPATH_ENV=PYTHONPATH=.

.PHONY: test validate quality report report-md precommit

test:
	$(PYTHONPATH_ENV) python3 -m pytest tests/tools tests/workflows -q

validate:
	$(PYTHONPATH_ENV) python3 scripts/validation/validate_repo.py

quality:
	bash scripts/validation/run_full_quality_gate.sh

report:
	python3 scripts/validation/generate_benchmark_report.py

report-md:
	python3 scripts/validation/render_markdown_report.py

precommit:
	pre-commit run --all-files
