#!/usr/bin/env python
# -*- coding: utf-8 -*-

from page import Page

class IltaSanomat(Page):

    def getBanner(self):
        return '\033[91mIlta-Sanomat'

    def getInfo(self):
        title = self.getTitle()
        if title is None:
            return None
        date = self.getRelativeDate()
        return '%s (%s)' % (title, date)

    def getTitle(self):
        titles = self.soup.find_all('h1')
        if len(titles) == 0:
            return None
        return titles[0].text

    def getAbsoluteDate(self):
        tags = self.soup.find_all('div', class_='date')
        if len(tags) == 0:
            return None
        else:
            return tags[0].text.split(':')[1].split()[0]
