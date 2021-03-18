from __future__ import print_function
import os
import sys
import requests
from PIL import Image, ExifTags
from io import BytesIO

# These variables need to match the pelicanconf.py settings.
PREFIX = 'https://jwh.ams3.digitaloceanspaces.com/homepage'
OUT_DIR = os.path.join(os.getcwd(), 'output')
THUMB_DIR = 'thumbs'

def get_thumbnail(filepath, size):
    image_url = PREFIX + '/' + filepath
    split_ext = os.path.splitext(os.path.basename(filepath))
    thumb_filename = split_ext[0] + '_' + size + split_ext[1]
    thumb_path = os.path.join(OUT_DIR, THUMB_DIR, thumb_filename)
    thumb_dir = os.path.dirname(thumb_path)
    thumb_url = os.path.join(THUMB_DIR, thumb_filename)
    # Return the thumb if it exists.
    if os.path.exists(thumb_path):
        return thumb_url
    # Create the directories if they don't exist.
    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)
    # Get the image.
    print('Fetching '+image_url)
    response = requests.get(image_url)
    if response.status_code != 200:
        print('Image not found: ' + image_url)
        sys.exit(1)
    # Rotate if recorded in metadata.
    # https://stackoverflow.com/questions/4228530/pil-thumbnail-is-rotating-my-image
    image = Image.open(BytesIO(response.content))
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
    print('Old size: {} x {}'.format(original_w, original_h))
    if 'x' in size:
        # <max-x-dim-size>x<max-y-dim-size>
        tokens = size.split('x')
        size = (int(tokens[0]), int(tokens[1]))
    elif size.startswith('h='):
        # Fixed height
        height = int(size.replace('h=', ''))
        width = int(height * (float(original_w) / float(original_h)))
        size = (width, height)
        print('New size: {} x {}'.format(size[0], size[1]))
    elif size.startswith('w='):
        # Fixed width
        width = int(size.replace('w=', ''))
        height = int(width * (float(original_h) / float(original_w)))
        size = (width, height)
    else:
        print('Invalid size: '+size)
        sys.exit(1)
    image.thumbnail(size, Image.ANTIALIAS)
    # Resize the image upto a maximum x OR y dimension.
    image.save(thumb_path)
    print('Wrote '+thumb_path)
    return thumb_url
