#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from twisted.internet import reactor, protocol

from protocol import IRCBot
from commander import Commander
from channel import Channel

class IRCBotFactory(protocol.ClientFactory):

	def __init__(self):
		self.born = time.time()
		self.channels = {}
		self.log_file_name = 'log.txt'

	def buildProtocol(self, addr):
		protocol = IRCBot(self.log_file_name)
		protocol.factory = self
		protocol.commander = Commander(protocol)
		self.buildChannels(protocol)
		return protocol

	def buildChannels(self, protocol):
		for channel in self.channels:
			self.channels[channel] = Channel()

	def addChannel(self, name):
		if name not in self.channels:
			self.channels.update({name: Channel()})

	def removeChannel(self, name):
		if name in self.channels:
			self.channels.pop(name)

	def clientConnectionLost(self, connector, reason):
		connector.connect()

	def clientConnectionFailed(self, connector, reason):
		print "connection failed:", reason
		reactor.stop()

	def getUptimeInSeconds(self):
		return time.time() - self.born