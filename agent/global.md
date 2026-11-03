# Global rules for coding agents

Applies to every project on this machine, whichever agent reads it. A project's own `AGENTS.md` /
`CLAUDE.md` overrides anything here.
These are personal working preferences, not a general standard.

## Communication

- Reply in the language the user writes in. Code, comments, log messages and commit messages: English,
  unless the project says otherwise.
- Report outcomes as they are. Failed tests are reported with their output; skipped steps are named.
- When unsure about a fact, say "unverified" instead of hedging. When a decision belongs to the user
  (scope, priority, anything irreversible or outward-facing), ask before acting.

## Git

- Never force push. On a rejected push, stop and report.
- Work on a branch (`feat/`, `fix/`, `chore/`) unless the project says main is fine. One working branch
  at a time; delete it locally and on the remote after merging.
- Merge with `--no-ff`.
- Pushing to a public repo publishes the code. Push there only when the user asked for it.
- Do not set git identity globally. Check `git config user.name` / `user.email` in a fresh clone and ask
  if they are unset.
- Never commit secrets. `.env` stays untracked; document variables in `.env.example`.

## Working files

- Temporary files (dumps, scratch scripts, intermediate output) go in `.scratch/` at the repo root, not
  `/tmp`. Add `.scratch/` to `.gitignore` if it is missing.
- If a script is likely to be needed again, make it a CLI command in a tool repo instead of a one-off.

## Verification

- Run the project's check command before saying work is done (`make check` in the Python standard).
- UI changes: verify in a headless browser (Playwright) and judge by counts from the DOM
  (expected elements, `pageerror` events), not screenshots alone. Use a real logged-in browser only
  when the screen needs the user's session. Against production, read only.

## Dependencies

- New projects start on the latest stable versions; pin them when the environment is created
  (`uv.lock`, `package-lock.json`, `Cargo.lock`).
- Ad-hoc tools also take a pinned version: `uv run --with <pkg>==<ver> ...`.
- After upgrading a dependency, check other projects in `~/repo/` that use it and say whether they
  should follow. Do not upgrade them unasked.

## Tools and design

- Python projects follow dev-kit `python/README.md` (uv, ruff, pyright, pytest, `make check`).
- Rust projects follow dev-kit `rust/README.md` (pinned toolchain, clippy, nextest, cargo-deny, `just check`).
- CLIs must be fully usable non-interactively (every input as an option, `--json` output, meaningful
  exit codes) so agents and cron can drive them. An interactive mode may exist next to it.
- Logs go to files. Key=value lines (`YYYY-MM-DDTHH:MM:SS+0900 [tag] key=value ... status`) or JSON
  lines for new projects.
- Containers: Docker Engine CLI. Not Docker Desktop.
