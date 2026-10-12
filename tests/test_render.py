import pytest

from ssg.render import (
    LinkError,
    render_formatted,
    render_markdown,
    resolve_links,
    typogrify,
)


def test_typogrify_wraps_acronyms_in_caps_spans():
    assert 'class="caps"' in typogrify("<p>A RISC-V core.</p>")


def test_typogrify_inserts_a_widont_nbsp_before_the_last_word():
    assert "&nbsp;" in typogrify("<p>one two three four five</p>")


def test_typogrify_converts_straight_quotes_to_smart_quotes():
    assert "&#8217;" in typogrify("<p>one year's data</p>")


def test_resolve_links_makes_intrasite_links_relative_for_pages():
    html = '<a href="{filename}/led-driver.md">driver</a>'
    urls = {"led-driver.md": "three-channel-high-power-led-driver.html"}
    assert resolve_links(html, ".", urls) == (
        '<a href="./three-channel-high-power-led-driver.html">driver</a>'
    )


def test_resolve_links_makes_intrasite_links_absolute_for_feeds():
    html = '<a href="{filename}/led-driver.md">driver</a>'
    urls = {"led-driver.md": "three-channel-high-power-led-driver.html"}
    assert resolve_links(html, "https://jameswhanlon.com", urls) == (
        '<a href="https://jameswhanlon.com/three-channel-high-power-led-driver.html">'
        "driver</a>"
    )


def test_resolve_links_rejects_a_link_to_a_file_that_does_not_exist():
    html = '<a href="{filename}/no-such-note.md">x</a>'
    with pytest.raises(LinkError, match="no-such-note.md"):
        resolve_links(html, ".", {})


TABLE = "| a | b |\n| --- | --- |\n| 1 | 2 |"


def test_render_formatted_uses_the_configured_extensions():
    # The extensions list must actually be loaded, or tables, footnotes,
    # fenced code and syntax highlighting all silently stop working.
    assert "<table>" in render_formatted(TABLE)


def test_render_markdown_uses_default_settings_without_the_extensions():
    # The markdown filter is deliberately plainer than the content pipeline.
    assert "<table>" not in render_markdown(TABLE)


def test_render_markdown_strips_surrounding_whitespace():
    assert render_markdown("\n  hi  \n") == "<p>hi</p>"


def test_render_formatted_highlights_fenced_code():
    assert 'class="highlight"' in render_formatted("```C\nint x;\n```")
