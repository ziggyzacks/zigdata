#!/usr/bin/env bash

cd zigdata
# delete release
helm del --purge zigdata
sleep 10
# install
helm install --debug --name zigdata --namespace development --values values.yaml --values secrets.yaml .
echo $(helm list)
kubectl get pods,svc,ing,deploy  --all-namespaces
sleep 60

cd ..
# dns
python bin/route53.py
# logs
stern --since 5m -n development zigdata