#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from urllib import quote_plus
import json

def shorten(url, name=None):
    data = {'url': url}
    if name is not None:
        data.update({'name': quote_plus(name)})
    request = urllib2.Request('http://api.lyli.fi', json.dumps(data), {'Content-Type': 'application/json'})
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        response = e
    result = json.loads(response.read())
    if 'error' in result:
        return result['error']
    return result['short-url']

def shorten_tinyurl(url, alias=None):
    tinyurl_url = 'http://tinyurl.com/create.php?source=indexpage&url=' + urllib2.quote(url)
    if alias is not None:
        tinyurl_url += '&alias=' + urllib2.quote(alias)
    page = urllib2.urlopen(tinyurl_url).read()
    page = page[page.find('preview.tinyurl') + 20:]
    url = 'http://tinyurl.com/' + page[:page.find('<')]
    return url
