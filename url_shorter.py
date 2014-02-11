#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2

def short(url, alias=None):
	tinyurl_url = 'http://tinyurl.com/create.php?source=indexpage&url=' + urllib2.quote(url)
	if alias is not None:
		tinyurl_url += '&alias=' + urllib2.quote(alias)
	page = urllib2.urlopen(tinyurl_url).read()
	page = page[page.find('preview.tinyurl') + 20:]
	url = 'http://tinyurl.com/' + page[:page.find('<')]
	return url