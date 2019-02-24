#!/usr/bin/env bash
docker build -t zigdata .
docker tag zigdata zigzacks/zigdata:$(git rev-parse HEAD)
docker push zigzacks/zigdata
