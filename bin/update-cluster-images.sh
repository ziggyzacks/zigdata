#!/usr/bin/env bash

cd zigdata
# delete release
helm del --purge zigdata
# install
helm install --debug --name zigdata --namespace development --values values.yaml --values secrets.yaml .

echo $(helm list)
function check_elb {
    echo $(kubectl get svc -n development -o json | jq '.items | length')
}

function log {
    echo "$(date) - $1"
}

log "updating the DNS"
cd ..
python bin/route53.py
stern --since 5m -n development zigdata