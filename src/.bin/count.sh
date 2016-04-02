#!/bin/bash

count() {  # {{{
    # ファイル・ディレクトリ数をカウントする
    local helpmsg="Usage: count [-afdVR] DIR"
    local fnum= dnum=
    local path=$(pwd)
    local opt_a= opt_f= opt_d= opt_v= opt_r=
    local opt_ls="-p" arg_grep=
    local optind_old=$OPTIND

    OPTIND=1
    while getopts :afdVR OPT; do
        case $OPT in
            a ) opt_a="1" ;;  # include hidden files (.*)
            f ) opt_f="1" ;;  # filter file
            d ) opt_d="1" ;;  # filter directory
            V ) opt_v="1" ;;  # verbose
            R ) opt_r="1" ;;  # recursive
            * ) echo "$helpmsg" 1>&2
                return 1 ;;
        esac
    done

    shift $((OPTIND - 1))
    OPTIND=$optind_old

    [ -n "$1" ] && path="$1"
    [ ! -d "$path" ] && echo "** `$path` was NOT found.\n$helpmsg" 1>&2 && return 1
    [ -z "$opt_f" -a -z "$opt_d" ] && opt_f="1" && opt_d="1"
    [ -n "$opt_a" ] && opt_ls="$opt_ls"A
    [ -n "$opt_r" ] && opt_ls="$opt_ls"lR || opt_ls="$opt_ls"1

    if [ -n "$opt_f" ]; then
        [ -n "$opt_r" ] && arg_grep="-c ^-" || arg_grep="-cv /$"
        fnum=$(ls $opt_ls "$path" | grep $arg_grep)
        [ -z "$opt_v" ] && echo -n "File: "
        echo "$fnum"
    fi

    if [ -n "$opt_d" ]; then
        dnum=$(ls $opt_ls "$path" | grep -c /$)
        [ -z "$opt_v" ] && echo -n "Directory: "
        echo "$dnum"
    fi

    return 0
}  # }}}

count $@
