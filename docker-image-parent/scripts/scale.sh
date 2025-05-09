#!/bin/sh
get_wait_count(){
    minutes=$1
    period=$2
    expr $minutes \* 60 / $period
}

waitperiod=5
maxwait=$(get_wait_count 10 $waitperiod) # - 10 mins
op=$(kubectl get deployment -n turbonomic --no-headers | cut -f1 -d' ' | grep 'operator')
echo "OPERATOR:${op}"
if [ "${1}" = 'down' ] ; then
    # scale down the operator first
    for dep in ${op} ; do
        # echo ${dep}
        kubectl scale --replicas=0 deployments/${dep} -n turbonomic
    done
    # wait for operator to scale down before we carry on....
    count=0
    while [ $(kubectl get po -n turbonomic --no-headers | grep operator | wc -l) -gt 0 -a ${count} -le ${maxwait} ] ; do
        echo "${count}/${maxwait}: waiting for operator pods to terminate"
        sleep ${waitperiod}
        count=$(expr ${count} + 1)
    done
    
    for dep in $(kubectl get deployment -n turbonomic --no-headers | cut -f1 -d' ' | grep -v actionscripts) ; do
        # echo $dep
        kubectl scale --replicas=0 deployments/${dep} -n turbonomic
    done    
else
    # echo 'NOT SCALING UP FOR NOW'
    # exit 0
    # Just need to scale up the operator. it takes care of everything else
    for dep in ${op} ; do
        # echo $dep
        kubectl scale --replicas=1 deployments/${dep} -n turbonomic
    done
    # TEMP scale everything back up as operator not working
    # for dep in $(kubectl get deployment  -n turbonomic --no-headers | cut -f1 -d' ' | grep -v actionscripts) ; do
    #     # echo $dep
    #     kubectl scale --replicas=1 deployments/${dep} -n turbonomic
    # done
    # check it all comes back up......
    count=0
    while [ $(kubectl get pods -n turbonomic --no-headers | grep -Ev '([0-9]+)\/\1' | wc -l) -gt 0 -a ${count} -lt ${maxwait} ] ; do
        # kubectl get pods -n turbonomic --no-headers | grep -Ev '([0-9]+)\/\1'
        pcount=$(kubectl get pods -n turbonomic --no-headers | grep -Ev '([0-9]+)\/\1' | wc -l)
        echo "${count}/${maxwait}: waiting for ${pcount} pods to start"
        # kubectl get pods -n turbonomic --no-headers | awk '!/1\/1/ {print $0}'
        # echo '=================================================================================================='
        sleep ${waitperiod}
        count=$(expr ${count} + 1)
    done
fi
