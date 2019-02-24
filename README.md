## Experiments with a modern stack

1. ./bin/cluster-up.sh
    - wait for cluster to spin up and become available 
2. Set up helm for the cluster 
    - kubectl create serviceaccount --namespace kube-system tiller                                                                                           1 ⏎  +21048 1:44 ❰─┘
    - kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
    - helm init --service-account tiller
3. kubectl create -f https://k8s.io/examples/admin/namespace-dev.json
4. kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml
5. helm install --debug --name zigdata --namespace development --values values.yaml --values secrets.yaml .
    - anytime the app is redeployed run `python route53.py` to add the elb's dns to the route53 records for that domain
    - will create {elb,app,lab,dev}.zigdata.org subdomains
6. Update images in cluster
    - ./bin/update-cluster-images.sh