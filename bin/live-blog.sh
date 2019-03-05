#!/usr/bin/env bash
cd apps/blog/zigdata
# constantly rebuild local
lektor build -O build --watch &
PID=$!
trap "kill -9 $PID" SIGINT SIGTERM
# start file watcher to hot reload static pages
python watcher.py
