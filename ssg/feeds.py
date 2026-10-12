"""
Syndication feeds.
"""

from posixpath import join as urljoin

from feedgenerator import Atom1Feed, Rss201rev2Feed, get_tag_uri
from markupsafe import Markup

from ssg import config


def entry_id(link, date):
    """
    Return the tag URI used as a feed entry's unique id.
    """
    return get_tag_uri(link, date)


def _add_item(feed, item, urls, is_rss):
    """
    Add one article to a feed.
    """
    link = urljoin(config.FEED_DOMAIN, item.url)

    if is_rss:
        # RSS carries only the summary, in its single description element.
        description, content = item.summary, None
    else:
        # Atom carries the body, plus a summary only if it differs from it.
        content = item.get_content(config.FEED_DOMAIN, urls)
        description = item.summary if item.summary != content else None

    categories = [str(item.category)] if item.category else []
    categories += [str(tag) for tag in item.tags]

    feed.add_item(
        title=Markup(item.title).striptags(),
        link=link,
        unique_id=entry_id(link, item.date),
        description=description,
        content=content,
        categories=categories or None,
        author_name=str(item.author) if item.author else "",
        pubdate=item.date,
    )


def _build(articles, urls, path, title, is_rss):
    """
    Return a populated feed object for the given articles.
    """
    feed_class = Rss201rev2Feed if is_rss else Atom1Feed
    feed = feed_class(
        title=title,
        link=f"{config.FEED_DOMAIN}/",
        feed_url=urljoin(config.FEED_DOMAIN, path),
        description="",
        subtitle=None,
    )
    for article in articles[: config.FEED_MAX_ITEMS]:
        _add_item(feed, article, urls, is_rss)
    return feed


def _group(articles, term_of):
    """
    Group articles by a single taxonomy term, preserving article ordering.
    """
    grouped = {}
    for article in articles:
        term = term_of(article)
        if term:
            grouped.setdefault(term, []).append(article)
    return grouped.items()


def write_feeds(site, articles, urls):
    """
    Write every feed the site publishes.
    """
    # A per-term feed is titled "SITENAME - term"; site-wide feeds are not.
    feeds = [
        (config.FEED_ATOM, articles, None, False),
        (config.FEED_RSS, articles, None, True),
        ("feeds/all.atom.xml", articles, None, False),
        (f"feeds/all-{config.DEFAULT_LANG}.atom.xml", articles, None, False),
    ]
    for term, items in _group(articles, lambda a: a.category):
        feeds.append((f"feeds/{term.slug}.atom.xml", items, term.name, False))
    for term, items in _group(articles, lambda a: a.author):
        feeds.append((f"feeds/{term.slug}.atom.xml", items, term.name, False))
        feeds.append((f"feeds/{term.slug}.rss.xml", items, term.name, True))

    for path, items, feed_title, is_rss in feeds:
        title = config.SITENAME
        if feed_title:
            title += f" - {Markup(feed_title).striptags()}"
        target = site.output_dir / path
        target.parent.mkdir(parents=True, exist_ok=True)
        feed = _build(items, urls, path, title, is_rss)
        target.write_text(feed.writeString("utf-8"), encoding="utf-8")
