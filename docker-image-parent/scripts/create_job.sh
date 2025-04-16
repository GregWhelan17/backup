#!/bin/bash

get_wait_count(){
    minutes=$1
    period=$2
    expr $minutes \* 60 / $period
}

ns=turbonomic
direction=$1
archive=$2

period=10
maxPodWait=$(get_wait_count 130 ${period}) # - 2 hrs 10 mins
maxJobWait=$(get_wait_count 1 ${period}) # - 1 min
startPodWait=$(get_wait_count 10 ${period}) # - 5 min

ls -lL /archive/archive
cat /archive/archive
exit

# check there isn't a backup running already
if [ "$(kubectl get pod -n ${ns} --no-headers | grep turbobkup)" != '' ] ; then
    echo 'ERROR: There is a backup already running, ending script'
    exit 1
fi
if [ "$(kubectl get pod -n ${ns} --no-headers | grep turbo-restore)" != '' ] ; then
    echo 'ERROR: There is a restore running, ending script'
    exit 1
fi

./scale.sh down

for pvc in $(kubectl get pvc -n ${ns} --no-headers -o custom-columns=":metadata.name" | grep -v 'timescaledb' | grep -v 'turbo-bkup'); do
    echo "        - mountPath: /pvcs/${pvc}
          name: ${pvc}" >> mounts.yaml
    echo "      - name: ${pvc}
        persistentVolumeClaim:
          claimName: ${pvc}" >> volumes.yaml
done

while IFS= read -r line ; do
    if [ "${direction}" = 'restore' ] ; then
        echo "$line" | tr -d '\015' | sed 's/NAME/turbo-restore/' | sed "s?COMMAND?\"/scripts/launch.sh\", \"restore.py\", \"$archive\"?" >> dbbkup.yaml
        name='turbo-restore'
    else
        echo "$line" | tr -d '\015' | sed 's/NAME/turbobkup/' | sed "s?COMMAND?\"/scripts/launch.sh\", \"backup.py\"?" >> dbbkup.yaml
        name='turbobkup'
    fi
    # echo "$line" | tr -d '\015' | sed 's/NAME/turbobkup/' | sed "s?COMMAND?\"/scripts/launch.sh\", \"backup.py\"?" >> dbbkup.yaml
    if [ "$(echo $line | grep 'volumes:')" != '' ] ; then
        cat volumes.yaml >> dbbkup.yaml
    fi
    if [ "$(echo $line | grep 'volumeMounts:')" != '' ] ; then
        cat mounts.yaml >> dbbkup.yaml
    fi
done < job.yaml 


echo '=============== Updated YAML ==============='
cat dbbkup.yaml

kubectl apply -f dbbkup.yaml -n ${ns}

# make sure the pod starts and runs
echo '=============== wait for pod to start ==============='
count=0
while [ "$(kubectl get pod -n ${ns} --no-headers | grep ${name} | awk '/Completed|Running/ {print $0}' )" = '' -a ${count} -lt ${startPodWait} ] ; do
    echo "${count}/${startPodWait}: waiting for job pod to start"
    sleep ${period}
    count=$(expr ${count} + 1)
done
if [ "$(kubectl get pod -n ${ns} --no-headers | grep ${name} | awk '/Completed|Running/ {print $0}' )" = '' ] ; then
    echo 'ERROR: Job Pod failed to start correctly'
    kubectl delete -f dbbkup.yaml
    failed=1
else
    echo '=============== wait for pod to finish ==============='
    count=0
    while [ "$(kubectl get pod -n ${ns} --no-headers | grep Completed | grep ${name} | cut -f1 -d' ')" = '' -a ${count} -lt ${maxPodWait} ] ; do
        echo "${count}/${maxPodWait}: waiting for job pod to finish"
        sleep ${period}
        count=$(expr ${count} + 1)
    done

    echo '=============== Logs ==============='
    if [ "$(kubectl get pod -n ${ns} --no-headers | grep Completed | grep ${name} | cut -f1 -d' ')" = '' ] ; then
        echo 'ERROR: Pod failed to complete successfully'
        kubectl delete -f dbbkup.yaml
        failed=1
    fi
    kubectl logs $(kubectl get pod -n ${ns} --no-headers | grep Completed | grep ${name} | cut -f1 -d' ')
    echo '============= Logs END ============='

fi
exit 0
./scale.sh up

# The job doesn't end if it didn't complete successfuly, so we delete 
if [ "$failed" ] ; then
    exit 1
fi
