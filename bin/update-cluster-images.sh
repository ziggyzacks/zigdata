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

#elb=$(check_elb)
#while [ $elb -eq 0 ]
#do
#    elb=$(check_elb)
#    log "waiting for ELB.."
#    sleep 5
#done
#log $elb
#
## dns
#cd ../bin
#python route53.py
# logs
stern --since 5m -n development zigdata