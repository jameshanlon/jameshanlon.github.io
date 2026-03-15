#!/usr/bin/env python

from __future__ import unicode_literals
import sys
import os
import logging
import yaml

sys.path.insert(0, os.getcwd())
import markdown as md
from thumbnail import get_thumbnail, get_image


def render_markdown(text):
    return md.markdown(text.strip())

AUTHOR = "James W. Hanlon"
SITENAME = "James W. Hanlon"
SITEURL = "https://jameswhanlon.com"

REMOTE_PREFIX = "https://jwh.ams3.digitaloceanspaces.com/homepage"


def get_asset_url(filepath):
    return REMOTE_PREFIX + "/" + filepath


def load_yaml(filename: str):
    with open(filename, "r") as f:
        return yaml.safe_load(f)


JINJA_CONTEXT = {
    "code": load_yaml("content/pages/code.yml"),
    "links": load_yaml("content/pages/links.yml"),
}

JINJA_GLOBALS = JINJA_CONTEXT

JINJA_FILTERS = {
    "asset": get_asset_url,
    "thumbnail": get_thumbnail,
    "image": get_image,
    "load_yaml": load_yaml,
    "markdown": render_markdown,
}

PATH = "content"
IMAGE_PATH = "images"
THUMBNAIL_DIR = "images"
THUMBNAIL_SIZES = {
    "thumb": "150x?",
}
THUMBNAIL_KEEP_TREE = True
GALLERY_PATH = "images"

RESIZE = [
    ("gallery", False, 200, 200),
]

TIMEZONE = "Europe/Paris"

DEFAULT_LANG = "en"
DEFAULT_DATE_FORMAT = "%d %b %Y"
DEFAULT_PAGINATION = False

PAGE_SAVE_AS = "{slug}.html"

MENU_ITEMS = [
    ("about", "index.html"),
    ("notes", "notes.html"),
    ("code", "code.html"),
    ("links", "links.html"),
    ("archive", "archive.html"),
]

DIRECT_TEMPLATES = ["index", "tags", "categories", "authors", "archives", "notes"]
NOTES_SAVE_AS = "notes.html"

STATIC_PATHS = [
    "files",
    "CNAME",
]

ARTICLE_EXCLUDES = [
    "vim-commands",  # vim-commands directory
]

EXTRA_PATH_METADATA = {
    "theme/static/files/robots.txt": {"path": "robots.txt"},
    "theme/static/images/favicon-16x16.png": {"path": "favicon-16x16.png"},
    "theme/static/images/favicon-32x32.png": {"path": "favicon-32x32.png"},
}

DEFAULT_METADATA = {
    "status": "draft",
}

THEME = "theme"

TYPOGRIFY = True

RELATIVE_URLS = True

FEED_ATOM = "reeds/atom.xml"
FEED_RSS = "reeds/rss.xml"

SUMMARY_MAX_LENGTH = 25

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["jinja_content"]
