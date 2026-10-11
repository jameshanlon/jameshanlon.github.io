#!/usr/bin/env python
"""Write Pelican-derived slugs and summaries into content front matter."""

import glob
import re
import sys

from pelican.settings import read_settings
from pelican.utils import slugify

SETTINGS = read_settings("pelicanconf.py")
SUBSTITUTIONS = SETTINGS["SLUG_REGEX_SUBSTITUTIONS"]

# Hand-written replacements for the two articles that currently rely on
# Pelican truncating rendered HTML at SUMMARY_MAX_LENGTH words. The four
# pages have no summary and none is rendered, so they are left alone.
SUMMARIES = {
    "content/xmp64.md": "An overview of the XMOS XMP-64 development board, a "
    "64-core parallel machine built from sixteen four-core XS1-G4 devices.",
    "content/ml-challenges.md": "Neural networks are developing rapidly and "
    "place new demands on computer architecture. A survey of where those "
    "demands fall and which of them are hard.",
}


def field(text, name):
    """Return the single-line value of a front matter field, or None."""
    match = re.search(rf"^{name}:[ \t]*(.*)$", text, re.M)
    return match.group(1).strip() if match else None


def insert_after(text, anchor, line):
    """Insert line immediately after the front matter field named anchor."""
    pattern = rf"^({anchor}:[^\n]*(?:\n[ \t]+[^\n]*)*)\n"
    return re.sub(pattern, rf"\1\n{line}\n", text, count=1, flags=re.M)


def main():
    paths = sorted(glob.glob("content/*.md")) + sorted(glob.glob("content/pages/*.md"))
    for path in paths:
        with open(path) as f:
            text = f.read()

        title = field(text, "Title")
        if title is None:
            sys.exit(f"{path}: no Title field")

        if field(text, "Slug") is None:
            slug = slugify(title, SUBSTITUTIONS)
            text = insert_after(text, "Title", f"Slug: {slug}")

        if field(text, "Summary") is None and not path.startswith("content/pages/"):
            summary = SUMMARIES.get(path)
            if summary is None:
                sys.exit(f"{path}: no Summary field and no replacement defined")
            text = insert_after(text, "Title", f"Summary: {summary}")

        with open(path, "w") as f:
            f.write(text)

    print(f"Froze metadata in {len(paths)} files")


if __name__ == "__main__":
    main()
