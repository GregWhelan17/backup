#!/bin/bash

if [ "$(id -u)" -ne 0 ] ; then
    echo 'Must be run as root'
    exit 1
fi

which apt-get > /dev/null 2>&1
if [ $? -eq 0 ] ; then
    echo 'Setting up using apt-get'
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
    sudo apt-get install git-lfs
fi


which yum > /dev/null 2>&1
if [ $? -eq 0 ] ; then
    echo 'Setting up using yum'
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.rpm.sh | sudo bash
    sudo yum install -y git-lfs
fi

git lfs pull
