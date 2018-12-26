#!/bin/sh
# Bash script to remove stale input files

# Ensure maxdays arg is a number
# or use default of 60 days
if [ "$1" != "" ]; then
    re=^[0-9]+$
    if ! [[ "$1" =~ "$re" ]] ; then
       echo $1
       echo "$1"
       echo "error: Not a number" >&2;
       exit 1
    fi
    maxdays=$1
else
    maxdays=60
fi

# Ensure archives directory exists
# and enter directory
archivesdir=archives
if ! [[ -d "./"$archivesdir"" ]] ; then
   echo "error: directory "$archivesdir" does not exist" >&2;
   exit 1
fi
cd ./"$archivesdir"

# For compressed archive files, check that
# files are not older than $maxdays. Remove if there
# are stale files present
echo "removing stale (>"$maxdays" days) feed file archives..."
for filename in *.tar.gz;
do
    if [[ -e "$filename" ]]
    then
        filedate=$(echo $filename | rev | cut -c 8- | rev | date -j -u -f '%Y_%m_%d_%H_%M_%S' +%s)
        curdate=$(date -u +%s)
        maxdiff=$(($maxdays * 86400))
        if [[ $(($curdate-$filedate)) -gt $maxdiff ]] ; then
            echo "removing stale file "$filename"."
            rm $filename
        fi
    else
        echo "no archive files found."
        continue
    fi
done
