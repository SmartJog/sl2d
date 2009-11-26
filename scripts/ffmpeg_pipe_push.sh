#!/bin/sh

TARGET_URL=$(echo -n $(echo $@ | tr ' ' '\n'| tail -n1) )

for arg in $@
do
	if [ "$arg" = "$TARGET_URL" ]; then
		continue
	fi

	FF_ARGS="${FF_ARGS} $arg"
done

/usr/bin/ffmpeg ${FF_ARGS} - | /usr/share/sl2d/push.py 10 ${TARGET_URL} &
FFPID=`ps | grep '/usr/bin/ffmpeg' | awk '{ print $1 }'`
wait $!
kill -9 $FFPID >/dev/null 2>&1
