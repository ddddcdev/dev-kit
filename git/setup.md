# Git

## Global settings

Safe to re-run. Identity is **not** set globally: set it per repo (below).

```bash
git config --global core.editor vi
git config --global merge.ff false          # merges keep the branch as a unit (--no-ff)
git config --global pull.rebase false       # pull merges; avoids the "divergent branches" prompt
git config --global init.defaultBranch main
```

## Global hooks (`git/hooks/`)

`core.hooksPath` points at `git/hooks/`, so the hooks run in every repo. Each hook forwards to the
repo-local `.git/hooks/<name>`, so existing hooks (pre-commit framework etc.) keep working.

```bash
sh ~/repo/dev-kit/git/hooks/install.sh
git config --global --get core.hooksPath    # ~/repo/dev-kit/git/hooks (absolute)
# remove
git config --global --unset core.hooksPath
```

- `pre-commit install` refuses while `core.hooksPath` is set. In a new repo:
	```bash
	GIT_CONFIG_GLOBAL=/dev/null pre-commit install     # or: ... uv run pre-commit install
	```
- Not forwarded: `reference-transaction` and other per-ref-update hooks (they would slow every repo).

### visibility-guard (pre-push)

Stops a push whose target is a public GitHub repo, according to a policy. Visibility is checked
with the unauthenticated API (200 = public, 404 = private). No token needed.

- Policy: `$VISIBILITY_GUARD_POLICY` or `~/.config/git/visibility-policy.toml`. **No policy file = no-op.**
  Owner names live only in that file, never in this repo.
- Format: `git/hooks/visibility-policy.example.toml`
	- `public = "deny"`: refuse pushes to that owner's public repos
	- `public = "confirm"`: allow only with `ALLOW_PUBLIC_PUSH=1 git push ...`
	- `on_error`: what to do when the API cannot be reached (offline, rate limit)
- ssh Host aliases (`git@github-work:...`) are resolved to their HostName with `ssh -G`.
- Needs Python 3.11+ (`tomllib`). Without Python it warns and lets the push through.

```bash
python3 -m unittest discover -s ~/repo/dev-kit/git/hooks/tests
```

## Commit identity (per repo)

Right after `git clone` / `git init`, before the first commit:

```bash
git config user.name  "<name>"
git config user.email "<id>+<account>@users.noreply.github.com"   # GitHub > Settings > Emails
```

Use the noreply address of the account that owns the repo. For a throwaway address use
`me@me.invalid` (`.invalid` is reserved and can never belong to a real account). Never invent an
address on a domain that could exist: GitHub attributes commits to whoever owns it.

## Authentication

### SSH (machines that push)

One key per GitHub account. With several accounts, give each a Host block and keep the remote URL
plain where clones are shared between environments:

```sshconfig
Host github.com
	IdentityFile ~/.ssh/id_ed25519_<account>
	IdentitiesOnly yes
```

### HTTPS, read-only (machines that only pull)

Public repos need no credentials. Clone over HTTPS and disable push:

```bash
git clone https://github.com/<owner>/<repo>.git
git -C <repo> remote set-url --push origin DISABLED
```

Do not store a token for read access to a public repo. Remove stale ones:

```bash
cat ~/.git-credentials 2>/dev/null      # plain-text tokens: delete the file if nothing uses it
```

### HTTPS with a credential helper

macOS (Keychain, one credential per repo path):

```bash
git config --global credential.https://github.com.useHttpPath true
printf "protocol=https\nhost=github.com\n" | git credential-osxkeychain erase   # forget a stored one
```

WSL (Windows Git Credential Manager, installed on the Windows side from https://aka.ms/gcm):

```bash
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"
git config --global credential.https://github.com.useHttpPath true
```

The GCM path depends on how it was installed (Git for Windows bundles it; the standalone installer
uses `C:\Program Files (x86)\Git Credential Manager\`). Check with `ls` before setting it.
