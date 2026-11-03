# dev-kit

Personal development environment, kept as files that the machine reads directly
(shell config, git hooks, agent instructions) plus the standards new projects start from.

Designed to be set up and maintained by an AI coding agent. A human reads this page;
the agent follows [AGENTS.md](AGENTS.md).

## Setting up a machine

Clone read-only to `~/repo/dev-kit` (the paths below assume it), then hand it to the agent:

```bash
git clone https://github.com/ddddcdev/dev-kit.git ~/repo/dev-kit
git -C ~/repo/dev-kit remote set-url --push origin DISABLED
cd ~/repo/dev-kit
claude "Set up this machine with dev-kit. Follow AGENTS.md."
```

No credentials are needed and nothing can be pushed from the clone. Update with
`git -C ~/repo/dev-kit pull --ff-only`.

Check the result at any time:

```bash
sh ~/repo/dev-kit/bin/doctor
```

Supported: macOS (zsh) and Linux / WSL2 on Windows (zsh). The same files are used on both;
only the install commands differ, and each `setup.md` lists both.

## What is in it

| dir | what | how it is used |
|---|---|---|
| [`shell/zsh/`](shell/zsh/setup.md) | aliases, `uv` wrapper, prompt theme | `~/.zshrc` sources `init.zsh` |
| [`git/`](git/setup.md) | global git settings, hook dispatcher, public-push guard | `core.hooksPath` points at `git/hooks/` |
| [`agent/`](agent/README.md) | rules for AI coding agents, Claude Code hooks, project templates | `~/.claude/CLAUDE.md` and hook scripts are symlinks into here |
| [`python/`](python/README.md) | Python project standard: uv, ruff, pyright, pytest, `make check` | templates copied into new projects |
| [`themes/`](themes/setup.md) | font and terminal / editor colors | applied by hand (GUI settings) |
| [`vscode/`](vscode/setup.md) | VS Code extensions and settings | applied by hand |
| [`bookmarklet/`](bookmarklet/setup.md) | browser bookmarklets | applied by hand |

## Personal customization

The colors, fonts, prompt theme, editor settings, bookmarklets and the agent rules and reply style in
`agent/claude/` are one person's preferences. They are not proposed as a general standard.
Fork and change them freely.

## Live files

Files under `shell/`, `git/hooks/` and `agent/` are **live**: a `git pull` here changes every
machine that links to them. Keep them working on both macOS and WSL.

## Rules for this repo

- Generic only. No employer, customer, host or account names, no secrets, no machine-specific paths
  other than `~/repo/dev-kit`. Machine-local additions go in gitignored `*.local.*` files.
- Docs, comments and commit messages in English.
- Tests: `python3 -m unittest discover -s git/hooks/tests` and `sh bin/doctor`.
