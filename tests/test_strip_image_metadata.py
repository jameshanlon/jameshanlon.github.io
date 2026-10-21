import io
import sys
from pathlib import Path

import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from strip_image_metadata import describe, pixel_digest, strip  # noqa: E402

from ssg.assets import AssetError  # noqa: E402


def jpeg(colour=(10, 20, 30), orientation=None, gps=True):
    """
    Return a JPEG carrying metadata, as a camera would produce.
    """
    exif = Image.Exif()
    exif[0x010F] = "Apple"
    exif[0x0132] = "2019:11:10 11:25:48"
    if gps:
        exif[0x8825] = {1: "N", 2: (51.0, 28.0, 30.0), 3: "W", 4: (2.0, 34.0, 40.0)}
    if orientation:
        exif[0x0112] = orientation
    buf = io.BytesIO()
    Image.new("RGB", (32, 24), colour).save(buf, "JPEG", exif=exif.tobytes())
    return buf.getvalue()


def png_with_text():
    """
    Return a PNG carrying a text chunk.
    """
    from PIL import PngImagePlugin

    info = PngImagePlugin.PngInfo()
    info.add_text("mxfile", "<diagram agent='draw.io' />")
    buf = io.BytesIO()
    Image.new("RGB", (8, 8), (1, 2, 3)).save(buf, "PNG", pnginfo=info)
    return buf.getvalue()


def test_jpeg_metadata_is_removed():
    assert describe(strip(jpeg())) == []


def test_png_text_is_removed():
    assert describe(strip(png_with_text())) == []


def test_pixels_survive_stripping():
    original = jpeg()
    assert pixel_digest(strip(original)) == pixel_digest(original)


def test_orientation_is_preserved():
    stripped = strip(jpeg(orientation=6))
    assert Image.open(io.BytesIO(stripped)).getexif().get(0x0112) == 6
    assert describe(stripped) == []


def test_every_frame_of_a_multi_picture_jpeg_is_stripped():
    first, second = jpeg(), jpeg((99, 80, 70))
    stripped = strip(first + second)
    tail = stripped[stripped.find(b"\xff\xd9") + 2 :]
    assert describe(stripped) == []
    assert describe(tail) == []
    assert pixel_digest(stripped) == pixel_digest(first)


def test_trailing_padding_is_dropped():
    original = jpeg()
    stripped = strip(original + bytes(4096))
    assert describe(stripped) == []
    assert pixel_digest(stripped) == pixel_digest(original)
    assert not stripped.endswith(bytes(16))


def test_unknown_trailing_data_is_refused():
    with pytest.raises(AssetError):
        strip(jpeg() + b"appended-document")


def test_stripping_is_idempotent():
    once = strip(jpeg(orientation=6))
    assert strip(once) == once
