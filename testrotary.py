#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Raspberry Pi Internet Radio
# using an HD44780 LCD display
# Rotary encoder version 4 x 20 character LCD version
#
# $Id: rradio4.py,v 1.42 2014/08/21 13:33:46 bob Exp $
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
# Author : (2014-2015) Julien Bellion
#
# This program uses  Music Player Daemon 'mpd'and it's client 'mpc'
# See http://mpd.wikia.com/wiki/Music_Player_Daemon_Wiki
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are
# implied or given. The authors shall not be liable for any loss or damage
# however caused.
#

import logging
import os
import signal
import sys
import time

import RPi.GPIO as GPIO
from encoders.encoder_class import Encoder
from encoders.simplerotary_class import RotaryEncoder
from utils.config_class import Config


# Class imports
# from encoders.gaugette_class import RotaryEncoder
# from encoders.rotary_class import RotaryEncoder
config = Config('/etc/pimpdradio.cfg')
logging.basicConfig(filename=config.getLogFile(), level=config.getLogLevel(), format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)s - %(message)s')

def tuner_event(event):
    print ('event')

    if event == Encoder.CLOCKWISE:
        print ('self.currentControler.tunerUp()')
    elif event == Encoder.ANTICLOCKWISE:
        print ('self.currentControler.tunerDown()')
    elif event == Encoder.BUTTONUP:
        print ('self.currentControler.tunerClickUp()')
    elif event == Encoder.BUTTONDOWN:
        print ('self.currentControler.tunerClickDown()')

tunerknob = RotaryEncoder(config.getSwitchMenuUp(),
                          config.getSwitchMenuDown(),
                          config.getSwitchMenuButton(),
                          tuner_event)


# Main routine ###
if __name__ == "__main__":
    

    while (True):
        time.sleep(1)


# End of script
