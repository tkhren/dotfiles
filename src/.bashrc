# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# if you need more options, see $man bash

#=============================================================================
# Shell Script Functions
#=============================================================================
tco() {  # {{{
    # Terminal Color
    ## echo $(tco RED)Hello$(tco)
    ## echo $(tco RED Hello)
    ## PS1="$(tco -e RED \u@\h)"

    local output=
    local i=0 c= opt_e=
    local colors=(black red green yellow blue magenta cyan white \
                  BLACK RED GREEN YELLOW BLUE MAGENTA CYAN WHITE)  # Bolded

    [[ $1 = "-e" ]] && opt_e=1 && shift

    if $($(which tput) setaf 1 >& /dev/null); then
        for c in ${colors[@]}; do
            if [[ $1 == $c ]]; then
                [[ $i -gt 7 ]] && output+="\[$(tput bold)\]"
                output+="\[$(tput setaf $((i % 8)))\]"
                shift
                break
            fi
            ((i++))
        done
        if [[ ( $# -ne 0 ) || ( $i -eq ${#colors[@]} ) ]]; then
            output+="$@\[$(tput sgr0)\]"
        fi
        if [[ -z $opt_e ]]; then
            output="$(sed -E 's/\\\[|\\\]//g' <<< "$output")"
        fi
        echo -n "$output"
    else
        shift
        echo -n "$@"
    fi
}  # }}}

dump() {  # {{{
    #> dump YELLOW "some messages"
    echo "$(tco $@)" 1>&2 
} # }}}

include() {  # {{{
    if [[ -f $1 ]]; then
        . "$1" && dump CYAN "(include): $1"
        return 0
    else
        dump RED "(include) Not found: $1"
        return 1
    fi
}  # }}}

getcmd() {  # {{{
    for cmd in "$@";do
        if $(which -s "$cmd");then
            echo "$cmd"
            return 0
        fi
    done
    return 1
}  # }}}

remove_path() {  # {{{
    local path="$1" p=
    for p in $(sed 's/:/ /g' <<< "$PATH"); do
        if [[ $p = $path ]]; then
            PATH="$(echo ":$PATH:" | sed "s/:$path:/:/g" | sed 's/:\+/:/g' | sed 's/^:\|:$//g')"
        fi
    done
}  # }}}

append_path() {  # {{{
    local path="$1" incd= p=

    if [[ ! -d $path ]]; then
        dump RED "(append_path) Not found: $path"
        return 1
    fi

    for p in $(sed 's/:/ /g' <<< "$PATH"); do
        [[ $p = $path ]] && incd=1 && break
    done

    if [[ -z $incd ]]; then
        PATH="$(echo "$PATH:$path" | sed 's/:\+/:/g' | sed 's/^:\|:$//g')"
    fi
}  # }}}

prepend_path() {  # {{{
    local path="$1" incd= p=
    if [[ -d $path ]]; then
        dump RED "(prepend_path): Not found: $path"
        return 1
    fi

    for p in $(sed 's/:/ /g' <<< "$PATH"); do
        [[ $p = $path ]] && incd=1 && break
    done

    if [[ -z $incd ]]; then
        PATH="$(echo "$path:$PATH" | sed 's/:\+/:/g' | sed 's/^:\|:$//g')"
    fi
}  # }}}

export_if() {  # {{{
    local opt=$1 name=$2 var="$3"
    if [[ -n $var ]] && [ $opt "$var" ]; then
        export $name=$var
        return 0
    else
        dump RED "(export_if) Failed: $name=$var"
        return 1
    fi
}  # }}}

mcd() {  # {{{
    [[ -e $1 ]] || mkdir -p "$1";
    cd "$1"
}  # }}}

bm() {  # {{{
    # Bookmark directory
    #
    # $ cd /PATH/TO/DIR
    # $ bm -a ALIAS
    # $ bm
    # ALIAS    /PATH/TO/DIR
    #
    # change directory
    # $ bm ALIAS
    # $ echo $(bm ALIAS)

    local helpmsg=$(cat << EOS
Usage: bm [-a NAME] [-d NAME] [NAME]

Jump to the NAME bookmark directory.
The bookmark list are saved in \$BASH_BOOKMARKS

-a NAME     Add a bookmark of current directory as NAME
-d NAME     Delete the NAME bookmark
EOS
)
    local opt_a= opt_d=
    local name= name_a= name_d=
    local optind_old=$OPTIND

    export BASH_BOOKMARKS=${BASH_BOOKMARKS:-~/.bash_bookmarks}

    OPTIND=1
    while getopts a:d: OPT; do
        case $OPT in
            a ) opt_a="1"
                name_a="$OPTARG" ;;
            d ) opt_d="1"
                name_d="$OPTARG" ;;

            * ) echo "$helpmsg" 1>&2
                return 1 ;;
        esac
    done

    shift $((OPTIND - 1))
    OPTIND=$optind_old

    if [[ -n $opt_a ]]; then
        echo -e "\n${name_a}\t\t$(pwd)" >> $BASH_BOOKMARKS
    fi
    if [[ -n $opt_d ]]; then
        cat $BASH_BOOKMARKS | grep -v "^${name_d}\\t" | tee $BASH_BOOKMARKS 1>/dev/null
    fi
    
    cat $BASH_BOOKMARKS | sort | uniq | grep -v '^\s*$' | tee $BASH_BOOKMARKS 1>/dev/null

    name=$1
    if [[ -n $name ]]; then
        path=$(cat $BASH_BOOKMARKS | grep "^${name}\\t" | head -1 | cut -f 3)
        echo "$path"
        cd "$path"
    else
        cat $BASH_BOOKMARKS
    fi

    return 0
}  # }}}

#=============================================================================
# Simplified OSTYPE
#=============================================================================
case "$(tr '[:upper:]' '[:lower:]' <<< $OSTYPE)" in
    linux*  ) OSTYPE='linux' ;;
    darwin* ) OSTYPE='darwin' ;;
    *bsd*   ) OSTYPE='bsd' ;;
    cygwin* ) OSTYPE='cygwin' ;;
    *       ) dump YELLOW "Unknown \$OSTYPE: $OSTYPE" ;;
esac


#=============================================================================
# Global Environmental Variables
#=============================================================================
[[ $OSTYPE = 'linux' ]] && {
    export XMODIFIERS="@im=fcitx"
    export GTK_IM_MODULE="fcitx"
    export QT_IM_MODULE="fcitx"
}


#=============================================================================
# Path
#=============================================================================
remove_path "."

append_path "$HOME/.bin"
append_path "$HOME/.cabal-sandbox/bin"

[[ $OSTYPE = 'darwin' ]] && {
    append_path '/Applications/Eclipse/android-sdk/platform-tools'
}


#=============================================================================
# If not running interactively, don't do anything more.
#=============================================================================
[[ -z $PS1 ]] && return


#=============================================================================
# No Core dump
#=============================================================================
ulimit -c 0


#=============================================================================
# Umask
# the default umask(022) is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
# file:-rw-r----- dir:drwxr-x---
#=============================================================================
umask 0022


#=============================================================================
# Language
#=============================================================================
export LANG='en_US.UTF-8'
export LC_ALL='en_US.UTF-8'


#=============================================================================
# System Environmental Variables
#=============================================================================
#export INPUTRC=~/.inputrc
export PAGER=$(getcmd less more)
export EDITOR=$(getcmd vim vi emacs nano)

export HISTFILE=~/.bash_history
export HISTSIZE=4096 # 2**12
export HISTFILESIZE=1024 # 2**10
# export HISTCONTROL=$HISTCONTROL${HISTCONTROL+,}ignoredups
export HISTCONTROL=ignoreboth
export HISTIGNORE='pwd:exit:clear:bg:q:'

# Shell Options
shopt -s histappend histreedit
shopt -s checkwinsize
shopt -s dotglob
shopt -s extglob # ?,*,+,@,!
shopt -s cdspell
shopt -s cmdhist
shopt -s lithist
shopt -s sourcepath
shopt -s no_empty_cmd_completion


#=============================================================================
# Lesspipe
# make less more friendly for non-text input files, see lesspipe(1)
#=============================================================================
[[ -x /usr/bin/lesspipe ]] && eval "$(SHELL=/bin/sh lesspipe)"


#=============================================================================
# Prompt (PS1)
#=============================================================================
# mac)    \h:\W \u\$
# cygwin) \u@\h \w\n\$
# debian|ubuntu|suse)   \u@\h:\w\$
# redhat|fedora|centos) [\u@\h \W]\$

if [[ $(id -u) -eq 0 ]]; then
    PS1="$(tco -e RED '\u@\h'):$(tco -e blue '\w')\$ "
elif [[ -n $SSH_CLIENT ]]; then
    PS1="$(tco -e MAGENTA '\u@\h'):$(tco -e blue '\w')\$ "
else
    PS1="$(tco -e GREEN '\u@\h'):$(tco -e blue '\w')\$ "
fi


#=============================================================================
# Check Chroot (only Debian)
#=============================================================================
if [[ ( -z $debian_chroot ) && ( -r /etc/debian_chroot ) ]]; then
    debian_chroot=$(cat /etc/debian_chroot)
    PS1="${debian_chroot:+($debian_chroot)}$PS1"
fi


#=============================================================================
# Directory Colors Setting
#=============================================================================
if [[ ( -z $LS_COLORS ) && $(which -s dircolors) ]]; then
    if [[ -f ~/.dircolorsrc ]]; then
        eval $(dircolors ~/.dircolorsrc)
    else
        eval $(dircolors -b)
    fi
fi


#=============================================================================
# Completion
#=============================================================================
if [[ $OSTYPE = 'darwin' ]]; then
    include "$(brew --prefix)/etc/bash_completion"
else
    include "/etc/bash_completion"
fi


#=============================================================================
# Aliases
#=============================================================================
include "$HOME/.bash_aliases" || {

    # LS
    alias sl='ls'         # for typo
    alias sls='ls'        # for typo
    if $(ls --color=auto 1>/dev/null 2>&1); then
        # GNU
        alias ls='ls --color=auto'
        alias ll='ls -lhF'
        alias la='ls -AF'
        alias lx='ls -lAXhF'  # show the detail
        alias lT='ls -lAtF'   # sorted by modified time
        alias lS='ls -lSF'    # sorted by file size
        alias recent='ls -lAt --color=always |head'
        alias bigger='ls -lAS --color=always |head'
    else
        # BSD
        alias ls='ls -G'
        alias ll='ls -lFh'
        alias la='ls -AF'
        alias lx='ls -lAFh'   # show the detail
        alias lT='ls -lAtF'   # sorted by modified time
        alias lS='ls -lSF'    # sorted by file size
        alias recent='ls -lAt --color=always |head'
        alias bigger='ls -lAS --color=always |head'
    fi

    alias fc='ls -U1F | grep -v / | wc -l'  # file count

    alias ..='cd ..'
    alias cd..='cd ..'
    alias td='cd - 1>/dev/null 2>&1'

    # File Operations
    alias rm='rm -iv'
    alias cp='cp -iv'
    alias mv='mv -iv'
    alias rmdir='rm -rfIv'
    alias mkdir='mkdir -p -v'

    # Grep Search
    export GREP_OPTIONS='-D skip --color=auto --binary-files=without-match'
    alias grepi='grep -i'
    alias egrepi='egrep -i'
    alias fgrepi='fgrep -i'

    # Process Operations
    alias f='fg'
    alias q='exit'

    # Others
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

    alias py='python -t'
    alias py3='python3 -t'
    alias ipy='ipython'
}


#=============================================================================
# Python
#=============================================================================
# export_if -f PYTHONSTARTUP "$HOME/.pythonrc"
# export_if -d PYTHONPATH "$HOME/.python2"
export PYENV_VIRTUALENV_DISABLE_PROMPT=0
export_if -d PYENV_ROOT "$HOME/.pyenv"
prepend_path "$PYENV_ROOT/bin"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# vim: ft=sh fenc=utf-8 ff=unix fdm=marker
