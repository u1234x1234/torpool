#!/bin/bash
set -e
cd "/usr/local/bin/"
DEFAULT_COMMAND="multitor --init 1 -u multitor --socks-port 9000 --control-port 9900 --proxy privoxy --haproxy --debug --verbose"

if [ -z "$*" ]
then
  bash $DEFAULT_COMMAND
else
  COMMAND=$(echo $* | sed 's/-u \w\+/-u multitor/')
  bash $COMMAND
fi

trap : TERM INT; (while true; do sleep 1000; done) & wait
