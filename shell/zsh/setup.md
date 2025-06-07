## 1. `oh-my-zsh` をインストール


```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```


## 2. pluginの追加

```pash
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

vi ~/.zshrc
```

```bash
plugins=( 
    git
    docker
    zsh-autosuggestions
)
```

```bash
source ~/.zshrc
```

## 2. `init.zsh`の読み込み設定

```bash
echo 'source ~/repo/dev-kit/shell/zsh/init.zsh' >> ~/.zshrc
source ~/.zshrc
```

- ~/repo/dev-kit/ は dev-kit リポジトリのパスに応じて適宜変更してください。