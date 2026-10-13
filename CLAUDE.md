# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Git Conventions

- All commits are authored by James Hanlon <mail@jameswhanlon.com>.
- Do not add `Co-Authored-By` trailers to commit messages.
- Do not add session URLs or other tool-generated links to commit messages.

Set the author identity in a fresh clone before committing:

```bash
git config user.name "James Hanlon"
git config user.email mail@jameswhanlon.com
```

## Overview

Personal homepage built with an in-repo static site generator, `ssg/`. Source lives in `content/` and `theme/`; output is generated into `output/`. The theme uses hand-written CSS with no framework dependencies. GLightbox is loaded from jsDelivr CDN for image lightboxes.

## Setup

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
pre-commit install
```

## Build Commands

```bash
make html        # Generate site with ssg
make all         # Same as make html (default target)
make serve       # Run dev server at http://0.0.0.0:8000, rebuilding on change with --watch
make test        # Run the test suite, including the URL surface check
make manifest    # Regenerate tests/url_manifest.txt from the current output/
make clean       # Remove output/
```

`make serve` runs `ssg serve --watch`; without `--watch` the dev server serves the current build without rebuilding.

## Architecture

### Content Pipeline

`ssg/` is a small, purpose-built static site generator. Each content file is rendered as a **Jinja2 template first**, then as Markdown. This means content files can use Jinja2 syntax, access custom filters, and reference shared data.

Modules:
- `ssg/config.py` — site-wide settings (author, URLs, menu, Markdown extensions)
- `ssg/content.py` — loads and parses articles and pages from `content/`
- `ssg/metadata.py` — front matter parsing: slugs, list fields, dates
- `ssg/render.py` — Markdown/Jinja rendering, typogrify, intra-site link resolution
- `ssg/assets.py` — asset filters: remote URLs, local image copies, thumbnails
- `ssg/feeds.py` — Atom and RSS feed generation
- `ssg/site.py` — ties the above together to build the full output tree
- `ssg/__main__.py` — the `ssg build`/`ssg serve` CLI, driven by the Makefile

Custom Jinja filters, provided by `Assets` in `ssg/assets.py`:
- `asset` — returns a remote URL on DigitalOcean Spaces (`https://jwh.ams3.digitaloceanspaces.com/homepage/...`)
- `thumbnail` — generates a thumbnail (from local file or remote fetch) and returns its path
- `image` — copies local image to `output/images/` or falls back to remote URL

A `load_yaml` filter loads a YAML file and returns its data; `projects` (from `content/pages/projects.yml`) is injected into all templates.

`tests/url_manifest.txt` is the committed URL contract for the site: it lists every output path and a hash of its contents. `tests/test_url_surface.py` fails the build if a URL appears, disappears, or changes content without the manifest being regenerated (`make manifest`) and reviewed — this is the main guard against unintended regressions.

### Content Files

Articles live directly in `content/` as `.md` files. Required frontmatter:
```
Title: ...
Date: YYYY-MM-DD
Category: notes
Tags: tag1, tag2
Summary: ...
Status: published   ← required; default is "draft" so articles won't appear until set
```

Optional frontmatter:
- `Math: true` — loads MathJax 3 for articles that use LaTeX math (`$...$` inline)

Pages live in `content/pages/` and are rendered as standalone pages (e.g. `about.md`, `projects.md`).

### Theme

`theme/templates/` — Jinja2 HTML templates; `base.html` is the root layout.
`theme/static/` — CSS and images.

The site uses a light theme. The navigation bar uses a CSS-only hamburger menu (hidden checkbox trick) for mobile — no JavaScript needed. Pygments syntax highlighting uses `pygments.css` with bare selectors (light mode only).

Image lightboxes use [GLightbox](https://biati-digital.github.io/glightbox/) — links need `class="glightbox"` and `data-gallery="name"` attributes.

Analytics via [GoatCounter](https://www.goatcounter.com/).

### Images

Images can be stored locally in `content/images/` (for development) or hosted remotely on DigitalOcean Spaces. `ssg/assets.py` checks for a local copy first and falls back to fetching remotely. This means the build works offline if images are present locally, and works without local images by fetching from the remote store.

To regenerate Pygments CSS after changing themes, generate light-mode rules with bare selectors into `pygments.css`.

Image conversion utilities (from `NOTES.md`):
```bash
mogrify -format jpg *.HEIC                                # HEIC → JPG (requires imagemagick)
sips -Z 1024 *.jpg                                        # Resize to 1024px wide (macOS)
convert -resize 1000x -density 150 -trim in.svg out.png  # SVG/PDF → PNG
```

### Source Files

`source-files/` contains article source assets (.graffle, .drawio, presentation files) that are not part of the published site.
