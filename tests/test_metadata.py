import re
from datetime import datetime
from pathlib import Path

import pytest

from ssg import config
from ssg.metadata import SlugError, parse_date, slugify, split_list


def test_slugify_lowercases_and_hyphenates():
    assert slugify("New chips for machine intelligence") == (
        "new-chips-for-machine-intelligence"
    )


def test_slugify_deletes_punctuation_rather_than_hyphenating_it():
    # The '+' is removed, not turned into a separator.
    assert slugify("Seeding parallel xoroshiro128+ generators") == (
        "seeding-parallel-xoroshiro128-generators"
    )


def test_slugify_keeps_existing_hyphens_and_collapses_runs():
    assert slugify("The XMOS  XMP-64") == "the-xmos-xmp-64"


def test_slugify_rejects_a_title_that_reduces_to_nothing():
    with pytest.raises(SlugError, match=r"\*\*\*"):
        slugify("***")


def test_slugify_rejects_non_ascii_rather_than_transliterating():
    # Unidecode is gone, so a non-ASCII title needs an explicit Slug field.
    with pytest.raises(SlugError, match="non-ASCII"):
        slugify("Überblick")


def test_split_list_splits_on_commas():
    assert split_list("computing, machine-intelligence") == [
        "computing",
        "machine-intelligence",
    ]


def test_split_list_prefers_semicolons_when_present():
    # content/ml-challenges.md depends on this.
    assert split_list("computing; computer-architecture; machine-intelligence") == [
        "computing",
        "computer-architecture",
        "machine-intelligence",
    ]


def test_split_list_ignores_commas_once_a_semicolon_appears():
    assert split_list("Doe, Jane; Doe, John") == ["Doe, Jane", "Doe, John"]


def test_split_list_drops_empty_entries():
    assert split_list("computing,, verilog,") == ["computing", "verilog"]


def test_parse_date_applies_the_site_timezone():
    parsed = parse_date("2019-10-04")
    assert parsed == datetime(2019, 10, 4, tzinfo=parsed.tzinfo)
    assert parsed.utcoffset().total_seconds() == 2 * 3600


def test_parse_date_accepts_every_unpadded_date_in_content():
    # Several real articles write Date fields with an unpadded month or day
    # (e.g. 2017-2-10); strptime's leniency here must not be tightened away.
    pattern = re.compile(r"^Date:\s*(\S+)", re.MULTILINE)
    unpadded = [
        value
        for path in Path(config.CONTENT_DIR).glob("*.md")
        for value in pattern.findall(path.read_text())
        if re.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}", value)
        and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)
    ]

    assert unpadded, "expected at least one unpadded date in content/"
    for value in unpadded:
        parse_date(value)
