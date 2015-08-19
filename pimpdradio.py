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

import os
import RPi.GPIO as GPIO
import signal
import sys
import time
import logging

# Class imports
from utils.radio_daemon import Daemon
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


# Signal SIGTERM handler
def signalHandler(signal, frame):
    global log
    pid = os.getpid()
    log.message("Radio stopped, PID " + str(pid), log.INFO)
    GPIO.cleanup()
    sys.exit(0)


# Daemon class
class MyDaemon(Daemon):

    def run(self):
        signal.signal(signal.SIGTERM, signalHandler)

        progcall = str(sys.argv)

        while True:
            time.sleep(1)

    def status(self):
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "radiod status: not running"
            logging.info(message)
        else:
            message = "radiod running pid " + str(pid)
            logging.info(message)
        return

# End of class overrides


# def interrupt():
#     global radio
#     interrupt = False
#     switch = radio.getSwitch()
#     if switch > 0:
#         interrupt = get_switch_states(lcd, radio, rss, volumeknob, tunerknob)
#         radio.setSwitch(0)
#
# Rapid display of track play status
#     if radio.getSource() == radio.PLAYER:
#         if radio.volumeChanged():
#             displayLine4(lcd, radio, "Volume " + str(radio.getVolume()))
#             time.sleep(0.5)
#         else:
#             lcd.line4(radio.getProgress())
#
#     elif (radio.getTimer() and not interrupt) or radio.volumeChanged():
#         displayLine4(lcd, radio, "Volume " + str(radio.getVolume()))
#         interrupt = checkTimer(radio)
#
#     if not interrupt:
#         interrupt = checkState(radio)
#
#     return interrupt


def no_interrupt():
    return False


# Execute system command
def exec_cmd(cmd):
    p = os.popen(cmd)
    result = p.readline().rstrip('\n')
    return result


# Main routine ###
if __name__ == "__main__":
    daemon = MyDaemon('/var/run/radiod.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        elif 'version' == sys.argv[1]:
            print "Version 0.1"
        else:
            print "Unknown command: " + sys.argv[1]
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart|status|version" % sys.argv[0]
        sys.exit(2)

# End of script
