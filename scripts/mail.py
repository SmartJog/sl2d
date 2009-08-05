#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Simple script to send mails. """

import smtplib
import sys
import os

def main():
    if len(sys.argv) < 5:
        print 'Usage:', sys.argv[0], 'HOST FROM TO TITLE BODY'
        sys.exit(os.EX_USAGE)

    host, from_addr, to_addr, title = sys.argv[1:5]
    body = sys.argv[5:]

    # Add the From: and To: headers at the start!
    msg = ("From: %s\r\nTo: %s\r\nSubject:%s\r\n\r\n" % (from_addr, to_addr, title))

    if hasattr(body, '__iter__') and not isinstance(body, basestring):
        msg = msg + '\n'.join(body)
    else:
        msg = msg + body

    server = smtplib.SMTP(host)
    server.set_debuglevel(1)
    server.sendmail(from_addr, to_addr.split(", "), msg)
    server.quit()
    sys.exit(os.EX_OK)

if __name__ == '__main__':
    main()
