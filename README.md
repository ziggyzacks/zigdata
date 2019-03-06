## Experiments with a modern stack

### Steps

#### Edit environment variables

#### Set environment variables
`source .env`

#### Create Cluster
```
kops create cluster \
        --zones us-east-1a \
        --node-count 1 \
        --node-size t3.small \
        --master-size t3.medium \
        --ssh-public-key $SSH \
        --name $NAME

kops update cluster ${NAME} --yes
```
run `watch kops validate cluster` to track the cluster creation process. Even after initial connectivity, the cluster
may take some time to become stable


#### Add helm (tiller) to cluster
```
kubectl create serviceaccount --namespace kube-system tiller
kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
helm init --service-account tiller
```

#### Create nginx ingress
```
helm install stable/nginx-ingress --name zigdata-ingress
```

#### Add A records to route53 that point to the load balancer that the ingress deployment creates
```
python bin/setupDNS.py
```

#### Install cert-manager to handle SSL/TLS
```
kubectl apply -f https://raw.githubusercontent.com/jetstack/cert-manager/release-0.6/deploy/manifests/00-crds.yaml
kubectl create namespace cert-manager
kubectl label namespace cert-manager certmanager.k8s.io/disable-validation=true
helm repo update
helm install --name cert-manager --namespace cert-manager stable/cert-manager
```

#### Create Issuers once cert-manager is ready
```
kubectl apply -f zigdata/staging-issuer.yaml
kubectl apply -f zigdata/production-issuer.yaml
```

#### Deployments
```
source .deployer
# redeploy whole site
deploy_all
# redeploy one chart 
redeploy <chart>
```

**optional**
```
helm install --name heapster stable/heapster --namespace kube-system
helm install --name dashboard stable/kubernetes-dashboard --namespace kube-system
helm install --name postgres stable/postgresql
helm install --name redis stable/redis
```

### Blogging
hot reloading at zigdata.org
```
./bin/live-blogging.sh
```