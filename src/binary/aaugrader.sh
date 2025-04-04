#!/usr/bin/bash

FILENAME=/tmp/$(date +"%Y-%m-%dT%H:%M:%S").strace

# Run program and produce syscall logs
strace -fvy -s 256 /home/jens/aaugrader 2> $FILENAME

# Forward syscall logs to IDS
if [ $? -eq 0 ]; then
  (curl -X POST --data-binary "@$FILENAME" "http://ids:8080/upload?name=$FILENAME" -s && rm "$FILENAME") & 
fi
