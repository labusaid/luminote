# Functions take a value between 0 and 255 and return a corresponding rgb tuple

# Input a value 0 to 255 to get a color value.
# The colours are a transition r - g - b - back to r.
def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)


# Red and Blue gradient
def clubwheel(pos):
    g = 0
    r = int(pos)
    b = int(255 - pos)
    return (r, g, b)