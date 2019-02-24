export KOPS_STATE_STORE=s3://zigdata-org-state-store
export NAME=zigdata.org
kops create cluster \
        --zones us-east-1a \
        --node-count 1 \
        --node-size t3.medium \
        --master-size c5.large \
        --ssh-public-key ssh/zigdata_rsa.pub \
        --name $NAME
kops update cluster ${NAME} --yes
# helm setup
kubectl create serviceaccount --namespace kube-system tiller                                                                                           1 ⏎  +21048 1:44 ❰─┘
kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
helm init --service-account tiller
# make a development namespace
kubectl create -f https://k8s.io/examples/admin/namespace-dev.json
# dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml