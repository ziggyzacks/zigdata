## Experiments with a modern stack

1. [Set up kubernetes cluster with kops](https://github.com/kubernetes/kops/blob/master/docs/aws.md)
2. Get docker repo & image set up/built/pushed
3. Set up helm for the cluster 
    - helm create
    - helm init
    - ...
4. kubectl create -f https://k8s.io/examples/admin/namespace-dev.json
5. helm install --name zigdata --namespace development .
    - anytime the app is redeployed run `python route53.py` to add the elb's dns to the route53 records for that domain
    - will create elb.zigdata.org and app.zigdata.org subdomains