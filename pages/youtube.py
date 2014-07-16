#!/usr/bin/env python
# -*- coding: utf-8 -*-

from page import Page

class YouTube(Page):

    def getBanner(self):
        return 'You\033[91mTube'

    def getInfo(self):
        title = self.getTitle()
        if title is None:
            return None
        duration = self.getDuration()
        author = self.getAuthor() or 'an unknown user'
        return '\033[1m%s\033[m (%s) by %s' % (title, duration, author)

    def getTitle(self):
        return self.getMetaInformation('name', 'title')

    def getDurationInSeconds(self):
        length = self.getMetaInformation('itemprop', 'duration')
        if length is None:
            return None
        minutes = int(length[2 : length.find('M')])
        seconds = int(length[length.find('M')+1 : length.find('S')])
        return minutes * 60 + seconds

    def getAuthor(self):
        tags = self.soup.find_all('span', class_='yt-user-name')
        if len(tags) > 0:
            return tags[0].text
        else:
            return None
