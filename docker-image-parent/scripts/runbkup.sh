#!/bin/sh

cd $(dirname $0)
echo 'Setting kubernets config'
mkdir -p ~/.kube
cp /kubeconfig/config ~/.kube/config
./create_backup_job.sh

