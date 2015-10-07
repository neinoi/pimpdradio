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

import time
import logging

from bottle import route, run, template

# Class imports
from display.lcd_class import Lcd
from utils.config_class import Config

# from encoders.gaugette_class import RotaryEncoder
# from encoders.rotary_class import RotaryEncoder
from encoders.simplerotary_class import RotaryEncoder

from maincontroler_class import MainControler
from controlers.MpdService import MPDService

config = Config('/etc/pimpdradio.cfg')
logging.basicConfig(filename=config.getLogFile(), level=config.getLogLevel(), format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)s - %(message)s')

mpdService = MPDService(config)

tempo = 0.3
lcd = Lcd(config, mpdService)

logging.info('Initializing main controller ...')
controler = MainControler(config, lcd, mpdService)
time.sleep(5)

logging.info('Initializing tuner controls ...')
tunerknob = RotaryEncoder(config.getSwitchMenuUp(),
                          config.getSwitchMenuDown(),
                          config.getSwitchMenuButton(),
                          controler.tuner_event)
#time.sleep(5)

logging.info('Initializing volume controls ...')
volumeknob = RotaryEncoder(config.getSwitchVolumeUp(),
                           config.getSwitchVolumeDown(),
                           config.getSwitchVolumeButton(),
                           controler.volume_event)
#time.sleep(5)
controler.setReady(True)


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='0.0.0.0', port=8080)

# End of script
