#!/usr/bin/env python
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

# Class imports
from utils.radio_daemon import Daemon
from utils.lcd_class import Lcd
from mpd import MPDClient

# import gaugette.rotary_encoder
# import gaugette.switch
#from gaugette_class import RotaryEncoder

from encoders.rotary_class import RotaryEncoder
from maincontroler_class import MainControler

# Switch definitions (Bob)
MENU_UP = 17
MENU_DOWN = 18
MENU_SWITCH = 25

VOLUME_UP = 15
VOLUME_DOWN = 14
VOLUME_SWITCH = 4

# With Gaugette :
# MENU_SWITCH = 6
# MENU_UP = 0
# MENU_DOWN = 1
# VOLUME_SWITCH = 7
# VOLUME_UP = 16
# VOLUME_DOWN = 15

revision = 2
tempo = 0.2

lcd = Lcd()
mpd = MPDClient()    # Create the MPD client
mpd.connect("localhost", 6600)  # connect to localhost:6600

lcd.init(revision, tempo)
lcd.setWidth(20)

controler = MainControler(lcd, mpd)
volumeknob = RotaryEncoder(VOLUME_UP, VOLUME_DOWN, VOLUME_SWITCH,
                           controler.volume_event)
tunerknob = RotaryEncoder(MENU_UP, MENU_DOWN, MENU_SWITCH,
                          controler.tuner_event)


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
            log.message(message, log.INFO)
            print message
        else:
            message = "radiod running pid " + str(pid)
            log.message(message, log.INFO)
            print message
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
#     # Rapid display of track play status
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


# ### Main routine ###
if __name__ == "__main__":
    daemon = MyDaemon('/var/run/radiod.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            os.system("service mpd stop")
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        elif 'version' == sys.argv[1]:
            print "Version " + radio.getVersion()
        else:
            print "Unknown command: " + sys.argv[1]
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart|status|version" % sys.argv[0]
        sys.exit(2)

# End of script
