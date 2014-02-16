#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from twisted.internet import reactor
from twisted.python import log

from factory import IRCBotFactory

if __name__ == '__main__':
	log.startLogging(sys.stdout)
	factory = IRCBotFactory()
	reactor.connectTCP('irc.zah.fi', 6667, factory)
	reactor.run()