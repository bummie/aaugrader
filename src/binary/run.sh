#!/bin/sh

socat -T60 TCP-LISTEN:8000,reuseaddr,fork,su=jens EXEC:"/home/jens/aaugrader.sh",stderr
