#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2

def shorten(url, name=None):
	lyli_url = 'http://lyli.fi/?url=' + urllib2.quote(url)
	if name is not None:
		lyli_url += '&name=' + urllib2.quote(name)
	short_url = urllib2.urlopen(lyli_url).read()
	return short_url
