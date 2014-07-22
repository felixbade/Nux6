#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from twisted.internet import reactor
from twisted.python import log

from factory import IRCBotFactory

if len(sys.argv) < 2:
    print 'An IRC bot.'
    print 'Usage: %s <host> [<port>]' % sys.argv[0]
    exit(1)

host = sys.argv[1]
port = 6667
try:
    port = int(sys.argv[2])
except IndexError, ValueError:
    pass

if __name__ == '__main__':
	log.startLogging(sys.stdout)
	factory = IRCBotFactory()
	reactor.connectTCP(host, port, factory)
	reactor.run()
