#!/usr/bin/env bash

function log {
    echo "$(date) - $1"
}

log "installing nginx-ingress helm chart"
helm install stable/nginx-ingress --name zigdata-ingress