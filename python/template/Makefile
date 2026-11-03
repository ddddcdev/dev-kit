.PHONY: help lint format fix typecheck test check

UV := uv run --no-env-file

help:
	@echo "make check      lint + format check + typecheck + test (run before every commit)"
	@echo "make fix        ruff format + ruff check --fix"
	@echo "make lint | format | typecheck | test"

lint:
	$(UV) ruff check .
	$(UV) ruff format --check .

format:
	$(UV) ruff format .

fix:
	$(UV) ruff format .
	$(UV) ruff check --fix .

typecheck:
	$(UV) pyright

test:
	$(UV) pytest -q

check: lint typecheck test
