#!/usr/bin/env bash
kops create cluster \
        --zones us-east-1a \
        --node-count 1 \
        --node-size t3.micro \
        --master-size t3.micro \
        --ssh-public-key ssh/zigdata_rsa.pub \
        --name $NAME

kops update cluster ${NAME} --yes

kops validate cluster