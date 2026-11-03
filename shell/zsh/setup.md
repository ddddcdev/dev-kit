# zsh

`~/.zshrc` sources `init.zsh`, which loads:

| file | content | tracked |
|---|---|---|
| `aliases.zsh` | git / docker / python aliases, `uv` wrapper (loads `./.env` only if it exists) | yes |
| `aliases.local.zsh` | machine-only aliases | no (`*.local.zsh` is gitignored) |
| `themes/simple-ex.zsh-theme` | two-line prompt: time, path, git branch | yes |

Same files on macOS and WSL. Edit them here, never copy them into `~/.zshrc`.

## 1. zsh and oh-my-zsh

```bash
# WSL only: zsh itself, then make it the login shell
sudo apt install -y zsh
chsh -s "$(command -v zsh)"

# both
[ -d ~/.oh-my-zsh ] || sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
```

## 2. Plugins

`plugins=(...)` in `~/.zshrc` must include `git` (the theme uses `git_prompt_info`) and `docker`.

macOS (Homebrew):

```bash
brew install zsh-autosuggestions zsh-syntax-highlighting fzf
```

Add to `~/.zshrc`, after `source $ZSH/oh-my-zsh.sh`:

```zsh
source /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh
source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source <(fzf --zsh)
```

WSL (oh-my-zsh custom plugins):

```bash
C=${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins
[ -d $C/zsh-autosuggestions ] || git clone https://github.com/zsh-users/zsh-autosuggestions $C/zsh-autosuggestions
[ -d $C/zsh-syntax-highlighting ] || git clone https://github.com/zsh-users/zsh-syntax-highlighting $C/zsh-syntax-highlighting
sudo apt install -y fzf
```

```zsh
plugins=(git docker zsh-autosuggestions zsh-syntax-highlighting)
```

and after `source $ZSH/oh-my-zsh.sh`: `source <(fzf --zsh)` (fzf 0.48+; older apt packages use
`source /usr/share/doc/fzf/examples/key-bindings.zsh`).

## 3. Load dev-kit

After `source $ZSH/oh-my-zsh.sh` (the theme here overrides `ZSH_THEME`):

```bash
grep -q 'dev-kit/shell/zsh/init.zsh' ~/.zshrc || echo 'source ~/repo/dev-kit/shell/zsh/init.zsh' >> ~/.zshrc
exec zsh
```

Remove any `export UV_ENV_FILE=...` from `~/.zshrc`: the `uv` wrapper replaces it, and a global
`UV_ENV_FILE` makes `uv` fail in repos without `.env`.

## 4. Check

```bash
type uv | head -1          # "uv is a shell function"
alias gst                  # gst='git status'
echo ${UV_ENV_FILE-unset}  # unset
```

`sh ~/repo/dev-kit/bin/doctor` runs the same checks.

The `uv` wrapper only exists in interactive zsh. `make`, cron and scripts call the real `uv`
and never read `.env` implicitly.
