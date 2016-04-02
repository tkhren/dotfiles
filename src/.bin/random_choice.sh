#!/bin/bash

random_choice() {  # {{{
    # Choose file(s) randomly under the given directory
    # Alternative of shuf(1)
    local helpmsg="Usage: random_choice [-n NUM] LINES"
    local optind_old=$OPTIND

    OPTIND=1
    while getopts n: OPT; do
        case $OPT in
            n ) opt_n="$OPTARG" ;;
            * ) echo "$helpmsg" 1>&2
                return 1 ;;
        esac
    done

    shift $((OPTIND - 1))
    OPTIND=$optind_old

    [ -z "$opt_n" ] && opt_n=1
    cat - | awk 'BEGIN{srand();}{print rand()"\t"$0}' | \
        sort -k1 -n | cut -f2- | head -$opt_n
    return 0
} # }}}

random_choice $@
