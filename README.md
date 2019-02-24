## Experiments with a modern stack

1. kops create cluster --zones us-east-1a --node-count 1 --node-size t3.medium --master-size c5.large --ssh-public-key ssh/zigdata_rsa.pub  zigdata.org
2. export NAME=zigdata.org export KOPS_STATE_STORE=s3://zigdata-org-state-store kops update cluster ${NAME} --yes
3. Set up helm for the cluster 
    - kubectl create serviceaccount --namespace kube-system tiller                                                                                           1 ⏎  +21048 1:44 ❰─┘
    - kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
    - helm init --service-account tiller
4. kubectl create -f https://k8s.io/examples/admin/namespace-dev.json
5. kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml
6. helm install --debug --name zigdata --namespace development --values values.yaml --values secrets.yaml .
    - anytime the app is redeployed run `python route53.py` to add the elb's dns to the route53 records for that domain
    - will create {elb,app,lab,dev}.zigdata.org subdomains