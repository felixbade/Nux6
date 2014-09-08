#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands
from url import hasURL, getLastURL
from urlinfo import URLInfo
from url_shortener import shorten

class Commander:

	command_prefix = '!'

	def __init__(self, bot):
		self.bot = bot

	def handle_message(self):
		message = self.bot.message
		if message.startswith(self.command_prefix):
			nocmd = False
			command = message.split()[0][1:]
			arguments = message.split()[1:]
			function = getattr(commands, command, None)
			if function is not None:
				function(arguments, self.bot)
		else:
			nocmd = True

		if hasURL(message):
			url = getLastURL(message)
			self.bot.reply(URLInfo(url).getInfo())
			if len(url) > 50 and nocmd:
				self.bot.reply(shorten(url))
