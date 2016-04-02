#!/bin/bash
# lame
#   -V 0      VBR (210 ~ 250kbps) extreme
#   -V 1      VBR (190 ~ 230kbps)
#   -V 2      VBR (170 ~ 210kbps)
#   -V 3      VBR (155 ~ 175kbps)
#   -V 4      VBR (145 ~ 165kbps) recommended
#   -V 5      VBR (120 ~ 140kbps)
#
#   -b 320    CBR 320kbps
#   -b 192    CBR 192kbps
#   -b 128    CBR 128kbps
#   -b xxx    CBR xxx <= 32,40,48,56,64,80,96,112,128,160,192,224,256,320

#LAME_OPTION="--cbr -b 192"
LAME_OPTION="--vbr-new -V 5"

if [ -f "$1" ]; then
    # If the given argument is a regular file,

    inf="$1"
    ouf="$(basename "$inf" ".flac").mp3"
    flac -c -d "$inf" | lame $LAME_OPTION -m j - "$ouf"

elif [ -d "$1" ]; then
    # If the given argument is a directory,

    cd "$1"
    cur_dir="$(pwd)"
#    save_dir="$cur_dir/flac2mp3"
    save_dir="$(echo $cur_dir | sed -e 's/\/Music\//\/Music\/MP3\//')"

    if [ ! -d "$save_dir" ];then
        mkdir -p "$save_dir"
    fi

    for inf in *.flac
    do
        if [ "$inf" == "*.flac" ];then
            continue
        fi
        ouf="${save_dir}/$(basename "$inf" ".flac").mp3"
        flac -c -d "$inf" | lame $LAME_OPTION -m j - "$ouf"
        mv "$ouf" "$save_dir"
    done
fi


