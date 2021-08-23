#! /bin/bash

LISTNAME=$1
PW=""

while read LINE
do
  PW=$(egauge-get-info $LINE | grep "Password:")
  PW=$(echo $PW | sed 's/Temp:.*//')
  PW=${PW:15}
  echo $PW $LINE
done < $LISTNAME
