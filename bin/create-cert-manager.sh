#!/usr/bin/env bash
# cert stuff
# Install the CustomResourceDefinition resources separately
kubectl apply -f https://raw.githubusercontent.com/jetstack/cert-manager/release-0.6/deploy/manifests/00-crds.yaml

# Create the namespace for cert-manager
kubectl create namespace cert-manager

# Label the cert-manager namespace to disable resource validation
kubectl label namespace cert-manager certmanager.k8s.io/disable-validation=true

# Update your local Helm chart repository cache
helm repo update

# Install the cert-manager Helm chart
helm install --name cert-manager --namespace cert-manager stable/cert-manager