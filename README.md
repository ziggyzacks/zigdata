## Experiments with a modern stack

export KOPS_STATE_STORE=s3://zigdata-org-state-store
export NAME=zigdata.org

1. ./bin/cluster-up.sh
    - wait for cluster to spin up and become available
2. ./bin/bootstrap-cluster.sh
3. ./bin/bootstrap-tls.sh
    - kubectl apply -f zigdata/staging-issuer.yaml
4. ./bin/deploy.sh
