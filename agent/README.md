# agent

Standard instructions and hooks for AI coding agents (Claude Code first; the rule files are plain
Markdown and work as `AGENTS.md` for other agents too).

| file | role | installed as |
|---|---|---|
| `claude/CLAUDE.md` | global rules for every project | symlink `~/.claude/CLAUDE.md` |
| `claude/output-styles/joint-ops-lite.md` | reply register (terse, no softening; persona and language set in one place each) | symlink in `~/.claude/output-styles/` |
| `claude/hooks/claude-notify.sh` | desktop notification when a long turn ends or a permission prompt appears | hook command in `~/.claude/settings.json` |
| `templates/AGENTS.md` | per-project instructions skeleton | copied into a new repo and filled in |
| `templates/CLAUDE.md` | points Claude Code at `AGENTS.md` | copied into a new repo |

`claude/CLAUDE.md` and `claude/output-styles/` hold personal preferences, not a general standard.

Layering: global rules (here) → project `AGENTS.md` (what this repo is, how to run and check it) →
the code. Keep each layer to what the next one cannot tell the agent.

## Install

### Global rules

```bash
ls -l ~/.claude/CLAUDE.md 2>/dev/null   # existing file: show it to the user before replacing
mkdir -p ~/.claude
ln -sfn ~/repo/dev-kit/agent/claude/CLAUDE.md ~/.claude/CLAUDE.md
```

Do not edit the linked file for one machine: every machine reads it. Machine- or project-specific
rules go in that project's `CLAUDE.md` / `AGENTS.md`.

### Output style

```bash
mkdir -p ~/.claude/output-styles
ln -sfn ~/repo/dev-kit/agent/claude/output-styles/joint-ops-lite.md ~/.claude/output-styles/joint-ops-lite.md
```

Select it with `/output-style joint-ops-lite`, or make it the default by setting
`"outputStyle": "joint-ops-lite"` in `~/.claude/settings.json` (ask the user first). A project's own
`outputStyle` setting takes precedence.

### Notify hook

Needs `jq`. Notification backend per platform: WSL → Windows toast via `powershell.exe`;
macOS → iTerm2 (OSC 9), else `terminal-notifier`, else `osascript`; Linux → `notify-send`.
Only turns longer than `CLAUDE_NOTIFY_THRESHOLD` seconds (default 30) notify on completion.

Merge into `~/.claude/settings.json` (keep the existing keys; if a `hooks` block exists, add to it):

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [{ "type": "command", "command": "~/repo/dev-kit/agent/claude/hooks/claude-notify.sh start" }] }
    ],
    "Stop": [
      { "hooks": [{ "type": "command", "command": "~/repo/dev-kit/agent/claude/hooks/claude-notify.sh done" }] }
    ],
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [{ "type": "command", "command": "~/repo/dev-kit/agent/claude/hooks/claude-notify.sh input" }]
      }
    ]
  }
}
```

Check: `echo '{"session_id":"t","cwd":"'"$PWD"'"}' | ~/repo/dev-kit/agent/claude/hooks/claude-notify.sh input`
shows a notification.

## Writing a project AGENTS.md

Write for an agent that has never seen the repo and will run commands, not read prose:

- First lines: what the tool does and the one command to check everything (`make check`).
- Exact commands, copy-pasteable, with the wrapper variable if the CLI is called from elsewhere
  (`TOOL="uv run --no-env-file --project ~/repo/<name> <cli>"`).
- Exit codes and `--json` fields the agent should branch on.
- Rules that are not visible in the code: where output must (not) go, what must never be committed,
  what needs the user's approval.
- Fix-in-this-order tables for recurring problems: cheapest layer first, code change last.
- Nothing the code or `--help` already says.
