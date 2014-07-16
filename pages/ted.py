#!/usr/bin/env python
# -*- coding: utf-8 -*-

from page import Page

class TED(Page):

	def getBanner(self):
		return '\033[91mTED'

	def getInfo(self):
		speaker = self.getSpeaker()
		title = self.getTitle()
		duration = self.getDuration()
		return '%s: %s (%s)' % (speaker, title, duration)

	def getSpeaker(self):
		return self.getMetaInformation('name', 'author')

	def getTitle(self):
		return self.getMetaInformation('property', 'og:title')

	def getDurationInSeconds(self):
		seconds = self.getMetaInformation('property', 'video:duration')
		try:
			return int(seconds)
		except:
			return None
