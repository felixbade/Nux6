#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet import reactor, protocol

from bot import IRCBot

class IRCBotFactory(protocol.ClientFactory):

	def __init__(self):#, channel, filename):
		self.channels = []#channel
		self.filename = 'log.txt'#filename

	def buildProtocol(self, addr):
		p = IRCBot()
		p.factory = self
		return p

	def addChannel(self, channel):
		if channel not in self.channels:
			self.channels.append(channel)

	def removeChannel(self, channel):
		if channel in self.channels:
			self.channels.remove(channel)

	def clientConnectionLost(self, connector, reason):
		"""If we get disconnected, reconnect to server."""
		connector.connect()

	def clientConnectionFailed(self, connector, reason):
		print "connection failed:", reason
		reactor.stop()