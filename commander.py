#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands
from url import hasURL
from link_handler import link_handler

class Commander:

	command_prefix = '!'

	def __init__(self, bot):
		self.bot = bot

	def handle_message(self):
		message = self.bot.message
		if message.startswith(self.command_prefix):
			command = message.split()[0][1:]
			arguments = message.split()[1:]
			function = getattr(commands, command, None)
			if function is not None:
				function(arguments, self.bot)
		
		if hasURL(message):
			link_handler(message, self.bot)