# Script used to prep images for use by animations.py
import config
from PIL import Image, ImageDraw, ImageFont

# Copy settings from config.py
num_pixels = config.num_pixels
rows = config.rows
columns = config.columns

# TODO: formats externally made image to insure compatibility
def format(image):
    img = Image.open(image)
    pic = img.load()
    print('prepping ' + image + ' for use with RGB leds')
    print('Detected resolution: ' + pic.size())

# draws text to specified image, defaults to a new image
def draw_text(text, image = Image.new('RGB',(columns,rows))):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('resources/visitor1.ttf')
    draw.text((0,0), text, font=font)