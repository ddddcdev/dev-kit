#!/usr/bin/env bash
# Claude Code hook: desktop notification on turn completion / permission prompt.
# Usage: claude-notify.sh {start|done|input}   (hook JSON on stdin)
# Platforms: WSL (Windows toast via powershell.exe), macOS (iTerm2 OSC 9 > terminal-notifier > osascript), Linux (notify-send).
set -u
MODE="${1:-}"
THRESHOLD_SEC="${CLAUDE_NOTIFY_THRESHOLD:-30}"
STATE_DIR="$HOME/.claude/hooks/state"
mkdir -p "$STATE_DIR"

INPUT="$(cat)"
SESSION="$(printf '%s' "$INPUT" | jq -r '.session_id // "unknown"')"
CWD="$(printf '%s' "$INPUT" | jq -r '.cwd // ""')"
PROJECT="$(basename "${CWD:-$PWD}")"
STAMP="$STATE_DIR/$SESSION.start"

platform() {
  case "$(uname -s)" in
    Darwin) echo mac ;;
    Linux)  if grep -qi microsoft /proc/version 2>/dev/null; then echo wsl; else echo linux; fi ;;
    *)      echo other ;;
  esac
}

toast_wsl() {
  local title="${1//\'/\'\'}" body="${2//\'/\'\'}"
  powershell.exe -NoProfile -NonInteractive -Command "
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
    \$t = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
    \$x = \$t.GetElementsByTagName('text')
    \$x.Item(0).AppendChild(\$t.CreateTextNode('$title')) | Out-Null
    \$x.Item(1).AppendChild(\$t.CreateTextNode('$body')) | Out-Null
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Claude Code').Show([Windows.UI.Notifications.ToastNotification]::new(\$t))
  " >/dev/null 2>&1
}

toast_iterm() {
  # iTerm2 posts OSC 9 as its own notification (uses iTerm's notification permission).
  # Hooks run without a tty, so walk up the process tree to find Claude's tty.
  local pid=$$ tty
  while [[ -n "$pid" && "$pid" != 1 ]]; do
    tty="$(ps -o tty= -p "$pid" 2>/dev/null | tr -d ' ')"
    if [[ -n "$tty" && "$tty" != "??" && -w "/dev/$tty" ]]; then
      printf '\033]9;%s: %s\007' "$1" "$2" > "/dev/$tty"
      return 0
    fi
    pid="$(ps -o ppid= -p "$pid" 2>/dev/null | tr -d ' ')"
  done
  return 1
}

toast_mac() {
  local title="${1//\"/\\\"}" body="${2//\"/\\\"}"
  if command -v terminal-notifier >/dev/null 2>&1; then
    terminal-notifier -title "$title" -message "$body" -sound default >/dev/null 2>&1
  else
    osascript -e "display notification \"$body\" with title \"$title\" sound name \"Glass\"" >/dev/null 2>&1
  fi
}

toast_linux() {
  command -v notify-send >/dev/null 2>&1 && notify-send "$1" "$2" >/dev/null 2>&1
}

toast() {
  local title="$1" body="$2"
  # iTerm path runs synchronously: the tty lookup needs this process's parents alive.
  if [[ "$(platform)" == mac && ( "${TERM_PROGRAM:-}" == "iTerm.app" || "${LC_TERMINAL:-}" == "iTerm2" ) ]]; then
    toast_iterm "$title" "$body" && return
  fi
  ( case "$(platform)" in
      wsl)   toast_wsl "$title" "$body" ;;
      mac)   toast_mac "$title" "$body" ;;
      linux) toast_linux "$title" "$body" ;;
    esac ) &
}

case "$MODE" in
  start)
    date +%s > "$STAMP"
    ;;
  done)
    now=$(date +%s)
    if [[ -f "$STAMP" ]]; then
      elapsed=$(( now - $(cat "$STAMP") ))
      rm -f "$STAMP"
    else
      elapsed=0
    fi
    if (( elapsed >= THRESHOLD_SEC )); then
      toast "Claude Code: done" "$PROJECT (${elapsed}s)"
    fi
    ;;
  input)
    toast "Claude Code: needs input" "$PROJECT"
    ;;
  *)
    echo "usage: $0 {start|done|input}" >&2; exit 1 ;;
esac
# Clean stale stamps (>1 day).
find "$STATE_DIR" -name '*.start' -mtime +1 -delete 2>/dev/null || true
exit 0
