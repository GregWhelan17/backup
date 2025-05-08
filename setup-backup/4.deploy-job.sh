kubectl -n turbobkup delete -f ../cronjob.yaml --ignore-not-found
kubectl -n turbobkup apply -f ../cronjob.yaml
