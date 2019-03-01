#!/usr/bin/env bash
docker login --username $DOCKER_USERNAME --password $DOCKER_PASSWORD
docker build -t base .
docker tag base zigzacks/zigdata:base
docker push zigzacks/zigdata:base
docker build -t jupyter apps/jupyter
docker tag jupyter zigzacks/zigdata:jupyter
docker push zigzacks/zigdata:jupyter
docker build -t reddit crons/reddit
docker tag reddit zigzacks/zigdata:reddit
docker push zigzacks/zigdata:reddit
docker build -t blog apps/blog
docker tag blog zigzacks/zigdata:blog
docker push zigzacks/zigdata:blog
