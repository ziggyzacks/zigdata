#!/usr/bin/env bash
docker build -t zigdata .
docker tag zigdata zigzacks/zigdata:latest
docker push zigzacks/zigdata
