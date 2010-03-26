#!/bin/sh

if [ -z "$FF_TCP_OPTIONS" ]; then
    export FF_TCP_OPTIONS="timeout=10000"
fi

if [ -z "$FF_UDP_OPTIONS" ]; then
    export FF_UDP_OPTIONS="timeout=10000"
fi

/usr/bin/ffmpeg $@

echo "Waiting for subprocess termination"
wait
