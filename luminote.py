import config
from animations import *
from gpiozero import ButtonBoard
from signal import pause
import concurrent.futures

# Threading was chosen over multiprocessing due to most deployments being run on single core CPUs and the loop program being IOBound

# LED mapping
if config.matrixmap == 'zigzag':
    print(f'using zigzag map with {columns} columns and {rows} rows')
    matrix_map = zigzag_map()
elif config.matrixmap == 'direct':
    print(f'using direct map with {columns} columns and {rows} rows')
    matrix_map = direct_map()
else:
    print('pixel map not correctly specified in config.py')

# Button mapping
btns = ButtonBoard(35, 36, 37, 38)

# Menu system
machinestate = 'default'

# Cue Control
def activate_cue(cue):
    print(f'Cue "{cue}" activated')


# Note: I belive it would be technically more efficient to define each button separately and have individual callbacks, but in this case I'm favoring clean code
def scan_buttons(button):
    if button == 0:
        activate_cue('test')
    elif button == 1:
        pass


# ButtonBoard callback
btns.when_activated(scan_buttons)

# TODO: implement threading and run driver code on a separate thread with interrupts on button events
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
