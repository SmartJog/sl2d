#!/bin/sh

TARGET_URL=$(echo -n $(echo $@ | tr ' ' '\n'| tail -n1) )

for arg in $@
do
	if [ "$arg" = "$TARGET_URL" ]; then
		continue
	fi

	FF_ARGS="${FF_ARGS} $arg"
done

CONFFILE=/etc/ezstream/$(echo -n $TARGET_URL | md5sum | cut -f1 -d' ')

/usr/bin/ffmpeg ${FF_ARGS} - |  ezstream -c ${CONFFILE} 2> /dev/null
rm $CONFFILE
