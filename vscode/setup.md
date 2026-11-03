# VS Code

Optional. Day-to-day work runs through an AI agent in the terminal; the editor is for reading
diffs and occasional edits. Formatting and lint rules come from each project's `pyproject.toml`
(see [python/README.md](../python/README.md)), so the editor and the agent agree.

### Extensions
- Git
  - GitLens
  - Git Graph
  - Git History
- Markdown
  - Markdown Preview Enhanced
  - Markdown Preview Mermaid Support
  - Markdown All in One
- Code Spell Checker
- Claude Code
- GitHub Copilot
- Python
  - Python / Pylance
  - Ruff (format + lint; replaces Black, isort, Pylint)
  - Jupyter
  - Quarto
- Rainbow CSV
- Bookmarks

### Settings (JSON)
- Ctrl + Shift + P > Open User Settings (JSON)
```json
{
    "remote.autoForwardPortsSource": "hybrid",
    "editor.fontFamily": "'UDEV Gothic 35NFLG', Consolas, 'Courier New', monospace",
    "editor.fontLigatures": true,
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports.ruff": "explicit"
        }
    }
}
```

