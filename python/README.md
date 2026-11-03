# Python project standard

One gate for humans, agents and git hooks alike: **`make check`** (ruff lint + format check, pyright,
pytest). A project is "done" only when it passes.

## Stack

| purpose | tool |
|---|---|
| Python, venv, dependencies, lock | [uv](https://docs.astral.sh/uv/) (`uv.lock` committed) |
| lint + format | ruff (rules `E F I UP B`, line length 120) |
| type check | pyright (`standard`) |
| tests | pytest (markers `unit` / `integration` / `smoke`, `--strict-markers`) |
| CLI | Typer |
| terminal output | Rich |
| TUI (when needed) | Textual |
| gate on commit | pre-commit running `make check` |
| agent gate on edit | Claude Code `PostToolUse` hook: ruff format + `ruff check --fix` on every edited `.py`; leftover errors go back to the agent |

Not used: poetry, pyenv, pip/venv by hand, black, isort, flake8 (ruff covers them).

## Template

`template/` is a working project (`sample-app` / package `sample_app`). It passes `make check` as is.

| file | role |
|---|---|
| `pyproject.toml` | metadata, deps, ruff / pyright / pytest config |
| `.python-version` | interpreter for uv |
| `Makefile` | `check` `fix` `lint` `format` `typecheck` `test` |
| `.pre-commit-config.yaml` | runs `make check` before each commit |
| `.claude/settings.json` | format/lint hook on edit, allowed check commands |
| `.gitignore`, `.env.example` | `.env` and `.scratch/` never committed |
| `src/sample_app/cli.py` | Typer CLI with a `--json` example command |
| `tests/test_cli.py` | smoke + unit test |
| `README.md` | stub |

## New project (checklist for the agent)

```bash
NAME=my-tool; PKG=my_tool                     # kebab-case repo name, snake_case package
cp -R ~/repo/dev-kit/python/template ~/repo/$NAME
cp ~/repo/dev-kit/agent/templates/AGENTS.md ~/repo/dev-kit/agent/templates/CLAUDE.md ~/repo/$NAME/
cd ~/repo/$NAME
mv src/sample_app src/$PKG
grep -rl 'sample[-_]app' . | xargs sed -i.bak -e "s/sample-app/$NAME/g" -e "s/sample_app/$PKG/g"
find . -name '*.bak' -delete
git init
```

1. Commit identity in the repo-local config (ask the user which account owns the repo).
2. Start on the latest stable versions. The template's lower bounds are a floor, not a target:
   raise each to the current release (`curl -s https://pypi.org/pypi/<pkg>/json | jq -r .info.version`),
   also `requires-python` / `.python-version` / ruff `target-version` / pyright `pythonVersion` if a newer
   Python is out, then `uv lock --upgrade && uv sync`.
3. `make check` passes.
4. `GIT_CONFIG_GLOBAL=/dev/null uv run pre-commit install`
   (pre-commit refuses to install while a global `core.hooksPath` is set; dev-kit's dispatcher then
   forwards to `.git/hooks/pre-commit`, so the hook still runs).
5. Fill in `AGENTS.md` and `README.md`. Replace the `hello` command.
6. First commit.

## Existing project → standard

Align in this order, one commit each, `make check` green after each:

1. `uv` (`uv init --bare` next to an existing `requirements.txt` / poetry config, move deps,
   delete the old lock).
2. ruff config from the template; `make fix`; commit the reformat alone.
3. `Makefile`, `.pre-commit-config.yaml`, `.claude/settings.json`.
4. pyright: start at `basic` if `standard` floods; tighten later.
5. `AGENTS.md` + `CLAUDE.md`.

## Conventions

- `uv run --no-env-file ...` in Makefiles, hooks and agent commands: checks never read `.env`, so they
  never touch real credentials. Code that needs env loads it itself (`load_dotenv()`) or the entry point
  passes `--env-file .env` explicitly.
- In an interactive zsh, dev-kit's `uv` wrapper loads `./.env` only when it exists
  ([shell/zsh](../shell/zsh/setup.md)).
- A shared helper CLI used from several repos goes into each repo's `dev` group (git source in
  `[tool.uv.sources]`) and is called with `uv run --project <repo> <cli>`, not `uv tool install`.
  Versions then live in each `uv.lock`.
- Ad-hoc tools: `uv run --with <pkg>==<ver> python -I script.py` with a pinned version.
- Scripts and dumps for investigation: `.scratch/`.
