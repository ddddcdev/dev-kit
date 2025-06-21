# Poetryセットアップ(WSL Ubuntu)

## 必要なパッケージをインストール
```
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl git
```

## pyenvをインストール
```
curl https://pyenv.run | bash
```
~/.bashrc または ~/.zshrc に以下を追記し、反映
```
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
source ~/.zshrc  # または source ~/.bashrc
```

## poetryをインストール
```
sudo apt install pipx
pipx ensurepath
pipx install poetry
```

## poetryプラグインを追加
```
poetry self add poetry-plugin-shell
poetry self add poetry-dotenv-plugin
poetry self add poetry-plugin-export
```

## Pythonをインストールし、ローカルで有効化
```
pyenv install 3.13 # 任意のバージョン
pyenv local 3.13
```

## 仮想環境をプロジェクト内に作成
```
poetry config virtualenvs.in-project true --local
poetry install
```

