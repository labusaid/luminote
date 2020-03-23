import config
from animations import direct_map, zigzag_map, wheel_cycle, clear_pixels, draw_frame, play_frame, play_animation
from gpiozero import ButtonBoard
from threading import Thread, Event
from signal import pause
import concurrent.futures

# LED mapping
if config.matrixmap == 'zigzag':
    print(f'using zigzag map with {config.columns} columns and {config.rows} rows')
    matrix_map = zigzag_map()
elif config.matrixmap == 'direct':
    print(f'using direct map with {config.columns} columns and {config.rows} rows')
    matrix_map = direct_map()
else:
    print('pixel map not correctly specified in config.py')

# Button mapping
btns = ButtonBoard(5, 6, 13, 19)

# Flow control
machinestate = 'default'


# Triggered on cue activation
def activate_cue(cue):
    print(f'Cue "{cue}" was activated')


# Triggered on any button press
def on_button_press(buttons):
    # Code to isolate button which caused state change event
    # if lastbuttonspressed < sum(buttons):
    #     return
    buttontotal = 0
    for button in buttons.value:
        buttontotal += button

    if buttontotal == 0:
        return

    if buttons.value[0] == 1:
        activate_cue('test0')
    if buttons.value[1] == 1:
        activate_cue('test1')
    if buttons.value[2] == 1:
        activate_cue('test2')
    if buttons.value[3] == 1:
        activate_cue('test3')


# Main
if __name__ == '__main__':
    print('Luminote started\nUse Ctrl+C to exit')

    # set ButtonBoard callback
    btns.when_activated = on_button_press

    pause()
    # while True:
    # play_animation(matrix_map, 'img/text.png', 32)
