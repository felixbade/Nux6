#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Message:

	def __init__(self, sender, message):
		self.sender = sender
		self.message = message

	def getSender(self):
		return self.sender

	def getMessage(self):
		return self.message