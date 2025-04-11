#!/bin/bash

get_wait_count(){
    minutes=$1
    period=$2
    expr $minutes \* 60 / $period
}

period=10
maxPodWait=$(get_wait_count 130 ${period}) # - 2 hrs 10 mins
maxJobWait=$(get_wait_count 1 ${period}) # - 1 min
startPodWait=$(get_wait_count 10 ${period}) # - 5 min

# check there isn't a backup running already
if [ "$(kubectl get pod --no-headers | grep db-backup-job)" != '' ] ; then
    echo 'ERROR: There is a backup already running, ending script'
    exit 1
fi
if [ "$(kubectl get pod --no-headers | grep db-restore-job)" != '' ] ; then
    echo 'ERROR: There is a restore running, ending script'
    exit 1
fi

./scale.sh down

for pvc in $(kubectl get pvc --no-headers -o custom-columns=":metadata.name" | grep -v 'timescaledb'); do
    echo "        - mountPath: /pvcs/${pvc}
          name: ${pvc}" >> mounts.yaml
    echo "      - name: ${pvc}
        persistentVolumeClaim:
          claimName: ${pvc}" >> volumes.yaml
done

while IFS= read -r line ; do
    echo "$line" | tr -d '\015' | sed 's/NAME/db-backup-job/' | sed "s?COMMAND?\"/scripts/launch.sh\", \"backup.py\"?" >> dbbkup.yaml
    if [ "$(echo $line | grep 'volumes:')" != '' ] ; then
        cat volumes.yaml >> dbbkup.yaml
    fi
    if [ "$(echo $line | grep 'volumeMounts:')" != '' ] ; then
        cat mounts.yaml >> dbbkup.yaml
    fi
done < job.yaml 


echo '=============== Updated YAML ==============='
cat dbbkup.yaml

kubectl apply -f dbbkup.yaml

# make sure the pod starts and runs
echo '=============== wait for pod to start ==============='
count=0
while [ "$(kubectl get pod --no-headers | grep db-backup-job | awk '/Completed|Running/ {print $0}' )" = '' -a ${count} -lt ${startPodWait} ] ; do
    echo "${count}/${startPodWait}: waiting for job pod to start"
    sleep ${period}
    count=$(expr ${count} + 1)
done
if [ "$(kubectl get pod --no-headers | grep db-backup-job | awk '/Completed|Running/ {print $0}' )" = '' ] ; then
    echo 'ERROR: Job Pod failed to start correctly'
    failed=1
else
    echo '=============== wait for pod to finish ==============='
    count=0
    while [ "$(kubectl get pod --no-headers | grep Completed | grep db-backup-job | cut -f1 -d' ')" = '' -a ${count} -lt ${maxPodWait} ] ; do
        echo "${count}/${maxPodWait}: waiting for job pod to finish"
        sleep ${period}
        count=$(expr ${count} + 1)
    done

    echo '=============== Logs ==============='
    if [ "$(kubectl get pod --no-headers | grep Completed | grep db-backup-job | cut -f1 -d' ')" = '' ] ; then
        echo 'ERROR: Pod failed to complete successfully'
        failed=1
    fi
    kubectl logs $(kubectl get pod --no-headers | grep Completed | grep db-backup-job | cut -f1 -d' ')
    echo '============= Logs END ============='

fi

./scale.sh up

# The job doesn't end if it didn't complete successfuly, so we delete 
if [ "$failed" ] ; then
    kubectl delete -f dbbkup.yaml
    exit 1
fi
