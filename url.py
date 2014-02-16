#!/usr/bin/env python
# -*- coding: utf-8 -*-

def hasURL(text):
	return 'http://' in text or 'https://' in text

def isURL(text):
	return (text.startswith('http://') or text.startswith('https://')) and ' ' not in text

def getLastURL(text):
	for word in text.split():
		if word.startswith('http://') or word.startswith('https://'):
			return word
	return None