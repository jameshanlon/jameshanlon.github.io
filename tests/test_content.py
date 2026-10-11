import pytest

from ssg.content import (
    DuplicateSlugError,
    MissingSummaryError,
    check_unique_slugs,
    load_one,
)
from ssg.render import build_environment
from ssg.site import relative_siteurl


def test_relative_siteurl_is_dot_at_the_output_root():
    assert relative_siteurl("notes.html") == "."


def test_relative_siteurl_is_dotdot_one_directory_deep():
    assert relative_siteurl("tag/computing.html") == ".."


def test_duplicate_slugs_are_reported_with_both_source_files():
    # Two titles can slugify to the same value; silently overwriting one
    # output would lose an article.
    class Stub:
        def __init__(self, slug, source_path):
            self.slug = slug
            self.source_path = source_path
            self.save_as = f"{slug}.html"

    items = [Stub("same", "content/a.md"), Stub("same", "content/b.md")]
    with pytest.raises(DuplicateSlugError) as excinfo:
        check_unique_slugs(items)

    message = str(excinfo.value)
    assert "content/a.md" in message and "content/b.md" in message


def test_unique_slugs_are_accepted():
    class Stub:
        def __init__(self, slug):
            self.slug = slug
            self.source_path = f"content/{slug}.md"
            self.save_as = f"{slug}.html"

    check_unique_slugs([Stub("one"), Stub("two")])


def test_content_without_a_status_field_is_not_published(tmp_path):
    # Forgetting Status must leave an article unpublished, not crash and not
    # publish it by accident.
    source = tmp_path / "note.md"
    source.write_text("Title: A note\nDate: 2024-01-01\n\nBody text.\n")
    env = build_environment({})

    assert load_one(env, {}, source, "article") is None


def test_published_article_without_a_summary_fails_the_build(tmp_path):
    # Pelican truncated the body to make one; nothing does that now, so the
    # omission must be loud rather than syndicating an empty summary.
    source = tmp_path / "note.md"
    source.write_text(
        "Title: A note\nDate: 2024-01-01\nStatus: published\n\nBody text.\n"
    )
    env = build_environment({})

    with pytest.raises(MissingSummaryError, match="note.md"):
        load_one(env, {}, source, "article")


def test_published_page_without_a_summary_is_allowed(tmp_path):
    # Pages render no summary, so they are exempt.
    source = tmp_path / "page.md"
    source.write_text("Title: A page\nStatus: published\n\nBody text.\n")
    env = build_environment({})

    assert load_one(env, {}, source, "page").summary is None


def test_content_marked_published_is_loaded(tmp_path):
    source = tmp_path / "note.md"
    source.write_text(
        "Title: A note\nDate: 2024-01-01\nStatus: published\n"
        "Summary: A short note.\n\nBody text.\n"
    )
    env = build_environment({})

    content = load_one(env, {}, source, "article")

    assert content.slug == "a-note"
    assert content.save_as == "a-note.html"
