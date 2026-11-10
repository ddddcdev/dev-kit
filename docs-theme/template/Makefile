.PHONY: build check serve

build:
	uv run python build.py

check:
	uv run ruff check .
	uv run ruff format --check .
	uv run pyright
	uv run python build.py

serve: build
	uv run python -m http.server -d dist 8000
