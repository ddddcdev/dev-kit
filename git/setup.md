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