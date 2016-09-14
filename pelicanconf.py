#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'James Hanlon'
SITENAME = u'James Hanlon'
SITEURL = 'http://jwhanlon.com'

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'
DEFAULT_DATE_FORMAT = "%d %b %Y"
DEFAULT_PAGINATION = False

MENUITEMS = [
    ('blog',    '/'),
    ('about',   '/pages/about.html'),
    ('archive', '/pages/archive.html'),
    ('links',   '/pages/links.html'),
]

STATIC_PATHS = [
    'images',
    'files',
]

THEME = 'theme'

TYPOGRIFY = True

RELATIVE_URLS = True

FEED_ATOM = 'reeds/atom.xml'
FEED_RSS = 'reeds/rss.xml'
