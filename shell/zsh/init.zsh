# init.zsh

source "${0:A:h}/aliases.zsh"
[[ -f "${0:A:h}/aliases.local.zsh" ]] && source "${0:A:h}/aliases.local.zsh"
# source "${0:A:h}/env.zsh"
source "${0:A:h}/themes/simple-ex.zsh-theme"