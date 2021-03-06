# Functions for organization and animation of NeoPixels
# Most code in this file is only designed to be run natively on a raspberry pi or other control device.
import config
import time
import board
import neopixel
import colorwheels as clr
from PIL import Image

# Copy settings from config.py
num_pixels = config.num_pixels
rows = config.rows
columns = config.columns

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=config.brightness, auto_write=False, pixel_order=ORDER)


# TODO: save last frame state globally and only update pixels that need updated to reduce IO needed (and boost performance)

# Pixel mapping for addressing using a 2d array
# Direct matrix map generation
def direct_map():
    pixel_map = [[0 for x in range(columns)] for y in range(rows)]
    pixnum = 0
    for r in range(rows):
        for c in range(columns):
            pixel_map[r][c] = pixnum
            pixnum += 1
    return pixel_map


# Vertical zig zag map generation
def zigzag_map():
    pixel_map = [[0 for x in range(columns)] for y in range(rows)]
    pixnum = 0
    for c in range(columns):
        # top down for even columns (starting from index 0)
        if c % 2 == 0:
            for r in range(rows):
                pixel_map[r][c] = pixnum
                pixnum += 1
        # bottom up for odd columns
        else:
            pixnum += rows - 1
            for r in range(rows):
                pixel_map[r][c] = pixnum
                pixnum -= 1
            pixnum += rows + 1
    return pixel_map


def wheel_cycle(colorwheel=clr.wheel, wait=.005):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


# clears all pixels
def clear_pixels():
    pixels.fill((0, 0, 0))
    pixels.show()


# load and display a frame for set amount of time
def play_frame(pixel_map, source, wait, frame_number=0):
    img = Image.open(source)  # Can be many different formats.
    pic = img.load()
    # Writes each pixel to mapped pixels
    for r in range(rows):
        for c in range(columns):
            pixels[pixel_map[r][c]] = pic[c, (r + frame_number * rows)]
    pixels.show()
    time.sleep(wait)


# draws frame ignoring black pixels, requires pixels.show() to display
def draw_frame(pixel_map, source, frame_number=0):
    img = Image.open(source)  # Can be many different formats.
    # Writes each pixel to mapped pixels
    for r in range(rows):
        for c in range(columns):
            if not (img[c, (r + frame_number * rows)] == (0, 0, 0)):
                pixels[pixel_map[r][c]] = img[c, (r + frame_number * rows)]


# plays through a sequence of frames at given framerate
def play_animation(pixel_map, source, fps=16):
    image = Image.open(source)
    frametime = 1 / fps
    for i in range(int(image.height / rows)):
        play_frame(pixel_map, source, i, frametime)
