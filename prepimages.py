# TODO: merge with prepimages.py and increase modularity
# Script used to prep images for use by animations.py when using an led matrix
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


# converts animation to advance right by frame instead of down for compatibility with other tools
def convert_right_advance(image):
    frames = int(image.height/rows)

    output = Image.new('RGB', (columns * frames, rows))

    # generate frames
    for i in range(frames):
        # image manipulation
        output.paste(image.crop((0, rows * i, columns, rows * i + rows)), (columns * i, 0))  # write image to animation

    # return animation
    return output


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
def draw_scanner(frames=32, colorwheel=clr.wheel, width=3, scandirection=1, scanbouce=False):
    global curroffset, offesetinc
    output = Image.new('RGB', (columns, rows * frames))

    # recursively call draws_scanner twice to generate each half of the output
    if scanbouce:
        output.paste(draw_scanner(frames=int(frames/2), colorwheel=colorwheel, width=width, scandirection=scandirection), (0, 0))
        output.paste(draw_scanner(frames=int(frames/2), colorwheel=colorwheel, width=width, scandirection=0-scandirection), (0, frames*int(rows/2)))

    else:
        # color cycle
        colorinc = 255 / frames
        currcolor = 0

        if (scandirection == 1):
            curroffset = 0
            offesetinc = columns/frames
        elif (scandirection == 2):
            curroffset = 0
            offesetinc = rows / frames
        elif (scandirection == -1):
            curroffset = columns
            offesetinc = -(columns / frames)
        elif (scandirection == -2):
            curroffset = rows
            offesetinc = -(rows / frames)

        # generate frames
        for i in range(frames):

            # image manipulation
            clear_scratch()
            if (scandirection == 1):
                draw.rectangle((curroffset-width/2, 0, curroffset+width/2, rows), fill=colorwheel(currcolor))
            elif (scandirection == 2):
                draw.rectangle((0, curroffset-width/2, columns, curroffset+width/2), fill=colorwheel(currcolor))
            elif (scandirection == -1):
                draw.rectangle((curroffset+width/2, 0, curroffset-width/2, rows), fill=colorwheel(currcolor))
            elif (scandirection == -2):
                draw.rectangle((0, curroffset-width/2, columns, curroffset+width/2), fill=colorwheel(currcolor))

            output.paste(image, (0, rows * i))  # write image to animation

            # iterate
            currcolor += colorinc
            curroffset += offesetinc

    # return animation
    return output

# TODO: candy cane

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


# TODO: add logic to reverse math when height is greater than width
# Creates roulette wheel animation
def draw_roulette_wheel(frames=32, colorwheel=clr.wheel, width=20, ccw=False):
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
# TODO: add fill option
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

# Generate default animations
# draw_spinning_line().save('img/spinningline.png')
# convert_right_advance(draw_spinning_line()).save('img/spinninglineconv.png')
# draw_roulette_wheel().save('img/roulettewheel.png')
# draw_roulette_wheel(frames=64, colorwheel=clr.clubwheel, ).save('img/clubroulettewheel.png')
# draw_scroll_text('   Sample Text   ').save('img/text.png')
# draw_ripple().save('img/ripple.png')
# draw_scanner(scanbouce=True).save('img/scanner.png')
