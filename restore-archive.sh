kubectl delete configmap archive -n turbobkup --ignore-not-found
kubectl create configmap archive --from-literal=archive=$1 -n turbobkup
kubectl apply -f testrestore.yaml -n turbobkup
# make sure the pod starts and runs
count=0
while [ "$(kubectl get pod -n turbobkup --no-headers | grep turbo-restore | awk '/Completed|Running/ {print $0}' )" = '' -a ${count} -lt 10 ] ; do
    echo "${count}/10: waiting for job pod to start"
    sleep 10
    count=$(expr ${count} + 1)
done
if [ "$(kubectl get pod -n turbobkup --no-headers | grep turbo-restore | awk '/Completed|Running/ {print $0}' )" = '' ] ; then
    echo 'ERROR: Job Pod failed to start correctly'
    kubectl delete -f testrestore.yaml
else
    echo '=============== wait for pod to finish ==============='
    count=0
    while [ "$(kubectl get pod -n turbobkup --no-headers | grep Completed | grep turbo-restore | cut -f1 -d' ')" = '' -a ${count} -lt 10 ] ; do
        echo "${count}/10: waiting for job pod to finish"
        sleep 10
        count=$(expr ${count} + 1)
    done

    echo '=============== Logs ==============='
    if [ "$(kubectl get pod -n turbobkup --no-headers | grep Completed | grep turbo-restore | cut -f1 -d' ')" = '' ] ; then
        echo 'ERROR: Pod failed to complete successfully'
        kubectl delete -f testrestore.yaml
    fi
fi
kubectl delete configmap archive -n turbobkup