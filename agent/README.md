# agent

Instructions for AI coding agents. The definitions are plain Markdown and do not depend on one agent;
each agent is connected to them by a link or a generated file.

| file | role |
|---|---|
| `global.md` | global rules for every project |
| `joint-ops-lite.md` | reply style: terse, no softening, authority by domain; persona and language set in one place each. The frontmatter is read by Claude Code and stripped for other agents |
| `claude/hooks/claude-notify.sh` | Claude Code only: desktop notification when a long turn ends or a permission prompt appears |
| `templates/AGENTS.md`, `templates/CLAUDE.md` | per-project instructions skeleton |

`global.md` and `joint-ops-lite.md` hold personal preferences, not a general standard.

Layering: global rules (here) → project `AGENTS.md` (what this repo is, how to run and check it) →
the code. Keep each layer to what the next one cannot tell the agent.

## Connect an agent

Before replacing an existing file, show it to the user and ask.

### Claude Code

Rules as the user memory file, style as an output style (kept separate: an output style sits higher in
the system prompt than memory).

```bash
mkdir -p ~/.claude/output-styles
ln -sfn ~/repo/dev-kit/agent/global.md ~/.claude/CLAUDE.md
ln -sfn ~/repo/dev-kit/agent/joint-ops-lite.md ~/.claude/output-styles/joint-ops-lite.md
```

Select the style with `/output-style joint-ops-lite`, or make it the default with
`"outputStyle": "joint-ops-lite"` in `~/.claude/settings.json` (ask the user first). A project's own
`outputStyle` takes precedence. `keep-coding-instructions: true` in the frontmatter keeps Claude Code's
built-in engineering instructions; without it a custom style drops them.

### Agents with one global instruction file

Generate the file from both definitions. It is a copy, so regenerate after `git pull`
(`bin/doctor` reports when it is stale).

```bash
sh ~/repo/dev-kit/bin/agent-instructions > ~/.codex/AGENTS.md      # Codex CLI
sh ~/repo/dev-kit/bin/agent-instructions > ~/.gemini/GEMINI.md     # Gemini CLI
```

For any other agent, put the same output wherever it reads user-level instructions.

### Notify hook (Claude Code)

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
