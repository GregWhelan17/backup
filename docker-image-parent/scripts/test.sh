#!/bin/bash
set -e
count=0
echo starting
mkdir -p ~/.kube
cp /kubeconfig/config ~/.kube/config
kubectl get ns
kubectl get pods
sleep 10
echo "going: ${count}"
while [ ${count} -lt 10 ] ; do
  count=$(expr ${count} + 1)
  echo "resting: ${count}"
  sleep 60
done