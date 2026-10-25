# Git

## git clone

```bash
git clone https://github.com/kojimat/dev-kit.git

git config user.name "me"
git config user.email "xxxxxxxx@users.noreply.github.com"
# GitHub > Setting > Emails
```

## GitHubのrepositoryごとに認証を保存する設定(Mac)
```bash
git config --global credential.https://github.com.useHttpPath true

# 既存の認証を削除する場合は
printf "protocol=https\nhost=github.com\n" | git credential-osxkeychain erase
```


## Install Git Credential Manager (WSL)

- GCMをダウンロード・インストール(Windows版)
  - https://aka.ms/gcm

```bash
# 現状の設定
git config --global credential.helper

# GCMを確認
/mnt/c/Program\ Files\ \(x86\)/Git\ Credential\ Manager/git-credential-manager.exe --version
# 2.6.1+786ab03440ddc82e807a97c0e540f5247e44cec6

# GCMを設定
git config --global credential.helper "/mnt/c/Program\ Files\ \(x86\)/Git\ Credential\ Manager/git-credential-manager.exe"

# GCMを確認
git config --global credential.helper
# /mnt/c/Program\ Files\ \(x86\)/Git\ Credential\ Manager/git-credential-manager.exe
```

## GitHubのrepositoryごとに認証を保存する設定(WSL)
```bash
git config --global credential.https://github.com.useHttpPath true

# 既存の認証を削除する場合は
echo -e "protocol=https\nhost=github.com" | "/mnt/c/Program Files (x86)/Git Credential Manager/git-credential-manager.exe" erase
```

## change default editor

```bash
git config --global core.editor vi
```

## hint: You have divergent branches and need to specify how to reconcile them.
```bash
git config --global pull.rebase false
```
## global hooks（`git/hooks/`）

`core.hooksPath` を `git/hooks/` に向け、全 repo で共通の hook を動かす。各 hook は repo ローカルの `.git/hooks/<name>` へ転送するので、既存の hook（pre-commit framework 等）もそのまま動く。

```bash
sh ~/repo/dev-kit/git/hooks/install.sh
# 解除
git config --global --unset core.hooksPath
```

- `pre-commit install` は `core.hooksPath` が設定されていると拒否する。新しい repo では次で入れる
	```bash
	GIT_CONFIG_GLOBAL=/dev/null pre-commit install
	```
- 転送しない hook: `reference-transaction` 等、ref 更新ごとに走るもの（置くだけで全 repo が遅くなるため）

### visibility-guard（pre-push）

push 先が public の GitHub repo のとき、policy に従って止める。visibility は認証なしの API で判定する（200 = public、404 = private 扱い）。トークン不要。

- policy: `$VISIBILITY_GUARD_POLICY` または `~/.config/git/visibility-policy.toml`。**無ければ何もしない**（具体的な owner はこの repo に置かない）
- 書式: `git/hooks/visibility-policy.example.toml`
	- `public = "deny"`: その owner の public repo への push を止める
	- `public = "confirm"`: `ALLOW_PUBLIC_PUSH=1 git push ...` のときだけ通す
	- `on_error`: API に届かないとき（offline・rate limit）の扱い
- ssh の Host alias（`git@github-work:...`）は `ssh -G` で HostName に解決して判定する
- Python 3.11+（`tomllib`）が要る。Python が無ければ警告して通す

```bash
python3 -m unittest discover -s ~/repo/dev-kit/git/hooks/tests
```
