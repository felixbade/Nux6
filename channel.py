#!/usr/bin/env python
# -*- coding: utf-8 -*-

import message
import url

class Channel:

	def __init__(self):
		self._messages = []
		self.max_messages = 5
		self._last_url = None

	def new_message(self, message):
		self._messages.append(message)
		self.checkForURL(message)
		self.removeExcessiveMessages()

	def checkForURL(self, message):
		if url.hasURL(message.getMessage()):
			self._last_url = url.getLastURL(message.getMessage())

	def removeExcessiveMessages(self):
		if len(self._messages) > self.max_messages:
			self._messages = self._messages[-self.max_messages:]

	def getLastURL(self):
		return self._last_url