#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Page:

	def __init__(self, soup):
		self.soup = soup

	def getDuration(self):
		seconds = self.getDurationInSeconds()
		if seconds is None:
			return 'unknown duration'
		minutes, seconds = divmod(seconds, 60)
		if minutes < 60:
			return '%i:%02i' % (minutes, seconds)
		else:
			hours, minutes = divmod(minutes, 60)
			return '%i:%02i:%02i' % (hours, minutes, seconds)

	def getMetaInformation(self, attribute, name):
		for meta_tag in self.soup.find_all('meta'):
			if attribute in meta_tag.attrs and meta_tag.attrs[attribute] == name:
				if 'content' in meta_tag.attrs:
					return meta_tag.attrs['content']
				else:
					return None
		return None

	def getRelativeDate(self, locale='en_US'):
		# today, yesterday, 5 days ago, over 2 weeks ago, 5.3.2014
		return self.getAbsoluteDate()
