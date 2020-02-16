import config
import animations as anima
from gpiozero import ButtonBoard
from time import sleep
import midi #py-midi
from midi import MidiConnector, ControlChange, Message

# LED mapping
test_map = anima.zigzag_map()
# MIDI setup
conn = MidiConnector('/dev/serial0')
# Button setup
btns = ButtonBoard(35,36,37,38)

# Menu system
machinestate = 'default'

# Main
# while True:
#     # anima.play_animation(test_map, 'img/roulettewheel.png', 15)
#     # anima.play_animation(test_map, 'img/text.png', 30)
#     anima.club_cycle(.005)

# Cue Control
def activate_cue(cue):
    print(cue + 'activated')

# TODO: usb midi control

# Note: it would be technically more efficient to define each button separately and have individual callbacks, but in this case I'm favoring clean code
def scan_buttons():
    if btns[0]:
        activate_cue('test')

# ButtonBoard callback
btns.when_activated(scan_buttons)

