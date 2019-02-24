#!/usr/bin/env bash
# helm setup
kubectl create serviceaccount --namespace kube-system tiller                                                                                           1 ⏎  +21048 1:44 ❰─┘
kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
helm init --service-account tiller
# make a development namespace
kubectl create -f https://k8s.io/examples/admin/namespace-dev.json
# dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml