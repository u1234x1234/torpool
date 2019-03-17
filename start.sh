#!/bin/bash
set -e
cd "/usr/local/bin/"
DEFAULT_COMMAND="multitor --init 5 -u root --socks-port 9000 --control-port 9900 --proxy privoxy --haproxy"

if [ -z "$*" ]
then
  bash $DEFAULT_COMMAND
else
  bash $*
fi

trap : TERM INT; (while true; do sleep 1000; done) & wait
