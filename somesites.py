#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urlparse

from pages.youtube import YouTube
from pages.ted import TED
from pages.iltasanomat import IltaSanomat
from pages.github import GitHub
from pages.speedtest import Speedtest

def getSiteName(site):
    if site == 'www.youtube.com':
        return 'You\x034Tube'
    elif site == 'www.ted.com':
        return '\x034TED'
    elif site.endswith('wikipedia.org'):
        return 'Wikipedia'
    elif site == 'www.iltasanomat.fi':
        return '\x034Ilta-Sanomat'
    elif site == 'github.com':
        return 'GitHub'
    elif site == 'www.speedtest.net':
        return '\x0312Speedtest.net'

def getInfo(url, soup):
    try:
        parsed = urlparse.urlparse(url)
        domain = parsed.hostname
        path = parsed.path[1:]
        if domain == 'www.youtube.com':
            return YouTube(soup).getInfo()
        elif domain == 'www.ted.com':
            return TED(soup).getInfo()
        elif domain == 'www.iltasanomat.fi':
            return IltaSanomat(soup).getInfo()
        elif domain == 'github.com':
            return GitHub(soup).getInfo()
        elif domain == 'www.speedtest.net':
            return Speedtest(soup).getInfo()
    except:
        return None
