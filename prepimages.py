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

# Draws text over a specified image, defaults to a new image with text starting in the top left
def draw_text(text, image = Image.new('RGB',(columns,rows)), location=(0,0)):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('resources/visitor1.ttf')
    draw.text(location, text, font=font)
    return image

# TODO: convert to use pie slice instead of line
# Creates roulette wheel animation
def draw_spinning_line(frames=32, fill=(255,255,255), width=1, ccw = False):
    output = Image.new('RGB', (columns, rows*frames))
    image = Image.new('RGB', (columns, rows))
    draw = ImageDraw.Draw(image)
    radius = columns if (columns > rows) else rows
    theta = 0
    radian_delta = np.deg2rad(360/frames)
    # generate frames
    for i in range(frames):
        # polar to cartesian
        point1 = (radius*np.cos(theta), radius*np.sin(theta))
        point2 = (radius*np.cos(theta+np.pi), radius*np.sin(theta+np.pi))

        # shift origin to center of matrix
        point1shifted = (point1[0]+columns/2, point1[1]+rows/2)
        point2shifted = (point2[0]+columns/2, point2[1]+rows/2)

        # image manipulation
        image.paste((0,0,0),(0,0,columns,rows)) # fill image with black
        draw.line((point1shifted,point2shifted),fill,width) # draw line on image
        output.paste(image,(0,rows*i)) # write image to animation

        # iterate
        theta = theta - radian_delta if ccw else theta + radian_delta
    # return animation
    return output

# Generate default animations
draw_spinning_line().save('img/spinningline.png')