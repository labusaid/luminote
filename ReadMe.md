# Luminote
This is still very much a work in progress, if you have feature requests or bug reports, please feel free to share them on [github](https://github.com/labusaid/luminote).
This project is originally designed to drive a matrix of ws2812 LEDs through a raspberry pi, but once the majority of features are impimented I plan on slowly increasing compatibility for different hardware setups and layouts.

## Setup
Read through the variables in config.py and configure to match how your leds are wired.

To install dependencies run: 
```bash
sudo apt-get install libjpeg-dev zlib1g-dev ffmpeg
sudo pip install -r requirements.txt
```
This may take a few minutes so just be patient

## Workflow
Luminote is designed to be as modular as possible to ensure that a majority of the code can be reused regardless of the hardware that is used.
 
## Tools
#### Default Animations
There are a handful of code driven example animations in animations.py that can be used for testing or basic functions.

#### Prepping images
In the case that you want to import your own animations there are a few functions to ensure that they are compatible with the driver code. 
Images must be in an 8 bit per channel rgb format, complete black (0,0,0) represents an off pixel.

## Integrated controller
#### Menu system
| Name | Code | Active | Function |
| --- | :---: | :--- | ---|
| Home | HOME | default state 
| Settings | SETTNG | hold singleplayer button for 3 seconds | used to configure general settings
| Cues | CUES | hold two player button for 3 seconds | used to map buttons to cues
Menu system is still subject to change