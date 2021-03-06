#!/usr/bin/env python
# -*- coding: utf-8 -*-

from page import Page

class Speedtest(Page):

	def getBanner(self):
		return '\033[34mSpeedtest.net'

	def getInfo(self):
		try:
			down = self.getData('share-download')
			up   = self.getData('share-upload')
			ping = self.getData('share-ping')
			isp  = self.getData('share-isp')
			return 'Down: %s, Up: %s, Ping: %s, ISP: %s' % (down, up, ping, isp)
		except:
			return None

	def getData(self, classname):
		return self.soup.find_all('div', class_=classname)[0].find_all('p')[0].text
