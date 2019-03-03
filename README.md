## Experiments with a modern stack

1. source .env 
2. ./bin/cluster-up.sh
    - wait for cluster to spin up and become available
3. ./bin/bootstrap-cluster.sh
4. ./bin/create-ingress.sh
    - python setupDNS.py
5. ./bin/create-cert-manager.sh
    - wait until resources are ready
    - kubectl apply -f zigdata/production-issuer.yaml
    - kubectl apply -f zigdata/staging-issuer.yaml
6. ./bin/deploy.sh

### Blogging
hot reloading at zigdata.org
```
./bin/live-blogging.sh
```