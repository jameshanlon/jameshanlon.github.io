"""
Check the built site against the recorded URL contract.
"""

import hashlib
from pathlib import Path

import pytest

MANIFEST = Path("tests/url_manifest.txt")


def load_manifest():
    """
    Return a mapping of output path to expected hash, or None for binaries.
    """
    expected = {}
    for line in MANIFEST.read_text().splitlines():
        path, digest = line.rsplit(" ", 1)
        expected[path] = None if digest == "-" else digest
    return expected


@pytest.fixture(scope="module")
def built(output_dir):
    actual = {
        p.relative_to(output_dir).as_posix()
        for p in output_dir.rglob("*")
        if p.is_file()
    }
    return actual


def test_no_urls_disappeared(built):
    missing = sorted(set(load_manifest()) - built)
    assert not missing, f"{len(missing)} URLs no longer generated: {missing[:10]}"


def test_no_urls_appeared(built):
    extra = sorted(built - set(load_manifest()))
    assert not extra, f"{len(extra)} unexpected URLs generated: {extra[:10]}"


def test_contents_unchanged(output_dir):
    changed = []
    for path, digest in load_manifest().items():
        if digest is None:
            continue
        actual = hashlib.sha256((output_dir / path).read_bytes()).hexdigest()
        if actual != digest:
            changed.append(path)
    assert not changed, f"{len(changed)} outputs changed: {changed[:10]}"
