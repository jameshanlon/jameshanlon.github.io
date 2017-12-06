#!/usr/bin/env python

from __future__ import unicode_literals

AUTHOR = u'James W. Hanlon'
SITENAME = u'James W. Hanlon'
SITEURL = 'http://jwhanlon.com'

PATH = 'content'
IMAGE_PATH = 'images'
THUMBNAIL_DIR = 'images'
THUMBNAIL_KEEP_NAME = True
THUMBNAIL_KEEP_TREE = True
GALLERY_PATH = 'images'

RESIZE = [
    ('', False, 200, 200),
]

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'
DEFAULT_DATE_FORMAT = "%d %b %Y"
DEFAULT_PAGINATION = False

MENU_ITEMS = [
    ('notes',    'index.html'),
    ('projects', 'pages/projects.html'),
    ('archive',  'pages/archive.html'),
    ('about',    'pages/about.html'),
]

STATIC_PATHS = [
    'images',
    'files/favicon.png',
    'files/robots.txt',
]
EXTRA_PATH_METADATA = {
    'files/robots.txt': {'path': 'robots.txt'},
    'files/favicon.png': {'path': 'favicon.png'},
}

THEME = 'theme'

TYPOGRIFY = True

RELATIVE_URLS = True

FEED_ATOM = 'reeds/atom.xml'
FEED_RSS = 'reeds/rss.xml'

PLUGIN_PATHS = ['pelican-plugins', ]
PLUGINS = ['thumbnailer', 'gallery', 'jinja2content']
