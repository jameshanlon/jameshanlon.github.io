import os
import sys
import requests
from PIL import Image, ExifTags
from io import BytesIO
import logging

# These variables need to match the pelicanconf.py settings.
LOCAL_PREFIX = os.path.join(os.getcwd(), 'content')
REMOTE_PREFIX = 'https://jwh.ams3.digitaloceanspaces.com/homepage'
OUT_DIR = os.path.join(os.getcwd(), 'output')
THUMB_DIR = 'thumbs'

def fetch_remote(filepath, size):
    image_url = REMOTE_PREFIX + '/' + filepath
    # Get the image.
    logging.info('Fetching '+image_url)
    response = requests.get(image_url)
    if response.status_code != 200:
        logging.error('Image not found: ' + image_url)
        sys.exit(1)
    return Image.open(BytesIO(response.content))

def get_thumbnail(filepath, size, local=False):
    # Setup paths
    split_ext = os.path.splitext(os.path.basename(filepath))
    thumb_filename = split_ext[0] + '_' + size + split_ext[1]
    thumb_path = os.path.join(OUT_DIR, THUMB_DIR, thumb_filename)
    thumb_dir = os.path.dirname(thumb_path)
    thumb_url = os.path.join(THUMB_DIR, thumb_filename)
    # Create directory if it don't exist.
    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)
    # For development, fetch the images from a local location. Otherwise,
    # fetch from remote.
    if local:
        image = Image.open(os.path.join(LOCAL_PREFIX, filepath))
    else:
        if os.path.exists(thumb_path):
            # Return the thumb if it exists.
            image = Image.open(thumb_path)
        else:
            image = fetch_remote(filepath, size)
    # Rotate if recorded in metadata.
    # https://stackoverflow.com/questions/4228530/pil-thumbnail-is-rotating-my-image
    if image.format == 'JPEG' or \
       image.format == 'TIFF':
        for orientation in ExifTags.TAGS.keys():
             if ExifTags.TAGS[orientation]=='Orientation':
                  break
        if image._getexif():
            exif=dict(image._getexif().items())
            if orientation in exif:
                if exif[orientation] == 3:
                    image=image.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    image=image.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    image=image.rotate(90, expand=True)
    original_w = image.size[0]
    original_h = image.size[1]
    logging.info('Old size: {} x {}'.format(original_w, original_h))
    if 'x' in size:
        # <max-x-dim-size>x<max-y-dim-size>
        tokens = size.split('x')
        size = (int(tokens[0]), int(tokens[1]))
    elif size.startswith('h='):
        # Fixed height
        height = int(size.replace('h=', ''))
        width = int(height * (float(original_w) / float(original_h)))
        size = (width, height)
        logging.info('New size: {} x {}'.format(size[0], size[1]))
    elif size.startswith('w='):
        # Fixed width
        width = int(size.replace('w=', ''))
        height = int(width * (float(original_h) / float(original_w)))
        size = (width, height)
    else:
        logging.error('Invalid size: '+size)
        sys.exit(1)
    image.thumbnail(size, Image.ANTIALIAS)
    # Resize the image upto a maximum x OR y dimension.
    image.save(thumb_path)
    logging.info('Wrote '+thumb_path)
    return thumb_url
