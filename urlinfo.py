#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urlparse
import urllib2
import httplib
import socket
import re
import math
import unicodedata

from bs4 import BeautifulSoup

import somesites

def removeControlCharacters(string):
    return "".join(char for char in string if unicodedata.category(char)[0] != 'C')

def removeExtraSpaces(string):
    return re.sub(r'  *', r' ', string).strip(' ')

class URLInfo:

    def __init__(self, url):
        self.timeout=10
        a = urlparse.urlparse(url)
        domain = unicode(a.hostname, 'utf-8').encode('idna')
        self.domain = domain
        netloc = domain
        try:
            if a.port:
                netloc = netloc + ':' + str(a.port)
        except ValueError:
            pass
        self.url = urlparse.SplitResult(scheme=a.scheme, netloc=netloc,
                path=a.path, query=a.query, fragment=a.fragment).geturl()
        print self.url

    def getInfo(self):
        # Valid HTTP response
        try:
            return self.getPageInfo()
        except urllib2.HTTPError as error:
            return self.getHTTPErrorMessage(error)

        # Invalid HTTP response
        except urllib2.URLError as error:
            return self.getURLErrorMessage(error)
        except httplib.BadStatusLine as error:
            return self.getURLErrorMessage(error)
        except socket.error as error:
            return self.getURLErrorMessage(error)

    def getPageInfo(self):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        http = opener.open(self.url, timeout=self.timeout)

        headers = http.info()
        if headers.status == 'EOF in headers':
            return self.getNotAWebServerMessage()
        
        self.url = http.geturl()
        self.domain = urlparse.urlparse(self.url).netloc
        self.path = urlparse.urlparse(self.url).path
        type = self.getFileTypeFromHTTPHeaders(headers)
        if type in ['text/html', 'application/xhtml+xml']:
            return self.getBanner() + self.getHTMLPageInfo(http)
        else:
            return self.getBanner() + self.getNonHTMLPageInfo(http)

    def getHTMLPageInfo(self, http):
        soup = BeautifulSoup(http.read())
        info = somesites.getInfo(self.url, soup)
        if info is not None:
            return info
        elif soup.title is not None:
            title = soup.title.text
            title = removeControlCharacters(title)
            title = removeExtraSpaces(title)
            return title
        else:
            return 'No title.'

    def getNonHTMLPageInfo(self, http):
        headers = http.info()
        length = self.getHumanReadableFileSizeFromHTTPHeaders(headers)
        filetype = self.getFileTypeFromHTTPHeaders(headers)
        return '%s (%s)' % (filetype, length)

    def getHumanReadableFileSizeFromHTTPHeaders(self, headers):
        lengthlist = headers.getheaders('Content-Length')
        if len(lengthlist) == 0:
            return 'unknown file size'
        else:
            kb = int(lengthlist[0]) / 1000.0
            def f(number):
                if number < 10:
                    return str(round(number, 1))
                else:
                    return str(int(round(number, 1 - int(math.log10(number)))))
            if kb < 1e3:
                return f(kb) + ' kB'
            elif kb < 1e6:
                return f(kb/1000) + ' MB'
            elif kb < 1e9:
                return f(kb/1000000) + ' GB'

    def getFileTypeFromHTTPHeaders(self, headers):
        types = headers.getheaders('Content-Type')
        if len(types) > 0:
            return types[0].split(';')[0]
        else:
            return 'unknown file type'

    def getHTTPErrorMessage(self, error):
        return self.getBanner() + '\x034%d - %s\x0f' % (error.code, error.msg)

    def getURLErrorMessage(self, error):
        # The errors are not formatted in the same way.
        # First try to find out what kind of error this is.
        if error.__class__ == httplib.BadStatusLine:
            return self.getNotAWebServerMessage()
        elif error.__class__ == urllib2.URLError:
            if str(error.reason) == 'timed out':
                return 'Connection timed out to %s' % self.getHilightedDomain()
            elif error.reason[1] == 'nodename nor servname provided, or not known':
                return 'Domain %s does not exist' % self.getHilightedDomain()
        elif error.__class__ == socket.timeout:
            return 'Connection timed out to %s' % self.getHilightedDomain()
        return 'Could not connect to %s' % self.getHilightedDomain()
    
    def getBanner(self):
        site = somesites.getSiteName(self.domain)
        if site is None:
            site = self.getHilightedDomain()
        return '\x0314[\x03\x02%s\x0314]\x0f ' % site

    def getNotAWebServerMessage(self):
        return '%s is not a web server' % self.getHilightedDomain()

    def getHilightedDomain(self):
        return '\x02' + self.domain.decode('idna') + '\x0g'
