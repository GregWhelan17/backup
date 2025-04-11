#!/bin/sh

DEFAULT_SCRIPTS_ORDER="pods pipeline stale actions targets"

# get Jenkins environment variables
# usage() { echo "Usage: $0 -u username -p password [-s scripts] [-n noncriticalpods]"; 1>&2; exit 10; }
usage() { echo "Usage: $0 -t turbohost -u username -p password [-s scripts] [-n noncriticalpods]" ;}

while getopts "t:u:p:s:n:h" o; do
    case "${o}" in
        t) 
            turbohost=$OPTARG
            ;;
        u) 
            username=$OPTARG
            ;;
        p) 
            password=$OPTARG
            ;;
        s)  
            if [ "$OPTARG" == '' ] ; then
                scripts=${DEFAULT_SCRIPTS_ORDER}
            else
                scripts=$(echo $OPTARG | sed 's/,/ /g')
            fi
            ;;
        n) 
            if [ "$OPTARG" != '' ] ; then
                noncriticalpods=$(echo $OPTARG | sed 's/,/ /g')
            fi
            ;;
        h)
            usage
            ;;
        *)
            usage
            exit 10
            ;;
    esac
done

bad=0

for monitor in $scripts ; do
    if [ "${monitor}" == "targets" ] ; then
        # echo "targets.py"
        result="$(python3 targets.py ${turbohost} ${username} ${password})"
        status=$?
        out="${out} ${result}"
        if [ ${status} -gt 0 ] ; then
            echo ${result} > targets.out
        fi
        # echo $monitor ${status}
        if [ ${status} -gt ${bad} ] ; then
            bad=${status}
        fi
    else
        # echo "${monitor}"
        result=$(./${monitor}.sh $noncriticalpods)
        status=$?
        out="${out} ${result}"
        if [ ${status} -gt 0 ] ; then
            echo ${result} > ${monitor}.out
        fi
        # echo $monitor ${status}
        if [ ${status} -gt ${bad} ] ; then
            bad=${status}
        fi
    fi
done

case $bad in
    0) 
        echo "Turbonomic is up and running. " > summary.out
        colour='green'
        subject_status='Normal'
    ;;
    1)
        summary="Turbonomic has some minor non-critical errors but is running. "
        colour='orange'
        subject_status='Minor'
    ;;
    *)
        summary="Turbonomic has critical errors and needs investigation. "
        colour='red'
        subject_status='CRITICAL'
    ;;
esac

# Send Notifications Here use ${out} for content
(echo "<h1 style="background-color:${colour}">Turbonomic Monitoring Status - ${subject_status}</h1>${summary}"
if [ ${bad} -ne 0 ] ; then
    echo ''
    echo '<ul>'
    for monitor in $scripts ; do
        if [ -f "${monitor}.out" ] ; then
            echo '  <li><a href="#'${monitor}'_status">'${monitor^}' Status</a> </li>'
        fi
    done
    echo '</ul>'
    echo '<p>The following problems were found with Turbonomic:</p>'
    echo "$out"
else
    echo 'Turbonomic is working correctly.  '
fi) > summary.out

cat summary.out
