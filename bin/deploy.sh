#!/usr/bin/env bash

cd zigdata
# delete release if present
helm del --purge zigdata
# install
helm install --debug --name zigdata --namespace default --values values.yaml --values secrets.yaml .
function log {
    echo "$(date) - $1"
}

log "updating the DNS"
cd ..
python bin/route53.py
stern --since 5m zigdata