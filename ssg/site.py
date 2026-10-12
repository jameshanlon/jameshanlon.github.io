"""
Build the site: load content, build indexes, write output.
"""

from pathlib import Path

import yaml

from ssg import config
from ssg.assets import Assets
from ssg.content import check_unique_slugs, load_one
from ssg.feeds import write_feeds
from ssg.render import build_environment, render_markdown


def relative_siteurl(save_as):
    """
    Return the SITEURL for a file written to save_as, as a relative path.
    """
    depth = save_as.count("/")
    return "." if depth == 0 else "/".join([".."] * depth)


def _group(articles, terms_of):
    """
    Group articles by taxonomy term, preserving the article ordering.

    Returns a list of (term, articles) pairs, which is what the templates'
    `{% for term, articles in tags|sort %}` expects.
    """
    grouped = {}
    for article in articles:
        for term in terms_of(article):
            grouped.setdefault(term, []).append(article)
    return list(grouped.items())


class _Bound:
    """
    An article or page with its links already resolved for one output file.
    """

    def __init__(self, item, body):
        self._item = item
        self.content = body

    def __getattr__(self, name):
        return getattr(self._item, name)


class Site:
    """
    One build of the site.
    """

    def __init__(self, output_dir=None):
        """
        Prepare the output directory, Jinja environment and shared data.
        """
        self.output_dir = Path(output_dir or config.OUTPUT_DIR)
        self.assets = Assets(self.output_dir)
        filters = dict(self.assets.filters())
        filters["load_yaml"] = lambda name: yaml.safe_load(Path(name).read_text())
        filters["markdown"] = render_markdown
        filters["strftime"] = lambda value, fmt: value.strftime(fmt)
        self.env = build_environment(filters)
        self.context = {
            "code": yaml.safe_load(Path("content/pages/code.yml").read_text()),
            "links": yaml.safe_load(Path("content/pages/links.yml").read_text()),
        }
        self.env.globals.update(self.context)

    def build(self):
        """
        Generate the whole site into the output directory.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
        articles, pages = self._load()
        check_unique_slugs(articles + pages)
        urls = self._link_targets(articles, pages)
        self._write_content(articles, pages, urls)
        self._write_indexes(articles)
        write_feeds(self, articles, urls)
        self.assets.copy_static()

    def _load(self):
        """
        Load every published article and page, newest article first.
        """
        articles, pages = [], []
        for path in sorted(config.CONTENT_DIR.glob("*.md")):
            content = load_one(self.env, self.context, path, "article")
            if content:
                articles.append(content)
        for path in sorted((config.CONTENT_DIR / "pages").glob("*.md")):
            content = load_one(self.env, self.context, path, "page")
            if content:
                pages.append(content)
        articles.sort(key=lambda a: a.date, reverse=True)
        return articles, pages

    def _link_targets(self, articles, pages):
        """
        Map a source path, as written in a {filename} link, to its URL.
        """
        targets = {}
        for item in articles + pages:
            relative = Path(item.source_path).relative_to(config.CONTENT_DIR)
            targets[relative.as_posix()] = item.url
            targets[relative.name] = item.url
        return targets

    def _base_context(self):
        """
        Return the config values every template expects.
        """
        return {
            name: getattr(config, name)
            for name in (
                "SITENAME",
                "AUTHOR",
                "SITEURL",
                "FEED_DOMAIN",
                "FEED_ATOM",
                "FEED_RSS",
                "DEFAULT_LANG",
                "MENU_ITEMS",
            )
        }

    def _render(self, template, save_as, **extra):
        """
        Render one template and write it to save_as.
        """
        context = self._base_context()
        context.update(extra)
        context["SITEURL"] = relative_siteurl(save_as)
        context["output_file"] = save_as

        target = self.output_dir / save_as
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            self.env.get_template(f"{template}.html").render(**context),
            encoding="utf-8",
        )

    def _write_content(self, articles, pages, urls):
        """
        Write every article and page.
        """
        for item in articles + pages:
            body = item.get_content(relative_siteurl(item.save_as), urls)
            self._render(
                item.template,
                item.save_as,
                **{item.template: _Bound(item, body)},
            )

    def _write_indexes(self, articles):
        """
        Write the direct templates and the per-term taxonomy pages.
        """
        tags = _group(articles, lambda a: a.tags)
        categories = _group(articles, lambda a: [a.category] if a.category else [])
        authors = _group(articles, lambda a: [a.author] if a.author else [])

        shared = {
            "articles": articles,
            "dates": articles,
            "tags": tags,
            "categories": categories,
            "authors": authors,
        }

        for template in config.DIRECT_TEMPLATES:
            self._render(template, f"{template}.html", **shared)

        for kind, terms in (
            ("tag", tags),
            ("category", categories),
            ("author", authors),
        ):
            for term, items in terms:
                self._render(
                    kind, term.url, **{**shared, kind: term, "articles": items}
                )
