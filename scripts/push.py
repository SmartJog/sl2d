#!/usr/bin/python
# -*- coding: utf-8 -*-

import fcntl
import os
import re
import select
import socket
import sys

def send_headers(sock, url, agent='Lavf52.36.0'):
    """ Send HTTP headers to @url@ through @sock@. """

    regex = re.match('http://(([^:]+)(:(.*))?@)?([^/@:]+)(:([^/]+))?/(.*)', url)
    if regex:
        _, _, _, _, host, _, port, path = regex.groups()

        if not port:
            port = 80
        else:
            try:
                port = int(port)
            except ValueError:
                sys.stderr.write("Invalid port number.\n")
                sys.exit(1)
    else:
        sys.stderr.write("Malformed URL %s.\n" % url)
        sys.exit(1)

    data = 'POST /%(path)s HTTP/1.1\n\
User-Agent: %(agent)s\n\
Accept: */*\n\
Range: bytes=0-\n\
Host: %(host)s:%(port)s\n\
Authorization: Basic\n\
Connection: close\n\
\n\
' % {
    'host' : host,
    'port' : port,
    'path' : path,
    'agent': agent,
}

    sys.stderr.write("Sending data to %s %s %s.\n" % (host, port, path))
    sock.connect((host, port))
    sock.send(data)


def main():
    """ Main function. """

    try:
        timeout = int(sys.argv[1])
    except ValueError:
        sys.stderr.write("Invalid value for timeout.\n")
        sys.exit(1)

    # Initialize socket and remote host
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_headers(sock, sys.argv[2])

    # Prepare streaming phase
    sock.setblocking(False)
    fcntl.fcntl(sys.stdin, fcntl.F_SETFL, os.O_NONBLOCK)
    fcntl.fcntl(sys.stdout, fcntl.F_SETFL, os.O_NONBLOCK)

    max_buf = 10000
    input_buf = ""

    # Streaming loop
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
                    sys.stderr.write("STDIN closed. Exiting.\n")
                    sys.exit(1)
                input_buf += read

        if fds[1]:
            try:
                sent = sock.send(input_buf[0:1024])
                input_buf = input_buf[sent:]
            except Exception:
                sys.stderr.write("Got an exception while sending data.\n")

        if fds == ([], [], []):
            sys.stderr.write("Pipe timeout (%s seconds).\n" % timeout)
            sys.stdin.flush()
            sys.stdin.close()
            sys.exit(2)

if __name__ == '__main__':
    main()

