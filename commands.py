#!/usr/bin/env python
# -*- coding: utf-8 -*-

import url_shorter
from url import isURL

def uptime(arguments, bot):
	seconds = bot.getFactoryUptimeInSeconds()
	days = seconds / 60 / 60 / 24
	hours = (seconds / 60 / 60) % 24
	if days > 0:
		reply_text = '%i days, %i hours.' % (days, hours)
	else:
		reply_text = '%i hours.'
	bot.reply(reply_text)

def short(arguments, bot):
	url = bot.getLastURL()
	alias = None
	
	if len(arguments) == 1:
		if isURL(arguments[0]):
			url = arguments[0]
		else:
			alias = arguments[0]
	
	if len(arguments) == 2:
		url = arguments[0]
		alias = arguments[1]

	if url is None:
		return

	short_url = url_shorter.short(url, alias)
	bot.reply(short_url)

def source(arguments, bot):
	bot.reply('https://github.com/felixbade/Nux6')

def s(arguments, bot):
	short(arguments, bot)