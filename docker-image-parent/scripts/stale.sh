#!/bin/bash

stale=$(kubectl logs deployment/rsyslog | awk '/== Stale Data Report ==/ {go=1} ; (go == 1) {print $0} ; /== end of report ==/ {go=0}')

if [ "${stale}" != '' ] ; then
    echo
    echo '<div><hr><h2 id="stale_status">Stale Target Status</h2>'
    echo '<p>Stale target data detected:</p>'
    echo "${stale}" | sed 's/$/<br>/'
    echo '</div>'
    exit 1
fi