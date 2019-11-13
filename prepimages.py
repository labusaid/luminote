# Script used to prep images for use by animations.py
import numpy as np
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

# draws text over a specified image, defaults to a new image with text starting in the top left
def draw_text(text, image = Image.new('RGB',(columns,rows)), location=(0,0)):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('resources/visitor1.ttf')
    draw.text(location, text, font=font)

# TODO: convert to use pie slice instead of line
# Creates roulette wheel animation
def draw_roulette_wheel(sections=2, frames=16, fill=(255,255,255)):
    image = Image.new('RGB', (columns, rows*frames))
    draw = ImageDraw.Draw(image)
    rotation = 0
    radian_rotation = np.deg2rad(360/frames)
    # TODO: a bunch of trig for calculating points based on rotation that I don't feel like doing right now
    for i in range(frames):
        rotation += radian_rotation
        point1 = (0,0)
        point2 = (columns,rows)
        # TODO: add counter clockwise support
        draw.line((point1,point2),fill=fill)