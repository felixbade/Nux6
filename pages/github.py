#!/usr/bin/env python
# -*- coding: utf-8 -*-

from page import Page

class GitHub(Page):

    def getBanner(self):
        return 'GitHub'

    def getInfo(self):
        if self.getMetaInformation('name', 'octolytics-dimension-repository_id') is None:
            return None
        user = self.getMetaInformation('name', 'octolytics-dimension-user_login')
        description = self.getMetaInformation('name', 'description')
        return '%s/%s' % (user, description)
