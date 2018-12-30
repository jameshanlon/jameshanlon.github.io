import os
import sys
import requests
from PIL import Image
from io import BytesIO

# These variables need to match the pelicanconf.py settings.
PREFIX = 'https://jwh.ams3.digitaloceanspaces.com/homepage'
OUT_DIR = os.path.join(os.getcwd(), 'output')
THUMB_DIR = 'thumbs'

def parse_size(size):
    # <max-x-dim-size>x<max-y-dim-size>
    tokens = size.split('x')
    return (int(tokens[0]), int(tokens[1]))

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
    print 'Fetching '+image_url
    response = requests.get(image_url)
    if response.status_code != 200:
        print 'Image not found: ' + image_url
        sys.exit(1)
    image = Image.open(BytesIO(response.content))
    # Resize the image up to a maximum x OR y dimension.
    image.thumbnail(parse_size(size), Image.ANTIALIAS)
    image.save(thumb_path)
    print 'Wrote '+thumb_path
    return thumb_url
