#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2

from bs4 import BeautifulSoup

from url import getLastURL

YOUTUBE_BANNER = '\00314[\00300You\00304Tube\00314]\x0f'

# TODO: non-ascii? newlines in title?
def link_handler(message, bot):
	url = getFinalRedirect(getLastURL(message))
	bot.reply(getInfoAboutURL(url))

def getFinalRedirect(url):
	return urllib2.urlopen(url).geturl()

def getInfoAboutURL(url):
	if isYoutubeLink(url):
		return getYoutubeVideoInfo(url)
	else:
		return getLinkInfo(url)

def isYoutubeLink(url):
	return '://www.youtube.com/watch' in url

def getLinkInfo(url):
	try:
		raw_http = urllib2.urlopen(url)
		if isHTML(raw_http):
			return getTitleMessage(raw_http)
		else:
			return getFileInfo(raw_http)
	except urllib2.HTTPError as e:
		return getErrorMessage(e)



def getYoutubeVideoInfo(url):
	youtube_page = getYoutubePageSoup(url)
	title = getYoutubeVideoTitle(youtube_page)
	duration = getYoutubeVideoDuration(youtube_page)
	uploader = getYoutubeVideoUploader(youtube_page)
	banner = YOUTUBE_BANNER
	return '%s \x02%s\x0f (%s) by %s' % (banner, title, duration, uploader)

def getYoutubePageSoup(url):
	return BeautifulSoup(urllib2.urlopen(url).read())

def getYoutubeVideoTitle(youtube_page):
	for meta_tag in youtube_page.find_all('meta'):
		if 'name' in meta_tag.attrs and meta_tag.attrs['name'] == 'title':
			title = meta_tag.attrs['content']
			return title
	return '???'

def getYoutubeVideoDuration(youtube_page):
	for meta_tag in youtube_page.find_all('meta'):
		if 'itemprop' in meta_tag.attrs and meta_tag.attrs['itemprop'] == 'duration':
			return getDurationFromYoutubeString(meta_tag.attrs['content'])
	return '?:??'

def getYoutubeVideoUploader(youtube_page):
	tags = youtube_page.find_all("span", class_='yt-user-name')
	if len(tags) > 0:
		return tags[0].text
	else:
		return '???'

def getDurationFromYoutubeString(length):
	# example: PT10M44S = 10 minutes, 44 seconds
	minutes = int(length[2 : length.find('M')])
	seconds = int(length[length.find('M')+1 : length.find('S')])
	return getDurationStringFromMinutesAndSeconds(minutes, seconds)

def getDurationStringFromMinutesAndSeconds(minutes, seconds):
	if minutes < 60:
		return '%i:%02i' % (minutes, seconds)
	else:
		hours = minutes / 60
		minutes = minutes % 60
		return '%i:%02i:%02i' % (hours, minutes, seconds)



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

def getFileInfo(raw_http):
	length = getContentLength(raw_http)
	file_type = getFileType(raw_http)
	return '%s, type: %s' % (length, file_type)

def getContentLength(raw_http):
	try:
		length = dummyGetContentLengthInKB(raw_http)
	except:
		length = '???'
	return '%s kB' % length

def dummyGetContentLengthInKB(raw_http):
	length_in_bytes = int(raw_http.info().getheaders('Content-Length')[0])
	return str(round(length_in_bytes/1024.0, 1))

def getFileType(raw_http):
	types = raw_http.info().getheaders('Content-Type')
	if len(types) > 0:
		return types[0]
	else:
		return '???'

def getErrorMessage(e):
	return "%i - %s" % (e.code, e.msg)