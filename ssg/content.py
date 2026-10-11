"""
Content model: articles, pages and taxonomy terms.
"""

from dataclasses import dataclass, field
from datetime import datetime

from ssg import config
from ssg.metadata import parse_date, slugify, split_list
from ssg.render import render_formatted, render_source, resolve_links, typogrify


class DuplicateSlugError(ValueError):
    """
    Raised when two content files would write to the same output path.
    """


class MissingSummaryError(ValueError):
    """
    Raised when a published article declares no summary.
    """


class MissingTitleError(ValueError):
    """
    Raised when published content declares no title.
    """


@dataclass(frozen=True)
class Taxonomy:
    """
    A tag, category or author, as referenced by the templates.
    """

    name: str
    kind: str

    @property
    def slug(self):
        """
        Return the term's URL slug.
        """
        return slugify(self.name)

    @property
    def url(self):
        """
        Return the term's index page, relative to the site root.
        """
        return f"{self.kind}/{self.slug}.html"

    def __str__(self):
        return self.name

    def __lt__(self, other):
        # Templates order terms by name with the |sort filter.
        return self.name.lower() < other.name.lower()


@dataclass
class Content:
    """
    A rendered article or page.
    """

    source_path: str
    title: str
    slug: str
    status: str
    content: str
    template: str
    summary: str = None
    date: datetime = None
    category: Taxonomy = None
    author: Taxonomy = None
    tags: list = field(default_factory=list)
    math: bool = False

    @property
    def save_as(self):
        """
        Return the output path for this content.
        """
        return f"{self.slug}.html"

    @property
    def url(self):
        """
        Return this content's URL, relative to the site root.
        """
        return self.save_as

    @property
    def locale_date(self):
        """
        Return the publication date in the site's display format.
        """
        return self.date.strftime(config.DEFAULT_DATE_FORMAT)

    def get_content(self, siteurl, urls):
        """
        Return the body with intra-site links resolved against siteurl.
        """
        return resolve_links(self.content, siteurl, urls)


def _single(meta, name, default=None):
    """
    Return a metadata field joined into one string, or default.
    """
    lines = meta.get(name)
    return "\n".join(lines) if lines else default


def load_one(env, context, path, template):
    """
    Read one content file and return its Content, or None if unpublished.
    """
    html, meta = render_source(env, path, context)

    status = _single(meta, "status", config.DEFAULT_STATUS)
    if status != "published":
        return None

    raw_title = _single(meta, "title", "")
    if not raw_title.strip():
        raise MissingTitleError(f"{path}: content has no Title field")
    title = typogrify(raw_title)

    summary = _single(meta, "summary", "")
    if not summary.strip():
        # Pelican's word-count truncation is not reimplemented, so an article
        # without a summary would be listed and syndicated with an empty one.
        # Pages render no summary, so they are exempt.
        if template == "article":
            raise MissingSummaryError(f"{path}: article has no Summary field")
        summary = None
    else:
        summary = typogrify(render_formatted(summary))

    slug = _single(meta, "slug") or slugify(raw_title)
    date = _single(meta, "date")
    category = _single(meta, "category")
    tags = _single(meta, "tags")

    return Content(
        source_path=str(path),
        title=title,
        slug=slug,
        status=status,
        content=typogrify(html),
        template=template,
        summary=summary,
        date=parse_date(date) if date else None,
        category=Taxonomy(category, "category") if category else None,
        author=Taxonomy(_single(meta, "author", config.AUTHOR), "author"),
        tags=[Taxonomy(t, "tag") for t in split_list(tags)] if tags else [],
        math=_single(meta, "math", "").lower() == "true",
    )


def check_unique_slugs(items):
    """
    Raise DuplicateSlugError if any two items share an output path.

    Content is written before the direct templates, so a slug matching one of
    those would be silently overwritten; such a collision is rejected too.
    """
    reserved = {f"{name}.html": name for name in config.DIRECT_TEMPLATES}
    seen = {}
    for item in items:
        if item.save_as in reserved:
            raise DuplicateSlugError(
                f"{item.source_path} writes to {item.save_as}, which is "
                f"reserved for the {reserved[item.save_as]} template"
            )
        if item.save_as in seen:
            raise DuplicateSlugError(
                f"{item.source_path} and {seen[item.save_as]} both write to "
                f"{item.save_as}"
            )
        seen[item.save_as] = item.source_path
