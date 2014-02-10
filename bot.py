#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from twisted.words.protocols import irc

from message_logger import MessageLogger


class IRCBot(irc.IRCClient):

	nickname = "tbot"

	def connectionMade(self):
		irc.IRCClient.connectionMade(self)
		logfile = open(self.factory.filename, "a")
		self.logger = MessageLogger(logfile)
		self.logger.log("Connected.")

	def connectionLost(self, reason):
		irc.IRCClient.connectionLost(self, reason)
		self.logger.log("Disconnected.")
		self.logger.close()

	def signedOn(self):
		for channel in self.factory.channels:
			self.join(channel)

	def joined(self, channel):
		self.logger.log("Joined %s" % channel)
		self.factory.addChannel(channel)

	def invited(self, channel):
		self.logger.log("Invited to %s" % channel)
		self.join(channel)

	def kickedFrom(self, channel):
		self.logger.log("Kicked from %s" % channel)
		self.factory.removeChannel(channel)

	def privmsg(self, user, channel, msg):
		user = user.split('!', 1)[0]
		self.logger.log("<%s> %s" % (user, msg))

		if channel == self.nickname:
			msg = "pleissihoulderi."
			self.msg(user, msg)
			return

		if msg.startswith(self.nickname + ":"):
			msg = "%s: olen botti" % user
			self.msg(channel, msg)
			self.logger.log("<%s> %s" % (self.nickname, msg))

	# Twisted IRC does not have a method for INVITE
	def handleCommand(self, command, prefix, params):
		if command == 'INVITE' and params[0] == self.nickname:
			channel = params[1]
			self.invited(channel)
		else:
			irc.IRCClient.handleCommand(self, command, prefix, params)