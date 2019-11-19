# Functions for organization and animation of NeoPixels
# Most code in this file is only designed to be run natively on a raspberry pi or other control device.
import config
import time
import board
import neopixel
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

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=.05, auto_write=False, pixel_order=ORDER)

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
        if (c%2 == 0):
            for r in range(rows):
                pixel_map[r][c] = pixnum
                pixnum += 1
        # bottom up for odd columns
        else:
            pixnum += rows-1
            for r in range(rows):
                pixel_map[r][c] = pixnum
                pixnum -= 1
            pixnum += rows+1
    return pixel_map

# Input a value 0 to 255 to get a color value.
# The colours are a transition r - g - b - back to r.
def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

# fills pixels columns by column with specified color
def color_wipe(pixel_map, wait, red, green, blue):
    for i in range(len(pixel_map[0])):
        for r in range(len(pixel_map)):
            pixels[pixel_map[r][i]] = (red,green,blue)
        pixels.show()
        time.sleep(wait)

# clears all pixels
def clear_pixels():
    pixels.fill((0,0,0))
    pixels.show()

# load and display a frame for set amount of time
def play_frame(pixel_map, source, frame_number, wait):
    img = Image.open(source)  # Can be many different formats.
    pic = img.load()
    # Writes each pixel to mapped pixels
    for r in range(rows):
        for c in range(columns):
            pixels[pixel_map[r][c]] = pic[c, (r + frame_number*rows)]
    pixels.show()
    time.sleep(wait)

# draws frame ignoring black pixels, requires pixels.show() to display
def draw_frame(pixel_map, source, frame_number):
    img = Image.open(source)  # Can be many different formats.
    # Writes each pixel to mapped pixels
    for r in range(rows):
        for c in range(columns):
            if not (img[c, (r + frame_number*rows)] == (0,0,0)):
                pixels[pixel_map[r][c]] = img[c, (r + frame_number*rows)]

# places through a sequence of frames at given framerate
def play_animation(pixel_map, source, fps):
    image = Image.open(source)
    frametime = 1/fps
    for i in range (int(image.height/rows)):
        play_frame(pixel_map, source, i, frametime)

test_map = zigzag_map()
# color_wipe(test_map, .05, 255,0,0)
# color_wipe(test_map, .05, 0,0,0)
while True:
    # play_animation(test_map, 'img/roulettewheel.png', 15)
    play_animation(test_map, 'img/text.png', 30)
