#Luminote
Still very much a work in progress
###Setup
Read through the global variables in animations.py and configure to match how your leds are wired.

To install dependencies run: 
```bash
sudo apt-get install libjpeg-dev zlib1g-dev
sudo pip install -r requirements.txt
```
This may take a few minutes so just be patient

###Config

###Prepping images
Images must be in an 8 bit per channel rgb format, complete black (0,0,0) represents an off pixel.

###Custom Animations
Most functions in this library are built on Pillow