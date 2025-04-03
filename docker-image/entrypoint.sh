#!/usr/bin/env bash
set -e
count=0
echo starting
sleep 10
echo "going: ${count}"
while [ ${count} -lt 100 ] ; do
  count=$(expr ${count} + 1)
  echo "resting: ${count}"
  sleep 60
done
