## Experiments with a modern stack

1. ./bin/cluster-up.sh
    - wait for cluster to spin up and become available 
2. ./bin/bootstrap-cluster.sh
3. helm install --debug --name zigdata --namespace development --values values.yaml --values secrets.yaml .
    - anytime the app is redeployed run `python route53.py` to add the elb's dns to the route53 records for that domain
    - will create {elb,app,lab,dev}.zigdata.org subdomains
4. Update images in cluster
    - ./bin/update-cluster-images.sh