"""Site configuration."""

from pathlib import Path

AUTHOR = "James W. Hanlon"
SITENAME = "James W. Hanlon"
SITEURL = "https://jameswhanlon.com"
FEED_DOMAIN = SITEURL

REMOTE_PREFIX = "https://jwh.ams3.digitaloceanspaces.com/homepage"

CONTENT_DIR = Path("content")
THEME_DIR = Path("theme")
OUTPUT_DIR = Path("output")

TIMEZONE = "Europe/Paris"
DEFAULT_LANG = "en"
DEFAULT_DATE_FORMAT = "%d %b %Y"

# Content without an explicit Status is unpublished.
DEFAULT_STATUS = "draft"

FEED_ATOM = "reeds/atom.xml"
FEED_RSS = "reeds/rss.xml"
FEED_MAX_ITEMS = 100

MENU_ITEMS = [
    ("about", "index.html"),
    ("notes", "notes.html"),
    ("code", "code.html"),
    ("links", "links.html"),
    ("archive", "archive.html"),
]

DIRECT_TEMPLATES = ["index", "tags", "categories", "authors", "archives", "notes"]

# The extensions list is explicit and load-bearing: passing extension_configs
# alone to Markdown() loads nothing, silently dropping tables, footnotes,
# fenced code and syntax highlighting.
MARKDOWN = {
    "extensions": [
        "markdown.extensions.codehilite",
        "markdown.extensions.extra",
        "markdown.extensions.meta",
    ],
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
    },
    "output_format": "html5",
}

# Static trees copied verbatim from CONTENT_DIR into the output root.
STATIC_PATHS = ["files", "CNAME"]
