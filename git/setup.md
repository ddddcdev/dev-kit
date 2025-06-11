# Git

## Install Git Credential Manager (GCM)

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


## change default editor
```bash
git config --global core.editor vi
```

## hint: You have divergent branches and need to specify how to reconcile them.
```bash
git config --global pull.rebase false

```