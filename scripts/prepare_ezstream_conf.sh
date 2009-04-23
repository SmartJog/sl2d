#!/bin/sh

NAME=$(echo $1 | sed  's/_/ /g')
TARGET_URL=$2
PASSWORD=$3
FORMAT=$4
CHANNELS=$5
BIT_RATE=$6
SAMPLE_RATE=$7

CONFFILE=/etc/ezstream/$(echo -n $TARGET_URL | md5sum | cut -f1 -d' ')

if [ ! -d "$(dirname ${CONFFILE})" ]; then
	mkdir -p $(dirname ${CONFFILE})
fi

REPORT=$(cat > ${CONFFILE} <<EOF
<ezstream>
	<url>${TARGET_URL}</url>
	<sourcepassword>${PASSWORD}</sourcepassword>

	<format>${FORMAT}</format>
	<filename>stdin</filename>
	<stream_once>1</stream_once>

	<svrtype>shoutcast</svrtype>
	<svrinfoname>${NAME}</svrinfoname>
	<svrinfourl> </svrinfourl>
	<svrinfogenre> </svrinfogenre>
	<svrinfodescription> </svrinfodescription>
	<svrinfopublic>0</svrinfopublic>

	<svrinfobitrate>${BIT_RATE}</svrinfobitrate>
	<svrinfochannels>${CHANNELS}</svrinfochannels>
	<svrinfosamplerate>${SAMPLE_RATE}</svrinfosamplerate>
</ezstream>
EOF)
