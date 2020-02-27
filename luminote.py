import config
from animations import *

# from gpiozero import ButtonBoard

# LED mapping
if config.matrixmap == 'zigzag':
    print('using zigzag map with ' + str(columns) + ' columns and ' + str(rows) + ' rows')
    matrix_map = zigzag_map()
elif config.matrixmap == 'direct':
    print('using direct map with ' + str(columns) + ' columns and ' + str(rows) + ' rows')
    matrix_map = direct_map()
else:
    print('pixel map not correctly specified in config.py')

# Button mapping
# btns = ButtonBoard(35, 36, 37, 38)

# Menu system
machinestate = 'default'


# Cue Control
def activate_cue(cue):
    print(cue + 'activated')


# Note: I belive it would be technically more efficient to define each button separately and have individual callbacks, but in this case I'm favoring clean code
# def scan_buttons():
#     if btns[0]:
#         activate_cue('test')


# ButtonBoard callback
# btns.when_activated(scan_buttons)

# Main
print('Luminote started\nUse Ctrl+C to exit')
while True:
    while True:
        play_animation(matrix_map, 'img/text.png', 32)
        for i in range(5):
            play_animation(matrix_map, 'img/scanner.png')
        for i in range(5):
            play_animation(matrix_map, 'img/spinningline.png')
        for i in range(5):
            play_animation(matrix_map, 'img/pinwheel.png')
        for i in range(5):
            play_animation(matrix_map, 'img/ripple.png', 32)
