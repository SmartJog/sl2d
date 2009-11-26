#!/usr/bin/python

import fcntl
import os
import re
import select
import socket
import sys
import time

def send_headers(sock, url):
    """ Send HTTP headers to @url@ through @sock@. """

    regex = re.match('http://(([^:]+)(:(.*))?@)?([^/@:]+)(:([^/]+))?/(.*)', url)
    if regex:
        _, _, _, _, host, _, port, path = regex.groups()

        if not port:
            port = 21
    else:
        print "Malformed URL", url
        sys.exit(1)

    data = 'POST /%(path)s HTTP/1.1\n\
User-Agent: Lavf52.36.0\n\
Accept: */*\n\
Range: bytes=0-\n\
Host: localhost:8080\n\
Authorization: Basic\n\
Connection: close\n\
\n\
' % {'path' : path}

    if port is None:
        port = 80
    else:
        port = int(port)

    print "Sending data to", host, port, path
    sock.connect((host, port))
    sock.send(data)

def main():


    timeout = int(sys.argv[1])

    fcntl.fcntl(0, fcntl.F_SETFL, os.O_NONBLOCK)
    fcntl.fcntl(1, fcntl.F_SETFL, os.O_NONBLOCK)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_headers(sock, sys.argv[2])
    sock.setblocking(False)

    fcntl.fcntl(0, fcntl.F_SETFL, os.O_NONBLOCK)
    fcntl.fcntl(1, fcntl.F_SETFL, os.O_NONBLOCK)

    last = time.time()
    max_buf = 10000
    input_buf = ""

    while True:
        rlisten = []
        wlisten = []
        if len(input_buf) < max_buf:
            rlisten = [sys.stdin]
            if len(input_buf) > 0:
                wlisten = [sock]
        else:
            wlisten = [sock]

        fds = select.select(rlisten, wlisten, [], timeout)

        if fds[0]:
            if len(input_buf) < max_buf:
                read = sys.stdin.read()
                if len(read) == 0:
                    print "STDIN closed. Exiting"
                    sys.exit(1)
                input_buf += read

                last = time.time()

        if fds[1]:
            try:
                sent = sock.send(input_buf[0:1024])
                input_buf = input_buf[sent:]
            except Exception:
                pass

        if fds == ([], [], []):
            sys.stderr.write("Pipe timeout (%s seconds)" % timeout)
            sys.stdin.flush()
            sys.stdin.close()
            sys.exit(2)

if __name__ == '__main__':
    main()
