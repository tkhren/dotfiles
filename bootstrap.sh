#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0);pwd)
cd "$SCRIPT_DIR"

git pull origin master;

opt=

if [ "$1" == "--force" -o "$1" == "-f" ]; then
    opt="-avh"
else
    echo ""
    echo "This is a dryrun result."
    echo "Are you sure? Please retry after adding '-f' or '--force' option to execute."
    opt="-avhn"
fi

rsync \
    --exclude "*.swp" \
    --exclude "*.bak" \
    --exclude "*~" \
    --exclude "*.pyc" \
    --exclude ".directory" \
    --exclude ".git/" \
    --exclude ".DS_Store" \
    --exclude "bootstrap.sh" \
    --exclude "README.*" \
    --exclude "LICENSE" \
    --exclude "__pycache__/" \
    --no-perms \
    $opt \
    . ~;
