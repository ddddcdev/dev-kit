# dev-kit — instructions for AI agents

You are setting up or maintaining a developer machine with this repo. Read this file fully first.

## Ground rules

- Start with an inventory: run `sh bin/doctor`, show the result, and plan only the missing items.
  The machine may already be partly set up; keep what works.
- Every step is idempotent: check first, change only what is missing, re-run safely.
- Ask before anything outside the home directory: `sudo`, `apt` / `brew`, `chsh`, Windows-side settings.
- Do not store credentials or tokens for this repo. It is cloned read-only over HTTPS.
- Never overwrite an existing user file. If `~/.zshrc`, an agent's global instruction file, a git setting or a hook
  already holds something else, show it to the user and ask before replacing it. Back up as
  `<file>.bak-YYYYMMDD` when replacing.
- Link, do not copy, for live files (`init.zsh`, `agent/global.md`, `agent/joint-ops-lite.md`, hook scripts), so that
  `git pull` here updates the machine.
- Detect the platform once and use the matching commands in each `setup.md`:
  `uname -s` → `Darwin` = macOS; `Linux` with `microsoft` in `/proc/version` = WSL.
- Do not install GUI items (fonts, terminal colors, VS Code settings). List them for the user at the end.
- Finish with `sh bin/doctor` and report its output as is.

## Setup order

Assume the repo is at `~/repo/dev-kit`. If it is elsewhere, ask the user to move it or use their path
consistently.

1. **Base tools** — `git`, `zsh`, `curl`, `jq`, `python3` (3.11+), `uv`, `tree`, `fzf`.
   macOS: Homebrew. WSL: `apt` for the system packages, the official installer for `uv`
   (`curl -LsSf https://astral.sh/uv/install.sh | sh`).
2. **zsh** — [shell/zsh/setup.md](shell/zsh/setup.md). Ends with `init.zsh` sourced from `~/.zshrc`.
3. **git** — [git/setup.md](git/setup.md): global settings, then `sh git/hooks/install.sh`.
   Do not set `user.name` / `user.email` without asking; which identity to use is the user's call.
   Do not create a visibility policy unless the user provides one.
4. **Agent** — [agent/README.md](agent/README.md): connect the global rules and the reply style to each
   agent the user runs (ask which), and install the notify hook for Claude Code.
5. **Verify** — `sh bin/doctor`. Fix every `NG` line or report why it cannot be fixed.
6. **Hand-off** — tell the user what to apply by hand: [themes](themes/setup.md),
   [VS Code](vscode/setup.md), [bookmarklets](bookmarklet/setup.md).

## Updating a machine

```bash
git -C ~/repo/dev-kit pull --ff-only
sh ~/repo/dev-kit/bin/doctor
```

Open a new shell afterwards (or `exec zsh`) so alias and function changes load.

## Starting a new project

- Python: [python/README.md](python/README.md) — copy `python/template/`, then follow its checklist.
- Web UI: [web/README.md](web/README.md) — copy `web/template/`, then follow its steps.
- Docs-style HTML from Markdown: [docs-theme/README.md](docs-theme/README.md) — copy `docs-theme/template/`.
- Rust: [rust/README.md](rust/README.md) — write the listed files; start on the latest stable toolchain.
- Any language: copy `agent/templates/AGENTS.md` and `agent/templates/CLAUDE.md` into the repo root
  and fill in the placeholders.

## Changing this repo

- Keep it generic: no employer, customer, host or account names, no secrets.
- A change to `shell/`, `git/hooks/` or `agent/` reaches every linked machine on the next pull.
  Test on the current machine before committing; say so if the other platform is untested.
- Run `python3 -m unittest discover -s git/hooks/tests` and `sh bin/doctor` before committing.
