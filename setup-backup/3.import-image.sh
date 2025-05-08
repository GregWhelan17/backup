#!/bin/bash

# - PARENT IMAGE
sudo ctr -n=k8s.io images import ../docker-image-parent/turbobkupparent.tar

imagepath=$(tar xf ../docker-image/turbobkupparent.tar index.json -O | jq -r '.manifests[0].annotations."io.containerd.image.name"' | cut -f1 -d':')

sha=$(tar xf ../docker-image/turbobkupparent.tar manifest.json -O | jq '.[0].Config' | awk 'BEGIN{FS="/"} {print substr($NF,1,13)}')

echo "EXPECTED IMAGE: ${imagepath}"
echo ""

sudo crictl images | head -1
sudo crictl images | grep ${sha}

# - CHILD IMAGE
sudo ctr -n=k8s.io images import ../docker-image-parent/turbobkupchild.tar

imagepath=$(tar xf ../docker-image/turbobkupchild.tar index.json -O | jq -r '.manifests[0].annotations."io.containerd.image.name"' | cut -f1 -d':')

sha=$(tar xf ../docker-image/turbobkupchild.tar manifest.json -O | jq '.[0].Config' | awk 'BEGIN{FS="/"} {print substr($NF,1,13)}')

echo "EXPECTED IMAGE: ${imagepath}"
echo ""

sudo crictl images | head -1
sudo crictl images | grep ${sha}
