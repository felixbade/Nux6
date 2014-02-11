#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2

try:
	from BeautifulSoup import BeautifulSoup
except ImportError:
	from bs4 import BeautifulSoup

from url import getLastURL

YOUTUBE_BANNER = '\00314[\00300You\00304Tube\00314]\x0f'

# TODO: non-ascii? newlines?
def link_handler(message, bot):
	url = getLastURL(message)
	url = getFinalRedirect(url)

	if isYoutubeLink(url):
		info = getYoutubeVideoInfo(url)

	else:
		info = getLinkInfo(url)
	
	bot.reply(info)

def getFinalRedirect(url):
	return urllib2.urlopen(url).geturl()

def isYoutubeLink(url):
	return '://www.youtube.com/watch' in url

def getYoutubeVideoInfo(url):
	youtube_page = getYoutubePage(url)
	title = getYoutubeVideoTitle(youtube_page)
	duration = getYoutubeVideoDuration(youtube_page)
	uploader = getYoutubeVideoUploader(youtube_page)
	banner = YOUTUBE_BANNER
	return '%s \002%s\002 (%s) by %s' % (banner, title, duration, uploader)

def getYoutubePage(url):
	return urllib2.urlopen(url).read()

def getYoutubeVideoTitle(youtube_page):
	return 'Title'

def getYoutubeVideoDuration(youtube_page):
	return '0:00'

def getYoutubeVideoUploader(youtube_page):
	return 'nobody'

def getLinkInfo(url):
	try:
		raw_http = urllib2.urlopen(url)
		if isHTML(raw_http):
			return getTitleMessage(raw_http)
		else:
			return getFileInfoMessage(raw_http)
	except urllib2.HTTPError as e:
		return getErrorMessage(e)

def isHTML(raw_http):
	content_type = raw_http.info().getheaders('Content-Type')[0]
	return content_type.startswith('text/html')

def getTitleMessage(raw_http):
	page = raw_http.read()
	soup = BeautifulSoup(page)
	title = soup.title
	if title is not None:
		title = title.string
		return 'Title: %s' % title
	else:
		return 'No title'

def getFileInfoMessage(raw_http):
	length = getContentLengthInKB(raw_http)
	file_type = getFileType(raw_http)
	return '%s kB, type: %s' % (length, file_type)

def getContentLengthInKB(raw_http):
	if len(raw_http.info().getheaders('Content-Length')) > 0:
		length_in_bytes = int(raw_http.info().getheaders('Content-Length')[0])
		return str(round(length_in_bytes/1024.0,1))
	else:
		return '???'

def getFileType(raw_http):
	types = raw_http.info().getheaders('Content-Type')
	if len(types) > 0:
		return types[0]
	else:
		return '???'

def getErrorMessage(e):
	return "%i - %s" % (e.code, e.msg)
