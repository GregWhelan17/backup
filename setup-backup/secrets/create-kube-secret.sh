#!/bin/bash
cd

kubectl -n turbobkup delete secret kube-secret --ignore-not-found
kubectl -n turbobkup create secret generic kube-secret --from-file=.kube/config
