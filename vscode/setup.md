# VSCode

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
- GitHub Copilot
- Python
  - Black Formatter
  - isort
  - Pylint
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
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit"
        }
    },
    "isort.args": ["--profile", "black"]
}

