#!/bin/bash

# try for 12 mins
count=0
while [ "${actions}" == '' -a ${count} -lt 12 ] ; do
    actions=$(kubectl logs deployment/rsyslog | grep ActionStorehouse)
    count=$(expr ${count} + 1)
    # echo "${count}/10"
    sleep 60
done
# echo "${count} - ${actions}"

if [  "${actions}" == '' ] ; then
    echo
    echo '<div><hr><h2 id="actions_status">Action Status</h2>'
    echo '<p>ERROR: No action generation message found. </p></div>'
    exit 2
fi
