# ~/.bash_aliases: called from ~/.bashrc

#==============================================================================
# Ls Commands
#==============================================================================:
alias sl='ls'         # for typo
alias sls='ls'        # for typo
if $(ls --color=auto 1>/dev/null 2>&1); then
    alias ls='ls --color=auto'
    alias ll='ls -lhF'
    alias la='ls -AF'
    alias lx='ls -lAXhF'  # show the detail
    alias lT='ls -lAtF'   # sorted by modified time
    alias lS='ls -lSF'    # sorted by file size
    alias recent='ls -lAt --color=always |head'
    alias bigger='ls -lAS --color=always |head'
else
    alias ls='ls -G'
    alias ll='ls -lFh'
    alias la='ls -AF'
    alias lx='ls -lAFh'  # show the detail
    alias lT='ls -lAtF'   # sorted by modified time
    alias lS='ls -lSF'    # sorted by file size
    alias recent='ls -lAt --color=always |head'
    alias bigger='ls -lAS --color=always |head'
fi

alias fc='ls -U1F | grep -v / | wc -l'  # file count

#==============================================================================
# Change Directory
#==============================================================================
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'
alias cd..='cd ..'
alias td='cd - 1>/dev/null 2>&1'

#==============================================================================
# File Operations
#==============================================================================
alias rm='rm -iv'
alias cp='cp -iv'
alias mv='mv -iv'
alias rmdir='rm -rfIv'
alias mkdir='mkdir -p -v'

#==============================================================================
# Grep Search
#==============================================================================
export GREP_OPTIONS='-D skip --color=auto --binary-files=without-match'
alias grepi='grep -i'
alias egrepi='egrep -i'
alias fgrepi='fgrep -i'

#==============================================================================
# Process Operations
#==============================================================================
alias f='fg'
alias q='exit'

#==============================================================================
# Others
#==============================================================================
alias vim='vim -p'
alias path='echo -e ${PATH//:/\\n}'
alias perl='perl -w'
alias df='df -kTh'
alias screen='\screen -U -D -RR'
alias hist='fc -r -l |less'
alias ps='ps aux'
alias free='free -mt'
alias psgrep='ps | grep -v grep | grep -i -e VSZ -e'
alias env='env | sort'
alias reload='exec $SHELL -l'


#==============================================================================
# Python
#==============================================================================
alias py='python -t'
alias py3='python3 -t'
alias ipy='ipython'


#==============================================================================
# Bookmarks
#==============================================================================
alias cdfx='cd ~/.mozilla/firefox/*.default'

#alias memo='cat > /dev/null'
#alias tree='tree -L 2'
#alias confcat='sed -e "s/#.*//;/^\s*$/d"'
#alias fstab='confcat /etc/fstab'
#alias dui='du --max-depth 1 -khc |sed -e "s/\.\///" |sed -e "s/4\.0K/---/"'

# vim: ft=sh
