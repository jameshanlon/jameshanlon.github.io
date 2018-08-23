#!/usr/bin/env python

from __future__ import unicode_literals

AUTHOR = u'James W. Hanlon'
SITENAME = u'James W. Hanlon'
SITEURL = 'http://jameswhanlon.com'

PATH = 'content'
IMAGE_PATH = 'images'
THUMBNAIL_DIR = 'images'
THUMBNAIL_SIZES = { 'thumb': '150x?', }
THUMBNAIL_KEEP_TREE = True
GALLERY_PATH = 'images'

RESIZE = [
    ('gallery', False, 200, 200),
]

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'
DEFAULT_DATE_FORMAT = "%d %b %Y"
DEFAULT_PAGINATION = False

CATEGORY_SAVE_AS = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

MENU_ITEMS = [
    ('notes',    'index.html'),
    ('archive',  'archive.html'),
    ('about',    'about.html'),
]

STATIC_PATHS = [
    'images',
    'files',
    'includes',
    'files/favicon.png',
    'files/robots.txt',
]
ARTICLE_EXCLUDES = [
    'vim-commands',
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
