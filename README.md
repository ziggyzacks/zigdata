## Experiments with a modern stack

export KOPS_STATE_STORE=s3://zigdata-org-state-store
export NAME=zigdata.org

1. ./bin/cluster-up.sh
    - wait for cluster to spin up and become available
2. ./bin/bootstrap-cluster.sh
3. # nginx ingress
    helm install stable/nginx-ingress --name zigdata-ingress \
    --set controller.stats.enabled=true \
    --set controller.metrics.enabled=true
4.  ./bin/deploy.sh
5. helm install --name redis stable/redis --values redis-production-values
6. ./bin/bootstrap-tls.sh
    - wait until resources are ready
    - kubectl apply -f zigdata/production-issuer.yaml
    - kubectl apply -f zigdata/staging-issuer.yaml
