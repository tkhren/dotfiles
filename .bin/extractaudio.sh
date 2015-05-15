#!/bin/bash

PROGRAM_NAME=${0##*/}

usage(){
cat << EOF
Usage:
    $PROGRAM_NAME [OPTIONS] FILE...

Example:
    $PROGRAM_NAME video.mp4
    $PROGRAM_NAME *.mp4

    --aac         output as .aac instead of .m4a if the audio codec is AAC
    -h, --help    display this message
    -r, --remove  remove the input file after the conversion  
    -d DIR, --dest=DIR
                  destination directory
    -g, --dialog  show gui dialog if an error occured
EOF
}


check_installation(){
    local command=$1
    local result=$(which $command 2>/dev/null | grep $command)
    if [ "$result" = "" ];then
        echo "command not found: $command"
        echo "please install the command, or recheck your PATH configuration."
        exit 1
    fi
}


confirm_overwrite(){
    local path="$1"
    local force="$2"
    if [ -z "$force" ] && [ -e "$path" ]; then
        read -p "\"$path\" already exists. Overwrite? [y/N] " ans
        if [ "$ans" = y -o "$ans" = Y ]; then
            return 0
        else
            return 1
        fi
    fi
    return 0
}


## check instllation of other programs
#check_installation mediainfo
check_installation ffmpeg


# parse arguments
while [ -n "$1" ]
do
    case $1 in
        --help | -h) usage ;;
        --aac) opt_aac=1 ;;
        --remove | -r) opt_remove=1 ;;
        --force | -f) opt_force=1 ;;
        
        --dest=*) opt_dest="${1#*=}" ;;
        -d) shift
            if [ -z "$1" ]; then
                echo "Error: -d option needs an argument"
                usage
                exit 1
            fi
            opt_dest="$1" ;;

        --*) echo "Error: invalid option $1"
             usage ;;
         -*) echo "Error: invalid option $1"
             usage ;;
          *) n=${#args[@]}
             args[$n]="$1" ;;
    esac
    shift
done

if [ "${#args[@]}" -eq 0 ]; then
    echo "Error: no arguments"
    usage
fi

if [ -n "$opt_dest" ]; then
    if [ -d "$opt_dest" ];then
        opt_dest=$(echo "$opt_dest" | sed -e 's/\/$//')
    else
        echo "Error: No such directory: $opt_dest"
        exit 1
    fi
fi


# extract audio from `args'
for f in "${args[@]}"
do
    #afmt=$(mediainfo --Inform=Audio\;%Format% "$f")
    afmt=$(ffmpeg -i "$f" 2>&1 | grep "Audio:" | sed -e 's/^.*Audio:\ \(\w\+\).*$/\1/')
    afmt=$(echo "$afmt" | tr [:upper:] [:lower:])

    echo "-----------------------------------------------------------"
    echo "Input: $f"
    echo "Audio Format: ${afmt:-No codec detected}"
    
    case $afmt in
        AAC|aac)
            if [ -n "$opt_aac" ]; then
                savename="${f%.*}.aac"
                if [ -n "$opt_dest" ]; then
                    savename="${opt_dest}/${savename##*/}"
                fi

                confirm_overwrite "$savename" "$opt_force" && \
                    ffmpeg -y -i "$f" -acodec copy "$savename" && \
                    echo "Output: $savename" && \
                    test -n "$opt_remove" && rm "$f" && \
                    echo "Remove: $f"
            else
                f_aac="${f%.*}.temp.aac"
                savename="${f%.*}.m4a"
                if [ -n "$opt_dest" ]; then
                    savename="${opt_dest}/${savename##*/}"
                fi

                confirm_overwrite "$savename" "$opt_force" && \
                    ffmpeg -y -i "$f" -acodec copy "$f_aac" && \
                    mv -f "$f_aac" "$savename" && \
                    echo "Output: $savename" && \
                    test -n "$opt_remove" && rm "$f" && \
                    echo "Remove: $f"
            fi
            ;;
        *)
            if [ -n "$afmt" ]; then
                echo "Not supported format: $afmt"
            fi
            ;;
    esac
done


