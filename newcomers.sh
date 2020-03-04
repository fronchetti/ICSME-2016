#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit
fi

cd $1

git log --format='%aN' | sort -u > committers.txt
cat committers.txt | while read line
do
  #echo $line
  git log --reverse  --date=short --pretty='format:%cd' -E --author="^${line}\s<(.+)>$" | head -1 >> contribs.txt
  echo "" >> contribs.txt
done
cat contribs.txt | sort -rn > ~/`basename $1`.txt
rm contribs.txt committers.txt

echo "done!"
