import os
import sys
import shutil
import requests
from PIL import Image, ExifTags
from io import BytesIO
import logging

# These variables need to match the pelicanconf.py settings.
LOCAL_PREFIX = os.path.join(os.getcwd(), "content")
REMOTE_PREFIX = "https://jwh.ams3.digitaloceanspaces.com/homepage"
OUT_DIR = os.path.join(os.getcwd(), "output")
IMAGE_DIR = "images"
THUMB_DIR = "thumbs"


def fetch_remote(filepath, size):
    image_url = REMOTE_PREFIX + "/" + filepath
    # Get the image.
    logging.info("Fetching " + image_url)
    response = requests.get(image_url)
    if response.status_code != 200:
        logging.error("Image not found: " + image_url)
        sys.exit(1)
    return Image.open(BytesIO(response.content))


def get_image(filepath):
    """
    Return a URL prefix to an image. If the image is found locally, copy the
    image to the output directory and return a reference to it there.
    """
    local_path = os.path.join(LOCAL_PREFIX, filepath)
    if os.path.exists(local_path):
        logging.info(f"Using local image version {local_path}")

        # Setup paths.
        image_name = os.path.basename(filepath)
        image_path = os.path.join(OUT_DIR, IMAGE_DIR, image_name)
        image_dir = os.path.dirname(image_path)

        if os.path.exists(image_path):
            # Return the image if it exists.
            return "/images/" + image_name

        if not os.path.exists(image_dir):
            # Create the image directory if it doesn't exist.
            os.makedirs(image_dir)

        # Copy the file to the output directory
        shutil.copyfile(local_path, image_path)

        return "/images/" + image_name

    else:
        # The image is hosted remotely.
        return REMOTE_PREFIX + "/" + filepath


def get_thumbnail(filepath, size):
    # Setup paths
    split_ext = os.path.splitext(os.path.basename(filepath))
    thumb_filename = split_ext[0] + "_" + size + split_ext[1]
    thumb_path = os.path.join(OUT_DIR, THUMB_DIR, thumb_filename)
    thumb_dir = os.path.dirname(thumb_path)
    thumb_url = os.path.join(THUMB_DIR, thumb_filename)
    # Create directory if it don't exist.
    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)
    if os.path.exists(thumb_path):
        # Return the thumb if it exists.
        return thumb_url
    # For development, fetch the images from a local location. Otherwise,
    # fetch the remote image.
    local_path = os.path.join(LOCAL_PREFIX, filepath)
    if os.path.exists(local_path):
        image = Image.open(local_path)
        logging.info(f"Using local image version {local_path}")
    else:
        image = fetch_remote(filepath, size)
    # Rotate if recorded in metadata.
    # https://stackoverflow.com/questions/4228530/pil-thumbnail-is-rotating-my-image
    if image.format == "JPEG" or image.format == "TIFF":
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        if image._getexif():
            exif = dict(image._getexif().items())
            if orientation in exif:
                if exif[orientation] == 3:
                    image = image.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    image = image.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    image = image.rotate(90, expand=True)
    original_w = image.size[0]
    original_h = image.size[1]
    logging.info("Old size: {} x {}".format(original_w, original_h))
    if "x" in size:
        # <max-x-dim-size>x<max-y-dim-size>
        tokens = size.split("x")
        size = (int(tokens[0]), int(tokens[1]))
    elif size.startswith("h="):
        # Fixed height
        height = int(size.replace("h=", ""))
        width = int(height * (float(original_w) / float(original_h)))
        size = (width, height)
        logging.info("New size: {} x {}".format(size[0], size[1]))
    elif size.startswith("w="):
        # Fixed width
        width = int(size.replace("w=", ""))
        height = int(width * (float(original_h) / float(original_w)))
        size = (width, height)
    else:
        logging.error("Invalid size: " + size)
        sys.exit(1)
    image.thumbnail(size, Image.LANCZOS)
    # Resize the image upto a maximum x OR y dimension.
    image.save(thumb_path)
    logging.info("Wrote " + thumb_path)
    return thumb_url
