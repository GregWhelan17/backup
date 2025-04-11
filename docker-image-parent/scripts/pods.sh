#!/bin/bash

if [ $# -eq 0 ] ; then
    if [ -f pods-non-critical-default ] ; then
        noncpods=$(grep -v '^\s*#' pods-non-critical-default )
    fi
else
    noncpods=$*
fi
# echo "NON CRITS: ${noncpods}"
# get the number of pods
podcount=$(kubectl get pods -n turbonomic --no-headers | wc -l)


echo "<div><hr><h2 id="pods_status">Pods Status</h2>"
echo "Total Pods: ${podcount} <p>"

    

# add the name of all bad pods to the bad env
bad=$(kubectl get pods -n turbonomic --no-headers | sed -r 's/([0-9]+)\s+(\(.*) ago/\1#\2#ago/' | while read NAME READY STATUS RESTARTS AGE ; do
    # echo "#${NAME}#"
    # echo "#${READY}#"
    # echo "#${STATUS}#"
    # echo "#${RESTARTS}#"
    # echo "${AGE}#"
    # echo '---------------------------'
    
    # status is not running
    if [ "${STATUS}" != 'Running' ] ; then
        # bad="${bad} $(echo ${NAME})"
        # kubectl get pods ${NAME} -n turbonomic --no-headers
        echo ${NAME}
        continue
    fi

    # number of containers is as expected (1/1 2/2 etc)
    if [ "$(echo ${READY} | awk 'BEGIN{FS="/"} {if($1 == $2) {print "Good"} else {print "BAD"} }')" == 'BAD' ] ; then
        # echo BAD
        # bad="${bad} $(echo ${NAME})"
        echo ${NAME}
        continue
    fi

    # multiple restarts last one less than an hour ago
    if [ "$(echo ${RESTARTS} | awk 'BEGIN {FS="#"}{if ($1 > 100 && (match($2,"d") || match($2,"s"))) print "BAD"}')" == 'BAD' ] ; then
        echo ${NAME}
        continue
    fi

done)


nonc_count=0
crit_count=0

table() {
    echo '<p><table>
            <tr>
                <th>NAME</th>
                <th>READY</th>
                <th>STATUS</th>
                <th>RESTARTS</th>
                <th>AGE</th>
            </tr>'

        kubectl get pods $* -n turbonomic --no-headers | sed -r 's/([0-9]+)\s+(\(.*) ago/\1#\2#ago/' | while read NAME READY STATUS RESTARTS AGE ; do
            echo '<tr>
                <td>'${NAME}'</td>
                <td>'${READY}'</td>
                <td>'${STATUS}'</td>
                <td>'${RESTARTS}'</td>
                <td>'${AGE}'</td>
                </tr>'
        done
        echo '</table></p>'
}

if [ "$bad" != '' ] ; then
    code=1
            # if [ "$(echo "${noncpods}" |  awk -v pod=${pod} '{if (match(pod,$0)) {print pod } }')" != '' ] ; then
    
    for pod in ${bad} ; do
        found=0
        for non in ${noncpods} ; do
            if [ "$(echo ${pod} | grep ${non})" != '' ] ; then
                # echo "NONC ${pod}"
                nonc="${nonc} ${pod}"
                nonc_count=$(expr ${nonc_count} + 1)
                found=1
                continue
            fi    
        done
        if [ ${found} -eq 0 ] ; then
            # echo "CRIT ${pod}"
            crit="${crit} ${pod}"
            crit_count=$(expr ${crit_count} + 1)
        fi
    done

    if [ "${crit}" != '' ] ;then
    code=2
        echo
        echo "${crit_count} CRITICAL pods not running correctly:<p>"
        table "${crit}"

    fi
    if [ "${nonc}" != '' ] ;then
        echo 
        echo "${nonc_count} non-critical pods not running correctly:<p>"
        table "${nonc}"
    fi
    echo "</div>"
    exit ${code}
fi

