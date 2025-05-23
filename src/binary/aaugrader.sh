#!/usr/bin/bash

FILENAME=/tmp/$(date +"%Y-%m-%dT%H:%M:%S").strace

# Run program and produce syscall logs
strace -o $FILENAME -fvy -s 256 /home/jens/aaugrader 2> "${FILENAME}_cfg_raw"

cat "${FILENAME}_cfg_raw" | grep -E "^(main|getUsername|retrieveGrades|findUser|printGrades|EXIT_OK)" > "${FILENAME}_cfg"
rm "${FILENAME}_cfg_raw"

if [ -f "${FILENAME}_cfg" ]; then
  (curl -X POST --data-binary "@${FILENAME}_cfg" "http://ids:8080/uploadcfg?name={${FILENAME}_cfg}" -s && rm "${FILENAME}_cfg") & 
fi

# Forward syscall logs to IDS
if [ -f $FILENAME ]; then
  (curl -X POST --data-binary "@$FILENAME" "http://ids:8080/upload?name=$FILENAME" -s && rm "$FILENAME") & 
fi
