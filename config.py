# General configuration shared globally

# Grid layout
# Currently it's recommended to make the width (columns) to larger dimension as some functions are not fully aspect ratio agnostic yet
rows = 8
columns = 32
matrixmap = 'zigzag'  # use 'direct' for direct map

# LED configuration
# RGB/GRB and GPIO pin selection can be done directly in animations.py
# The number of pixels (only needs to be manually configured if using non-standard pixel mapping)
num_pixels = rows * columns
# LED brightness (color accuracy will fade the more this is turned down due to the nature of how these LEDs work)
brightness = .25

# Font for text drawing
font = 'resources/visitor1.ttf'

# For music analysis
music_path = 'music/example.mp3'
