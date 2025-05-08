#!/bin/bash

kubectl create ns turbobkup
cd secrets
for f in * ; do
    ./$f
done
