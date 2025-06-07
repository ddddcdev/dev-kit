#aliases.zsh

# Python関連
alias py='python'
alias py3='python3'
alias pi='pip install'
alias pu='pip uninstall'
alias pes='pipenv shell'

# 履歴確認
alias h='history'
alias hg='history | grep'

# git関連
alias gst='git status'
alias gsw='git switch'
alias ga='git add'
alias gaa='git add --all'
alias gc='git commit -m'
alias gps='git push'
alias gpl='git pull'
alias gb='git branch'
alias gco='git checkout'
alias gcm='git commit'
alias gd='git diff'
alias grs='git restore'
alias gm='git merge'

alias gwip='ga . && gc wip'
alias gchore='ga . && gc chore'
alias gfix='ga . && gc fix'
alias gup='ga . && gc update'

alias gl='git log --oneline --graph --all --decorate'


# Docker関連
alias dps='docker ps'
alias dpa='docker ps -a'
alias dcu='docker compose up'
alias dcd='docker compose down'
alias di='docker images'
alias drmi='docker rmi'
alias drmc='docker rm $(docker ps -aq)'
alias dex='docker exec -it'

# コンテナ起動
alias dcub='docker compose up --build'

# etc
alias repo='cd ~/repo && ls'