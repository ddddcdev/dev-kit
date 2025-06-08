# Git

## 🔷git clone

```bash
git clone https://github.com/kojimat/dev-kit.git

git config user.name "me"
git config user.email "xxxxxxxx@users.noreply.github.com"
# GitHub > Setting > Emails
```

## 🔷WSL環境で安全にGitトークンを保存する方法（Windows用）

---

### 補足

- WSL（Windows Subsystem for Linux）では、Windows側のGit Credential Manager（GCM）との連携が最も安全かつ推奨される。
- macOSでは`osxkeychain`が標準で利用される。

---

## 🔷WSLでのGit Credential Manager設定手順（推奨） ※未確認

1. **Windows側で「Git for Windows」をインストール**  
   - [公式ダウンロードページ](https://git-scm.com/download/win)

2. **Credential Manager Coreのパスを確認**  
   - 一般的なパス例：
     - `C:\Program Files\Git\mingw64\libexec\git-core\git-credential-manager.exe`
     - または
     - `C:\Program Files\Git Credential Manager Core\git-credential-manager-core.exe`

3. **WSLからcredential.helperにパスを設定**

    ```bash
    git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/libexec/git-core/git-credential-manager.exe"
    ```

    - 上記はパスに空白が含まれるため、`\`でエスケープすること
    - パスは環境により異なる場合があるため、確認のこと

4. **以降は最初の認証情報入力後、自動でWindows資格情報マネージャに暗号化保存される**

## 🔷GitHubのrepositoryごとに認証を保存する設定(Mac)
```bash
git config --global credential.https://github.com.useHttpPath true

# 既存の認証を削除する場合は
printf "protocol=https\nhost=github.com\n" | git credential-osxkeychain erase
```
