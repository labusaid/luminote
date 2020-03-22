# Script used to prep images for use by animations.py when using an led matrix

import random
import numpy as np
import config
import colorwheels as clr
from PIL import Image, ImageDraw, ImageFont

# Copy settings from config.py
num_pixels = config.num_pixels
rows = config.rows
columns = config.columns

# Scratch data for creating a one frame representation of the LED matrix
image = Image.new('RGB', (columns, rows))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype(config.font)


# fills scratch image with black
def clear_scratch():
    image.paste((0, 0, 0), (0, 0, columns, rows))


# TODO: formats externally made image to insure compatibility
# format image for use with display code
def format(image):
    img = Image.open(image)
    pic = img.load()
    print('prepping ' + image + ' for use with RGB leds')
    print('Detected resolution: ' + pic.size())


# converts animation to advance right by frame instead of down for compatibility with other tools (used to export animations)
def convert_right_advance(image):
    frames = int(image.height / rows)

    output = Image.new('RGB', (columns * frames, rows))

    # generate frames
    for i in range(frames):
        # image manipulation
        output.paste(image.crop((0, rows * i, columns, rows * i + rows)), (columns * i, 0))  # write image to animation

    # return animation
    return output


# converts animation to advance down by frame instead of right for compatibility with other tools (used to import animations)
def convert_down_advance(imgpath):
    img = Image.open(imgpath)  # Can be many different formats.
    pic = img.load()
    frames = int(img.width / columns)

    output = Image.new('RGB', (columns, rows * frames))

    # generate frames
    for i in range(frames):
        # image manipulation
        output.paste(img.crop((columns * i, 0, columns * i + columns, rows)), (0, rows * i))  # write image to animation

    # return animation
    return output


# TODO: draw_fire(), draw_checkers(), draw_strobe()


# Draws text over a specified image, defaults to a new image with text starting in the top left
def draw_text(text, image=Image.new('RGB', (columns, rows)), location=(0, 0), fill=(255, 255, 255)):
    textdraw = ImageDraw.Draw(image)
    textdraw.font = ImageFont.truetype(config.font)
    textdraw.text(location, text, fill)
    return image


def draw_scroll_text(text, colorwheel=clr.wheel):
    textwidth, textheight = draw.textsize(text, font=font)

    # center if text is less than width
    if textwidth <= columns:
        offset = (columns - textwidth) / 2
        draw_text(text, image, (offset, 0))
        return image
    else:
        frames = (textwidth - columns) + 1
        output = Image.new('RGB', (columns, rows * frames))
        offset = 0

        # color cycle
        colorinc = 255 / frames
        currcolor = 0

        # generate frames
        for i in range(frames):
            # image manipulation
            clear_scratch()
            draw_text(text, image, (offset, 0), fill=colorwheel(currcolor))
            output.paste(image, (0, rows * i))  # write image to animation
            offset -= 1
            currcolor += colorinc
        return output


# Creates scanner animation
def draw_scanner(frames=32, colorwheel=clr.wheel, width=3, direction=1, bounce=True):
    global curroffset, offesetinc
    output = Image.new('RGB', (columns, rows * frames))

    # recursively call draws_scanner twice to generate each half of the output
    if bounce:
        output.paste(
            draw_scanner(frames=int(frames / 2), colorwheel=colorwheel, width=width, direction=direction),
            (0, 0))
        output.paste(
            draw_scanner(frames=int(frames / 2), colorwheel=colorwheel, width=width, direction=0 - direction),
            (0, frames * int(rows / 2)))

    else:
        # color cycle
        colorinc = 255 / frames
        currcolor = 0

        # calculate offsets based on direction
        if direction == 1:
            curroffset = 0
            offesetinc = columns / frames
        elif direction == 2:
            curroffset = 0
            offesetinc = rows / frames
        elif direction == -1:
            curroffset = columns
            offesetinc = -(columns / frames)
        elif direction == -2:
            curroffset = rows
            offesetinc = -(rows / frames)

        # generate frames
        for i in range(frames):

            # image manipulation
            clear_scratch()

            if direction == 1:
                draw.rectangle((curroffset - width / 2, 0, curroffset + width / 2, rows), fill=colorwheel(currcolor))
            elif direction == 2:
                draw.rectangle((0, curroffset - width / 2, columns, curroffset + width / 2), fill=colorwheel(currcolor))
            elif direction == -1:
                draw.rectangle((curroffset + width / 2, 0, curroffset - width / 2, rows), fill=colorwheel(currcolor))
            elif direction == -2:
                draw.rectangle((0, curroffset - width / 2, columns, curroffset + width / 2), fill=colorwheel(currcolor))

            output.paste(image, (0, rows * i))  # write image to animation

            # iterate
            currcolor += colorinc
            curroffset += offesetinc

    # return animation
    return output


# Randomly places pixels
def draw_sparkle(frames=32, colorwheel=clr.wheel, quantity=3):
    output = Image.new('RGB', (columns, rows * frames))

    # color cycle
    colorinc = 255 / frames
    currcolor = 0

    # generate frames
    for i in range(frames):
        clear_scratch()
        for _ in range(quantity):
            x = random.randrange(rows)
            y = random.randrange(columns)

            print(colorwheel(currcolor))
            image.paste(colorwheel(currcolor), (y, x, y + 1, x + 1))

        # image manipulation
        output.paste(image, (0, rows * i))  # write image to animation

        # iterate
        currcolor += colorinc

    # return animation
    return output


# Creates spinning line animation
def draw_spinning_line(frames=32, colorwheel=clr.wheel, width=1, ccw=False):
    output = Image.new('RGB', (columns, rows * frames))

    # color cycle
    colorinc = 255 / frames
    currcolor = 0

    # graphics stuff
    radius = columns if (columns > rows) else rows
    theta = 0
    radian_delta = np.deg2rad(360 / frames)
    # generate frames
    for i in range(frames):
        # polar to cartesian
        point1 = (radius * np.cos(theta), radius * np.sin(theta))
        point2 = (radius * np.cos(theta + np.pi), radius * np.sin(theta + np.pi))

        # shift origin to center of matrix
        point1shifted = (point1[0] + columns / 2, point1[1] + rows / 2)
        point2shifted = (point2[0] + columns / 2, point2[1] + rows / 2)

        # image manipulation
        clear_scratch()
        draw.line((point1shifted, point2shifted), colorwheel(currcolor), width)  # draw line on image
        output.paste(image, (0, rows * i))  # write image to animation

        # iterate
        theta = theta - radian_delta if ccw else theta + radian_delta
        currcolor += colorinc
    # return animation
    return output


# TODO: add numcolors and buffer functionality
# Draws a polygon based on given points that moves across the display
def draw_moving_poly(points, colorwheel=clr.wheel, direction=1, numcolors=1, buffer=0):
    # determine relevant outer bound of polygon
    # use x coords
    if direction == 1 or -1:
        bound1 = columns
        bound2 = 0
        for i in points:
            if i[0] < bound1: bound1 = i[0]
            if i[0] > bound2: bound2 = i[0]
    # use y coords
    else:
        bound1 = rows
        bound2 = 0
        for i in points:
            if i[1] < bound1: bound1 = i[1]
            if i[1] > bound2: bound2 = i[1]
    # calculate width
    width = bound2 - bound1

    # calculate number of frames necessary for loop
    frames = numcolors * width

    # calculate quantity of polygons to draw per frame
    if direction == 1 or -1:
        numpolys = int(columns / width + 1)
    # use y coords
    else:
        numpolys = int(rows / width + 1)

    # prep output image
    global curroffset, offesetinc
    output = Image.new('RGB', (columns, rows * frames))

    # color cycle
    colorinc = 255 / frames
    currcolor = 0

    # calculate offsets based on direction
    if direction == 1:
        curroffset = 0
        offesetinc = columns / frames
    elif direction == 2:
        curroffset = 0
        offesetinc = rows / frames
    elif direction == -1:
        curroffset = columns
        offesetinc = -(columns / frames)
    elif direction == -2:
        curroffset = rows
        offesetinc = -(rows / frames)

    # generate frames
    for i in range(frames):
        # image manipulation
        clear_scratch()

        # draw polygons
        patternoffset = -width
        for _ in range(numpolys):
            if direction == 1:
                pointstemp = [[x[0] + patternoffset, x[1]] for x in points]
            elif direction == 2:
                pointstemp = [[x[0], x[1] + patternoffset] for x in points]
            elif direction == -1:
                pointstemp = [[x[0] - patternoffset, x[1]] for x in points]
            elif direction == -2:
                pointstemp = [[x[0], x[1] - patternoffset] for x in points]
            tuplepoints = tuple(tuple(x) for x in pointstemp)  # converts to tuple for passing into draw.polygon()
            draw.polygon(tuplepoints, fill=colorwheel(currcolor))
            patternoffset += width

        # for j in range(numcolors):

        output.paste(image, (0, rows * i))  # write image to animation

        # iterate
        currcolor += colorinc
        curroffset += offesetinc

        for i in points:
            if direction == 1:
                i[0] += 1
            elif direction == 2:
                i[1] += 1
            elif direction == -1:
                i[0] -= 1
            elif direction == -2:
                i[1] -= 1

    # return animation
    return output


# TODO: add logic to reverse math when height is greater than width
# Creates pin wheel animation
def draw_pin_wheel(frames=32, colorwheel=clr.wheel, width=20, ccw=False):
    radius = columns if (columns > rows) else rows
    constraint = columns if (columns < rows) else rows
    offset = (radius - constraint) / 2

    output = Image.new('RGB', (columns, rows * frames))

    theta = 360 / frames  # in degrees
    start = 0
    end = start + width

    # color cycle
    colorinc = 255 / frames
    currcolor = 0

    # generate frames
    for i in range(frames):
        # image manipulation
        clear_scratch()
        draw.pieslice((0, -offset, columns, columns - offset), start, end, colorwheel(currcolor))
        draw.pieslice((0, -offset, columns, columns - offset), start + 180, end + 180, colorwheel(currcolor))
        output.paste(image, (0, rows * i))  # write image to animation

        currcolor += colorinc

        # iterate
        start = theta - width if ccw else start + theta
        end = start + width

    # return animation
    return output


# Creates ripple animation
def draw_ripple(frames=32, colorwheel=clr.wheel, width=3):
    output = Image.new('RGB', (columns, rows * frames))

    radius = 0
    center = (rows / 2, columns / 2)
    maxradius = rows / 2 if rows > columns else columns / 2
    growrate = maxradius / frames

    # color cycle
    colorinc = 255 / frames
    currcolor = 0

    # generate frames
    for i in range(frames):
        # image manipulation
        clear_scratch()
        draw.ellipse((np.floor(center[1] - radius), np.floor(center[0] - radius), np.ceil(center[1] + radius),
                      np.ceil(center[0] + radius)), outline=colorwheel(currcolor), width=width)
        output.paste(image, (0, rows * i))  # write image to animation

        # iterate
        radius += growrate
        currcolor += colorinc

    # return animation
    return output


# Generating animations examples
# draw_spinning_line().save('img/spinningline.png') # basic usage
# draw_spinning_line(colorwheel=lambda a: (255,0,0)).save('img/spinningline.png') # lamda function for static color
# convert_right_advance(draw_spinning_line()).save('img/spinninglineexport.bmp') # example of use for exporting to other programs
# convert_down_advance('img/spinninglineexport.bmp').save('img/spinninglineimport.png') # example of use for importing from other programs
# draw_scroll_text('   Sample Text   ').save('img/text.png') # generated text animation
# draw_scanner(scanbouce=True).save('img/scanner.png') # example with arguments
# draw_pin_wheel(frames=64, colorwheel=clr.clubwheel, ).save('img/clubpinwheel.png') # another example with arguments

# Default animations
# draw_scroll_text('   Luminote   ').save('img/text.png')
# draw_scanner().save('img/scanner.png')
# draw_sparkle().save('img/sparkle.png')
# draw_spinning_line().save('img/spinningline.png')
# draw_pin_wheel().save('img/pinwheel.png')
# draw_ripple().save('img/ripple.png')

# WIP ignore for now
draw_moving_poly([[0, 0], [rows, 0], [rows * 2, rows], [rows, rows]], direction=1).save('img/candycane.png')
# draw_moving_poly([[columns-0, 0], [columns-rows, 0], [columns-rows * 2, rows], [columns-rows, rows]], direction=-1).save('img/candycane.png')
