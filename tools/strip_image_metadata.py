#!/usr/bin/env python
"""
Report and remove metadata from the site's images.

Camera images carry EXIF metadata including GPS coordinates, device models and
capture timestamps. This tool reports what the published images contain and
rewrites them without it, leaving the pixel data untouched.
"""

import argparse
import concurrent.futures
import hashlib
import re
import sys
import threading
from io import BytesIO
from pathlib import Path

import requests
from PIL import ExifTags, Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ssg import config  # noqa: E402
from ssg.assets import AssetError, asset_url  # noqa: E402

ORIENTATION = 0x0112
EXIF_IFD = 0x8769
GPS_IFD = 0x8825

# EXIF lives in the application segments at the head of a JPEG, so a scan can
# sample one. PNG text chunks can follow the image data, so a PNG cannot.
HEAD_BYTES = 128 * 1024
WORKERS = 8

# Application segments worth keeping: the JFIF density header, the colour
# profile, Adobe's colour transform marker and the radiometric data of thermal
# images. The thermal payload records the camera serial number and the capture
# date, but no location.
JPEG_KEEP = {
    0xE0: (b"JFIF\0",),
    0xE1: (b"FLIR\0",),
    0xE2: (b"ICC_PROFILE\0",),
    0xEE: (b"Adobe",),
}

# PNG chunks holding text, EXIF or timestamps.
PNG_DROP = {b"tEXt", b"zTXt", b"iTXt", b"eXIf", b"tIME"}

# Tags called out by name in the report. Everything else is counted, so an
# unlisted tag is never reported as clean; stripping ignores both lists.
REPORTED = (
    "Make",
    "Model",
    "HostComputer",
    "Software",
    "Artist",
    "Copyright",
    "DateTime",
    "DateTimeOriginal",
    "LensModel",
    "BodySerialNumber",
    "CameraOwnerName",
)

# PNG keys describing how to render the image rather than where it came from.
PNG_RENDERING = {
    "dpi",
    "gamma",
    "srgb",
    "icc_profile",
    "transparency",
    "interlace",
    "aspect",
    "chromaticity",
}

URL_PATTERN = re.compile(
    re.escape(config.REMOTE_PREFIX) + r"/([^\"')>\s]+\.(?:jpe?g|png))",
    re.IGNORECASE,
)

LOCAL = threading.local()


def session():
    """
    Return this thread's HTTP session, since a session is not thread-safe.
    """
    if not hasattr(LOCAL, "session"):
        LOCAL.session = requests.Session()
    return LOCAL.session


def collect_paths(output_dir):
    """
    Return the image asset paths referenced by a built site.
    """
    paths = set()
    for page in Path(output_dir).rglob("*.html"):
        paths.update(URL_PATTERN.findall(page.read_text(errors="replace")))
    return sorted(paths)


def read_asset(filepath, head_only=False):
    """
    Return the bytes of an asset, preferring a local copy over the object store.
    """
    local = config.CONTENT_DIR / filepath
    if local.exists():
        return local.read_bytes()
    url = asset_url(filepath)
    sample = head_only and not filepath.lower().endswith(".png")
    headers = {"Range": f"bytes=0-{HEAD_BYTES - 1}"} if sample else {}
    try:
        response = session().get(url, headers=headers, timeout=60)
    except requests.RequestException as exc:
        raise AssetError(f"fetch failed: {url}: {exc}") from exc
    if response.status_code not in (200, 206):
        raise AssetError(f"fetch failed ({response.status_code}): {url}")
    return response.content


def read_assets(paths, head_only):
    """
    Yield each path with its bytes, or with the error that prevented reading it.

    Assets are fetched a batch at a time so that only a batch is held in memory.
    """
    with concurrent.futures.ThreadPoolExecutor(WORKERS) as pool:
        for start in range(0, len(paths), WORKERS):
            batch = paths[start : start + WORKERS]
            futures = [pool.submit(read_asset, path, head_only) for path in batch]
            for filepath, future in zip(batch, futures):
                error = future.exception()
                yield filepath, None if error else future.result(), error


def describe(data):
    """
    Return a list of human-readable metadata findings for an image.

    Orientation is excluded: it describes how to display the image and is
    deliberately preserved.
    """
    image = Image.open(BytesIO(data))
    findings = []
    exif = image.getexif()
    if exif.get_ifd(GPS_IFD):
        findings.append("GPS location")
    tags = dict(exif) | dict(exif.get_ifd(EXIF_IFD))
    for pointer in (ORIENTATION, EXIF_IFD):
        tags.pop(pointer, None)
    if tags:
        findings.append(f"{len(tags)} EXIF tags")
    named = {ExifTags.TAGS.get(tag, hex(tag)): value for tag, value in tags.items()}
    for tag in REPORTED:
        value = str(named.get(tag, "")).strip()
        if value:
            findings.append(f"{tag}={value}")
    if image.format == "PNG":
        findings += [
            f"PNG {key}" for key in sorted(image.info) if key not in PNG_RENDERING
        ]
    return findings


def metadata_of(filepath, data, sampled):
    """
    Return the findings for an asset, refetching it whole if a sample of it was
    too small to parse.

    Some images carry megabytes of application segments ahead of the image
    data, so a sample large enough for most files is not large enough for all.
    """
    try:
        return describe(data)
    except OSError:
        if not sampled:
            raise
        return describe(read_asset(filepath))


def pixel_digest(data):
    """
    Return a digest of an image's decoded pixels, mode and size.
    """
    image = Image.open(BytesIO(data))
    digest = hashlib.blake2b(f"{image.mode} {image.size}".encode())
    digest.update(image.tobytes())
    return digest.digest()


def orientation_segment(orientation):
    """
    Return an APP1 segment holding nothing but an orientation tag.
    """
    exif = Image.Exif()
    exif[ORIENTATION] = orientation
    payload = b"Exif\0\0" + exif.tobytes()
    return b"\xff\xe1" + (len(payload) + 2).to_bytes(2, "big") + payload


def strip_jpeg_tail(data, index):
    """
    Return the image data from a scan or end marker, with later frames stripped.

    Multi-picture JPEGs append further images after the first end-of-image
    marker, each carrying its own metadata. Within entropy-coded data an 0xFF
    byte is always stuffed or a restart marker, so the first end-of-image
    marker found cannot be a false positive.
    """
    end = data.find(b"\xff\xd9", index)
    if end < 0:
        raise AssetError("missing end-of-image marker")
    end += 2
    tail = data[end:]
    if not tail:
        return data[index:end]
    if tail[:2] != b"\xff\xd8":
        raise AssetError(f"unexpected trailing data at offset {end}")
    return data[index:end] + strip_jpeg(tail)


def strip_jpeg(data):
    """
    Return the JPEG with metadata segments removed and orientation preserved.

    Entropy-coded data is copied verbatim, so the image is not re-encoded.
    """
    orientation = Image.open(BytesIO(data)).getexif().get(ORIENTATION, 1)

    segments = []
    index = 2
    while True:
        if index + 1 >= len(data):
            raise AssetError("JPEG ended without an end-of-image marker")
        if data[index] != 0xFF:
            raise AssetError(f"unexpected byte at offset {index}")
        marker = data[index + 1]
        if marker == 0xFF:
            index += 1
            continue
        if marker in (0xD9, 0xDA):
            segments.append(strip_jpeg_tail(data, index))
            break
        length = int.from_bytes(data[index + 2 : index + 4], "big")
        end = index + 2 + length
        metadata = 0xE0 <= marker <= 0xEF or marker == 0xFE
        payload = data[index + 4 : end]
        keep = any(payload.startswith(p) for p in JPEG_KEEP.get(marker, ()))
        if not metadata or keep:
            segments.append(data[index:end])
        index = end

    if orientation != 1:
        at = 1 if segments and segments[0][1] == 0xE0 else 0
        segments.insert(at, orientation_segment(orientation))
    return b"\xff\xd8" + b"".join(segments)


def strip_png(data):
    """
    Return the PNG with text, EXIF and timestamp chunks removed.
    """
    chunks = []
    index = 8
    while index < len(data):
        length = int.from_bytes(data[index : index + 4], "big")
        kind = data[index + 4 : index + 8]
        end = index + 12 + length
        if kind not in PNG_DROP:
            chunks.append(data[index:end])
        index = end
        if kind == b"IEND":
            break
    return data[:8] + b"".join(chunks)


def strip(data):
    """
    Return the image with its metadata removed.
    """
    if data[:2] == b"\xff\xd8":
        return strip_jpeg(data)
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return strip_png(data)
    raise AssetError("unsupported image format")


def clean(filepath, data, dest):
    """
    Write a metadata-free copy of an image, or return False if it had none.

    The decoded pixels and the stripped result are both checked before the copy
    is kept, so a cleaned image can only differ from its original in metadata.
    """
    cleaned = strip(data)
    if cleaned == data:
        return False
    if pixel_digest(cleaned) != pixel_digest(data):
        raise AssetError(f"{filepath}: pixel data changed")
    remaining = describe(cleaned)
    if remaining:
        raise AssetError(f"{filepath}: metadata remains: {remaining}")
    target = dest / filepath
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(cleaned)
    return True


def main():
    """
    Scan or clean the images referenced by a built site.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command", choices=("scan", "clean"), help="report or rewrite metadata"
    )
    parser.add_argument(
        "-o", "--output-dir", default="output", help="built site to read URLs from"
    )
    parser.add_argument(
        "-d", "--dest", default="cleaned", help="directory for cleaned images"
    )
    parser.add_argument("paths", nargs="*", help="asset paths, instead of all of them")
    args = parser.parse_args()

    paths = args.paths or collect_paths(args.output_dir)
    if not paths:
        parser.error(f"no images found in {args.output_dir}; run 'make html' first")

    scanning = args.command == "scan"
    dest = Path(args.dest)
    affected = 0
    failures = 0
    for filepath, data, error in read_assets(paths, head_only=scanning):
        findings = []
        changed = False
        if error is None:
            try:
                findings = metadata_of(filepath, data, sampled=scanning)
                changed = bool(findings) if scanning else clean(filepath, data, dest)
            except (AssetError, OSError, ValueError) as exc:
                error = exc
        if error is not None:
            failures += 1
            print(f"{filepath}: FAILED: {error}", file=sys.stderr)
            continue
        if findings or changed:
            affected += 1
            print(f"{filepath}: {', '.join(findings) or 'unreported metadata'}")

    print(f"\n{affected} of {len(paths)} images carry metadata")
    if failures:
        print(f"{failures} images could not be processed", file=sys.stderr)
    if not scanning and affected:
        if failures:
            print(f"{dest}/ is incomplete; re-run before relying on it")
        print(f"Cleaned copies written to {dest}/. Upload them with:\n")
        print(f"  s3cmd sync {dest}/ s3://jwh/homepage/ --acl-public")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
