import pytest

from ssg.assets import AssetError, Assets


def test_asset_url_points_at_the_remote_store():
    assets = Assets(output_dir="/tmp/does-not-matter")
    assert assets.asset_url("talks/slides.pdf").endswith("/homepage/talks/slides.pdf")


def test_thumbnail_writes_into_the_requested_output_directory(tmp_path):
    # thumbnail.py wrote to ./output/thumbs whatever output directory was asked
    # for; the replacement must honour the argument.
    source = tmp_path / "content" / "pic.png"
    source.parent.mkdir()
    _write_png(source, size=(40, 30))

    assets = Assets(output_dir=tmp_path / "out", content_dir=tmp_path / "content")
    url = assets.thumbnail("pic.png", "20x20")

    assert url == "thumbs/pic_20x20.png"
    assert (tmp_path / "out" / "thumbs" / "pic_20x20.png").is_file()


def test_thumbnail_reuses_an_existing_file(tmp_path):
    source = tmp_path / "content" / "pic.png"
    source.parent.mkdir()
    _write_png(source, size=(40, 30))
    assets = Assets(output_dir=tmp_path / "out", content_dir=tmp_path / "content")

    assets.thumbnail("pic.png", "20x20")
    written = (tmp_path / "out" / "thumbs" / "pic_20x20.png").stat().st_mtime_ns
    assets.thumbnail("pic.png", "20x20")

    assert (tmp_path / "out" / "thumbs" / "pic_20x20.png").stat().st_mtime_ns == written


def test_thumbnail_rejects_an_unparsable_size(tmp_path):
    source = tmp_path / "content" / "pic.png"
    source.parent.mkdir()
    _write_png(source, size=(40, 30))
    assets = Assets(output_dir=tmp_path / "out", content_dir=tmp_path / "content")

    with pytest.raises(AssetError, match="banana"):
        assets.thumbnail("pic.png", "banana")


def test_thumbnail_reports_a_missing_remote_source(tmp_path, monkeypatch):
    # A 404 must abort rather than leave a truncated image for CI to cache.
    class Response:
        status_code = 404
        content = b""

    monkeypatch.setattr("ssg.assets.requests.get", lambda url, timeout: Response())
    assets = Assets(output_dir=tmp_path / "out", content_dir=tmp_path / "content")

    with pytest.raises(AssetError, match="gone.png"):
        assets.thumbnail("gone.png", "20x20")

    assert not (tmp_path / "out" / "thumbs" / "gone_20x20.png").exists()


def _write_png(path, size):
    from PIL import Image

    Image.new("RGB", size, "red").save(path)
