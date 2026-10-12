"""
Static assets: remote URLs, local copies and generated thumbnails.
"""

import logging
import shutil
from io import BytesIO

import requests
from PIL import Image, ImageOps, UnidentifiedImageError

from ssg import config

logger = logging.getLogger(__name__)

THUMB_DIR = "thumbs"
IMAGE_DIR = "images"


class AssetError(RuntimeError):
    """
    Raised when an asset cannot be found or processed.
    """


def _target_size(size, width, height):
    """
    Return the bounding box for a size spec of NxN, h=N or w=N.
    """
    if "x" in size:
        x, _, y = size.partition("x")
        return int(x), int(y)
    if size.startswith("h="):
        target_height = int(size[2:])
        return int(target_height * (width / height)), target_height
    if size.startswith("w="):
        target_width = int(size[2:])
        return target_width, int(target_width * (height / width))
    raise AssetError(f"invalid thumbnail size: {size}")


class Assets:
    """
    Resolves asset references for one build, writing into output_dir.
    """

    def __init__(self, output_dir, content_dir=None):
        """
        Bind this build's output directory and content source.
        """
        self.output_dir = output_dir
        self.content_dir = content_dir or config.CONTENT_DIR

    def filters(self):
        """
        Return the Jinja filters this class provides.
        """
        return {
            "asset": self.asset_url,
            "thumbnail": self.thumbnail,
            "image": self.image,
        }

    def asset_url(self, filepath):
        """
        Return the remote URL for an asset on the object store.
        """
        return f"{config.REMOTE_PREFIX}/{filepath}"

    def image(self, filepath):
        """
        Return a URL for an image.

        A local copy under the content directory is copied into the output and
        referenced there; otherwise the remote URL is returned.
        """
        local = self.content_dir / filepath
        if not local.exists():
            return self.asset_url(filepath)

        target = self.output_dir / IMAGE_DIR / local.name
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(local, target)
        return f"/{IMAGE_DIR}/{local.name}"

    def thumbnail(self, filepath, size):
        """
        Return the URL of a thumbnail, generating it if necessary.

        The source image is taken from the content directory when present, so
        that builds work offline, and fetched from the object store otherwise.
        """
        local = self.content_dir / filepath
        name = f"{local.stem}_{size}{local.suffix}"
        target = self.output_dir / THUMB_DIR / name
        url = f"{THUMB_DIR}/{name}"
        if target.exists():
            return url

        if local.exists():
            logger.info("Using local image %s", local)
            image = Image.open(local)
        else:
            image = self._fetch(filepath)

        image = ImageOps.exif_transpose(image)
        box = _target_size(size, image.size[0], image.size[1])
        image.thumbnail(box, Image.LANCZOS)
        target.parent.mkdir(parents=True, exist_ok=True)
        image.save(target)
        logger.info("Wrote %s", target)
        return url

    def _fetch(self, filepath):
        """
        Fetch an image from the object store.
        """
        url = self.asset_url(filepath)
        logger.info("Fetching %s", url)
        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            raise AssetError(f"image not found: {url}")
        try:
            return Image.open(BytesIO(response.content))
        except UnidentifiedImageError as exc:
            raise AssetError(f"not a valid image: {url}") from exc

    def copy_static(self):
        """
        Copy the configured static trees into the output root.
        """
        for entry in config.STATIC_PATHS:
            source = self.content_dir / entry
            target = self.output_dir / entry
            if source.is_dir():
                shutil.copytree(source, target, dirs_exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)

        theme_static = config.THEME_DIR / "static"
        shutil.copytree(
            theme_static, self.output_dir / "theme", dirs_exist_ok=True
        )
