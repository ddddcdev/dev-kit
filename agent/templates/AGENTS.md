# <project> — instructions for AI agents

<One sentence: what this project does and for whom.>

Check everything: `make check` (lint, format check, type check, tests). Run it before saying work is done.

## Run

```bash
TOOL="uv run --no-env-file --project ~/repo/<project> <cli>"
$TOOL --help
```

- `<command> --json` → <fields to read>. Exit codes: 0 ok, 1 error, <2.. meanings>.

## Layout

| path | what |
|---|---|
| `src/<package>/` | <...> |
| `tests/` | pytest; markers `unit` / `integration` / `smoke` |

## Rules

- <Where output goes / never goes (e.g. user data outside the repo).>
- <What needs the user's approval (production writes, publishing, paid API calls).>
- Code, comments, commit messages, docs: English.
- Commit identity for this repo: `<name>` / `<email>` (set in the repo-local config).

## When something is wrong

| problem | fix here first | then |
|---|---|---|
| <...> | <config / data> | <command> |
| none of the above | code change + test | `make check` |
