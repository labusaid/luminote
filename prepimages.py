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
    font = ImageFont.truetype(config.font)
    draw.text(location, text, font=font)
    return image

# TODO: draw_scroll_text function
def draw_scroll_text(text):
    image = Image.new('RGB', (columns, rows))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(config.font)

    textwidth = draw.textsize(text,font=font)[0]
    textheight = draw.textsize(text,font=font)[1]

    # center if text is less than width
    if (textwidth <= columns):
        offset = (columns-textwidth)/2
        draw_text(text, image, (offset,0))
        return image
    else:
        frames = (textwidth-columns)+1
        output = Image.new('RGB', (columns, rows * frames))
        offset = 0
        # generate frames
        for i in range(frames):
            # image manipulation
            image.paste((0, 0, 0), (0, 0, columns, rows))  # fill image with black
            draw_text(text, image, (offset,0))
            output.paste(image, (0, rows * i))  # write image to animation
            offset -= 1
        return output

# Creates spinning line animation
def draw_spinning_line(frames=32, fill=(255,255,255), width=1, ccw=False):
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

# TODO: add logic to reverse math when height is greater than width
# Creates roulette wheel animation
def draw_roulette_wheel(frames=32, fill=(255,255,255), width=20, ccw=False):
    radius = columns if (columns > rows) else rows
    constraint = columns if (columns < rows) else rows
    offset = (radius - constraint) / 2

    output = Image.new('RGB', (columns, rows*frames))
    image = Image.new('RGB', (columns, rows))
    draw = ImageDraw.Draw(image)

    theta = 360/frames # in degrees
    start = 0
    end = start+width


    print(str(rows) + ', ' + str(columns))

    # generate frames
    for i in range(frames):

        # image manipulation
        image.paste((0,0,0),(0,0,columns,rows)) # fill image with black
        draw.pieslice((0,-offset,columns,columns-offset),start,end,fill)
        draw.pieslice((0,-offset,columns,columns-offset),start+180,end+180,fill)
        output.paste(image,(0,rows*i)) # write image to animation

        # iterate
        start = theta - width if ccw else start + theta
        end = start+width

    # return animation
    return output

# Generate default animations
# draw_spinning_line().save('img/spinningline.png')
# draw_roulette_wheel().save('img/roulettewheel.png')
draw_scroll_text('  why milan built like an improper fraction  ').save('img/text.png')
