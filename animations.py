# Functions for organization and animation of NeoPixels
import time
import board
import neopixel

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 256

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=.05, auto_write=False, pixel_order=ORDER)

# Pixel mapping for addressing using a 2d array
# Direct matrix map generation
def direct_map(rows, columns):
    pixel_map = [[0 for x in range(columns)] for y in range(rows)]
    pixnum = 0
    for r in range(rows):
        for c in range(columns):
            pixel_map[r][c] = pixnum
            pixnum += 1
    return pixel_map

# Vertical zig zag map generation
def zigzag_map(rows, columns):
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

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
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

def clear_pixels():
    pixels.fill((0,0,0))
    pixels.show()

# Main
rainbow_cycle(.0000001)
clear_pixels()