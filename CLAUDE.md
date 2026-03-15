# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal homepage built with [Pelican](https://blog.getpelican.com/) (Python static site generator). Source lives in `content/` and `theme/`; output is generated into `output/`. The theme uses hand-written CSS with no framework dependencies. GLightbox is loaded from jsDelivr CDN for image lightboxes.

## Setup

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
pre-commit install
```

## Build Commands

```bash
make html        # Generate site with Pelican
make all         # Same as make html (default target)
make serve       # Run dev server at http://0.0.0.0:8000 with auto-rebuild
make validate    # Build then run html5validator on output/
make clean       # Remove output/
```

For development, `pelican --listen` (without `-r`) serves without watching for changes. `make serve` adds `-r` for auto-regeneration.

## Architecture

### Content Pipeline

The `jinja_content` plugin (`plugins/jinja_content/`) intercepts Pelican's readers and renders each Markdown/RST/HTML file as a **Jinja2 template first**, then as normal Markdown. This means content files can use Jinja2 syntax, access custom filters, and reference shared data.

Custom Jinja filters defined in `pelicanconf.py`:
- `asset` — returns a remote URL on DigitalOcean Spaces (`https://jwh.ams3.digitaloceanspaces.com/homepage/...`)
- `thumbnail` — generates a thumbnail (from local file or remote fetch) and returns its path; implemented in `thumbnail.py`
- `image` — copies local image to `output/images/` or falls back to remote URL; implemented in `thumbnail.py`
- `load_yaml` — loads a YAML file and returns its data

`JINJA_CONTEXT` in `pelicanconf.py` injects `projects` (from `content/pages/projects.yml`) into all templates.

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

Images can be stored locally in `content/images/` (for development) or hosted remotely on DigitalOcean Spaces. `thumbnail.py` checks for a local copy first and falls back to fetching remotely. This means the build works offline if images are present locally, and works without local images by fetching from the remote store.

To regenerate Pygments CSS after changing themes, generate light-mode rules with bare selectors into `pygments.css`.

Image conversion utilities (from `NOTES.md`):
```bash
mogrify -format jpg *.HEIC                                # HEIC → JPG (requires imagemagick)
sips -Z 1024 *.jpg                                        # Resize to 1024px wide (macOS)
convert -resize 1000x -density 150 -trim in.svg out.png  # SVG/PDF → PNG
```

### Source Files

`source-files/` contains article source assets (.graffle, .drawio, presentation files) that are not part of the published site.
