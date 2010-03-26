#!/bin/sh

TARGET_URL=$(echo -n $(echo $@ | tr ' ' '\n'| tail -n1) )

for arg in $@
do
	if [ "$arg" = "$TARGET_URL" ]; then
		continue
	fi

	FF_ARGS="${FF_ARGS} $arg"
done

# ezstream might die from starving for input but not ffmpeg
# add timeout in order to avoid zombie creation
if [ -z "$FF_TCP_OPTIONS" ]; then
    export FF_TCP_OPTIONS="timeout=10000"
fi

if [ -z "$FF_UDP_OPTIONS" ]; then
    export FF_UDP_OPTIONS="timeout=10000"
fi


CONFFILE=/etc/ezstream/$(echo -n $TARGET_URL | md5sum | cut -f1 -d' ')

/usr/bin/ffmpeg ${FF_ARGS} - |  ezstream -c ${CONFFILE} 2> /dev/null
rm $CONFFILE
