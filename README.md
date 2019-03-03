## Experiments with a modern stack

1. source .env 
2. ./bin/cluster-up.sh
    - wait for cluster to spin up and become available
3. ./bin/bootstrap-cluster.sh
4. # nginx ingress
    helm install stable/nginx-ingress --name zigdata-ingress \
    --set controller.stats.enabled=true \
    --set controller.metrics.enabled=true
5.  ./bin/deploy.sh
    - helm install --name redis stable/redis --values redis-production-values
6. ./bin/bootstrap-tls.sh
    - wait until resources are ready
    - kubectl apply -f zigdata/production-issuer.yaml
    - kubectl apply -f zigdata/staging-issuer.yaml
    - kubectl apply -f zigdata/production-certificate.yaml
    - kubectl apply -f zigdata/staging-certificate.yaml
7. ./bin/deploy.sh to redeploy and get certs connected
8. wait and then delete zigdata-org certificate

### Blogging
```
cd apps/blog/zigdata
# constantly rebuild local
lektor build -O build --watch &
# start file watcher to hot reload static pages
python watcher.py
```

or for convienence
```
./bin/live-blogging.sh
```