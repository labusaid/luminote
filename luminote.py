import config
import animations as anima
import gpiozero

# Main
test_map = anima.zigzag_map()

while True:
    # anima.play_animation(test_map, 'img/roulettewheel.png', 15)
    # anima.play_animation(test_map, 'img/text.png', 30)
    anima.club_cycle(.005)