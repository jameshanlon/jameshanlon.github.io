"""
Render content files: Jinja2, then Markdown, then typogrify.
"""

import re
from posixpath import join as urljoin

import smartypants
from jinja2 import ChoiceLoader, Environment, FileSystemLoader
from markdown import Markdown, markdown
from typogrify.filters import typogrify as _typogrify

from ssg import config

# smartypants exposes its configuration as a module global, so set it once
# rather than per call. Attr.w additionally converts &quot; entities.
smartypants.Attr.default = smartypants.Attr.set1 | smartypants.Attr.w

#: Matches a Pelican-style intra-site link, e.g. {filename}/led-driver.md
LINK_MARKER = re.compile(r"\{filename\}/?(?P<target>[^\"'#?]+)")


class LinkError(ValueError):
    """
    Raised when an intra-site link names a file that does not exist.
    """


def build_environment(filters):
    """
    Return the Jinja2 environment used to render content and templates.
    """
    loaders = [
        FileSystemLoader(config.CONTENT_DIR),
        FileSystemLoader(config.THEME_DIR / "templates"),
    ]
    env = Environment(
        loader=ChoiceLoader(loaders), trim_blocks=True, lstrip_blocks=True
    )
    env.filters.update(filters)
    return env


def render_source(env, path, context):
    """
    Render a content file and return its HTML body and raw metadata.

    The file is rendered as a Jinja2 template first, so that content may use
    macros and filters, then converted from Markdown. Metadata is extracted by
    Markdown's meta extension, giving each field as a list of lines.
    """
    source = path.read_text(encoding="utf-8").lstrip("﻿")
    rendered = env.from_string(source).render(**context)
    md = Markdown(**config.MARKDOWN)
    html = md.convert(rendered)
    return html, getattr(md, "Meta", {})


def render_formatted(value):
    """
    Convert a metadata value from Markdown to HTML.
    """
    md = Markdown(**config.MARKDOWN)
    md.preprocessors.deregister("meta")
    return md.convert(value)


def render_markdown(text):
    """
    Convert a string to HTML using Markdown's default settings.

    The `markdown` Jinja filter, used by content/pages/code.md to render
    project descriptions from YAML. Deliberately not the configured extension
    set, matching pelicanconf.py's render_markdown.
    """
    return markdown(text.strip())


def typogrify(text):
    """
    Apply typographic refinements to rendered HTML.
    """
    return _typogrify(text)


def resolve_links(html, siteurl, urls):
    """
    Replace intra-site link markers with URLs resolved against siteurl.

    Pass "." for a page at the output root, ".." for one a directory deep, or
    the absolute site URL for feeds.
    """

    def replace(match):
        target = match.group("target")
        if target not in urls:
            raise LinkError(f"intra-site link to missing file: {target}")
        return urljoin(siteurl, urls[target])

    return LINK_MARKER.sub(replace, html)
