#!/bin/sh

fx_prof=`echo ~/.mozilla/firefox/*.default`
cd $fx_prof
pwd
for f in `ls *.sqlite`
do
    echo "$f"
	sqlite3 "$f" vacuum
	sqlite3 "$f" reindex
done
