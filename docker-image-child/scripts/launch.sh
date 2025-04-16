#!/bin/sh
mkdir -p /pvcs-test
chmod 777 /pvcs-test
ls -l /scripts
ls -l /pvcs
ls -l /turbo-backup
echo "=========================" 
echo  /usr/bin/python3 /scripts/$*
/usr/bin/python3 /scripts/$*
echo "========================="
ls -l /turbo-backup
echo "========================="
echo 'Restored'
ls -l /pvcs-test
# # EXTRA SLEEP FOR DEBUGGING
# count=0
# while [ $count -lt 5 ]; do
#   echo "count: $count"
#   count=$((count+1))
#   sleep 60
# done
    echo DONE