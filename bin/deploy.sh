#!/usr/bin/env bash

cd zigdata
# delete release if present
helm del --purge zigdata
# install
helm install --debug --name zigdata --namespace default --values values.yaml --values secrets.yaml .