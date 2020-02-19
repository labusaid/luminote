# Luminote
This is still very much a work in progress, if you have feature requests or bug reports please feel free to share them on [github](https://github.com/labusaid/luminote).
This project is originally designed to drive a matrix of ws2812 LEDs through a raspberry pi, but once the majority of features are impimented I plan on slowly increasing compatibility for different hardware setups and layouts.

## Setup
Read through the variables in config.py and configure to match how your leds are wired.

Assuming I actually remembered to keep everything up this should be the entire setup process.  


```bash
git clone https://github.com/labusaid/luminote
```
edit config.py to match your hardware setup
```bash
sudo apt-get install libjpeg-dev zlib1g-dev ffmpeg libatlas-base-dev
sudo pip3 install -r requirements.txt
python3 prepimages.py
sudo python3 luminote.py
```
This may take a few minutes so just be patient.

## Workflow
Luminote is designed to be as modular as possible to ensure that a majority of the code is hardware agnostic and customization takes as little effort as possible.
Animations are saved as .png files with as a sequence of frames representing the matrix appended vertically.
 
#### Default Animations
By default running prepimages.py will generate one of each of the animations with the default arguments and save it in /img/

## Tools
#### Prepping custom images
TODO: add brief description of each animation and configuration.

## Integrated controller (WIP)
#### Menu system
| Name | Code | Active | Function |
| --- | :---: | :--- | ---|
| Home | HOME | default state 
| Settings | SETTNG | hold singleplayer button for 3 seconds | used to configure general settings
| Cues | CUES | hold two player button for 3 seconds | used to map buttons to cues
Menu system is still subject to change