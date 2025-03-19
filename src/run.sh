#!/bin/sh

echo 0 | tee /proc/sys/kernel/randomize_va_space

socat -T60 TCP-LISTEN:8000,reuseaddr,fork,su=jens EXEC:/home/jens/aaugrader,stderr
