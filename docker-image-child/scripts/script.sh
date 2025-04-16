#!/bin/sh

echo starting
while [ ${count} -lt 10 ] ; do
  echo "resting: ${count}"
  sleep 10
  count=$(expr ${count} + 1)
done
