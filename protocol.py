#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

from twisted.words.protocols import irc

from logger import MessageLogger
from message import Message

class IRCBot(irc.IRCClient):

	nickname = 'nux'

	def __init__(self, log_file_name):
		# weird, connectionMade seems to be called before __init__
		log_file = open(log_file_name, 'a')
		self.logger = MessageLogger(log_file)

	def connectionMade(self):
		irc.IRCClient.connectionMade(self)
		print 'Connected.'

	def connectionLost(self, reason):
		irc.IRCClient.connectionLost(self, reason)
		print 'Disconnected.'

	def signedOn(self):
		for channel in self.factory.channels:
			self.join(channel)

	def joined(self, channel):
		print 'Joined %s' % channel
		self.factory.addChannel(channel)

	def invited(self, channel, inviter):
		print 'Invited to %s by %s' % (channel, inviter)
		self.join(channel)

	def kickedFrom(self, channel, kicker, message):
		print 'Kicked from %s by %s (%s)' % (channel, kicker, message)
		self.factory.removeChannel(channel)

	def left(self, channel):
		print 'Left %s' % channel
		self.factory.removeChannel(channel)

	def privmsg(self, prefix, channel, msg):
		self.sender_nick = self.getNickFromPrefix(prefix)
		self.destination_channel = channel
		self.message = msg

		if channel == self.nickname:
			self.is_from_channel = False
			self.channel = None
		else:
			self.is_from_channel = True
			self.channel = channel
			self.factory.channels[channel].new_message(
					Message(self.sender_nick, self.message))

		self.commander.handle_message()

	def getLastURL(self):
		if self.channel is not None:
			return self.factory.channels[self.channel].getLastURL()
		else:
			return None

	def reply(self, message):
		if self.is_from_channel:
			to = self.destination_channel
		else:
			to = self.sender_nick
		self.msg(to, message)

	def getNickFromPrefix(self, prefix):
		return prefix.split('!', 1)[0]

	# Twisted IRC does not have a method for INVITE
	def handleCommand(self, command, prefix, params):
		if command == 'INVITE' and params[0] == self.nickname:
			channel = params[1]
			inviter = self.getNickFromPrefix(prefix)
			self.invited(channel, inviter)
		else:
			irc.IRCClient.handleCommand(self, command, prefix, params)

	def lineReceived(self, line):
		self.logger.log('-> %s' % line)
		irc.IRCClient.lineReceived(self, line)

	def sendLine(self, line):
		line = line.encode('utf-8', 'replace')
		self.logger.log('<- %s' % line)
		irc.IRCClient.sendLine(self, line)

	def getFactoryUptimeInSeconds(self):
		return self.factory.getUptimeInSeconds()
