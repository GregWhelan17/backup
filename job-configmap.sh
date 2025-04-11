kubectl create namespace turbobkup
kubectl -n turbobkup delete configmap job-yaml --ignore-not-found
kubectl -n turbobkup create configmap job-yaml --from-file=job.yaml
