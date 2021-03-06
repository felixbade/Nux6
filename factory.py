#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import shelve

from twisted.internet import reactor, protocol

from protocol import IRCBot
from commander import Commander
from channel import Channel

class IRCBotFactory(protocol.ClientFactory):

	def __init__(self):
		self.born = time.time()
		self.channels = shelve.open('channels.db')
		self.log_file_name = 'log.txt'
		self.reconnect_wait = 300

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
                        self.channels.sync()

	def removeChannel(self, name):
		if name in self.channels:
			self.channels.pop(name)
                        self.channels.sync()

	def clientConnectionLost(self, connector, reason):
		print 'Connection lost:', reason
		connector.connect()

	def clientConnectionFailed(self, connector, reason):
		print 'Connection failed:', reason
		print 'Reconnecting in %i seconds' % self.reconnect_wait
		time.sleep(self.reconnect_wait)
		connector.connect()

	def getUptimeInSeconds(self):
		return time.time() - self.born
