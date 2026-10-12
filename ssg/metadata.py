"""Front matter value parsing: slugs, list fields and dates."""

import re
from datetime import datetime
from zoneinfo import ZoneInfo

from ssg import config

#: Applied in order to derive a slug from a title.
SLUG_SUBSTITUTIONS = [
    (re.compile(r"[^\w\s-]"), ""),
    (re.compile(r"(?u)\A\s*"), ""),
    (re.compile(r"(?u)\s*\Z"), ""),
    (re.compile(r"[-\s]+"), "-"),
]


class SlugError(ValueError):
    """
    Raised when a title cannot be turned into a usable URL slug.
    """


def slugify(value):
    """
    Return the URL slug for a title.

    Raises SlugError if the result would be empty or contain non-ASCII
    characters, both of which would produce an unusable URL.
    """
    slug = value
    for pattern, replacement in SLUG_SUBSTITUTIONS:
        slug = pattern.sub(replacement, slug)
    slug = slug.lower()
    if not slug:
        raise SlugError(f"title {value!r} produces an empty slug; add a Slug field")
    if not slug.isascii():
        raise SlugError(
            f"title {value!r} produces a non-ASCII slug {slug!r}; add a Slug field"
        )
    return slug


def split_list(value):
    """
    Split a comma- or semicolon-separated metadata field into its entries.

    Semicolons take precedence when present, so that entries may themselves
    contain commas.
    """
    separator = ";" if ";" in value else ","
    return [entry.strip() for entry in value.split(separator) if entry.strip()]


def parse_date(value):
    """
    Return a timezone-aware datetime for a Y-M-D front matter date.

    Month and day need not be zero-padded.
    """
    naive = datetime.strptime(value.strip(), "%Y-%m-%d")
    return naive.replace(tzinfo=ZoneInfo(config.TIMEZONE))
