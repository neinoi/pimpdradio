#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Raspberry Pi Rotary Encoder Class
# $Id: rotary_class.py,v 1.4 2014/06/02 14:31:49 bob Exp $
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# This class uses standard rotary encoder with push switch
#
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are
#             implied or given. The authors shall not be liable for any loss
#             or damage however caused.
#

from encoder_class import Encoder
import RPi.GPIO as GPIO


class RotaryEncoder(Encoder):

    pinA = None
    pinB = None
    button = None
    callback = None
    oldPinA = None
    previous = 0

    # Initialise rotary encoder object
    def __init__(self, pinA, pinB, button, callback):
        self.pinA = pinA
        self.pinB = pinB
        self.button = button
        self.callback = callback
        self.oldPinA = False
        self.previous = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # The following lines enable the internal pull-up resistors
        # on version 2 (latest) boards
        GPIO.setup(self.pinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Add event detection to the GPIO inputs
        GPIO.add_event_detect(self.pinA, GPIO.BOTH, callback=self.rotate_event)
        GPIO.add_event_detect(self.pinB, GPIO.BOTH, callback=self.rotate_event)
        
        # Pour le bouton
        GPIO.add_event_detect(
            self.button, GPIO.BOTH, callback=self.button_event, bouncetime=75)
        return

    # Call back routine called by switch events
    def rotate_event(self, switch):
        
        pA = GPIO.input(self.pinA)
        pB = GPIO.input(self.pinB)
        
        if pA == False and pB == False:
            self.previous = 0
        elif self.previous == 0 and pA == True:
            self.previous = self.CLOCKWISE
            self.callback(self.CLOCKWISE)
        elif self.previous == 0 and pB == True:
            self.previous = self.ANTICLOCKWISE
            self.callback(self.ANTICLOCKWISE)
        else:
            self.previous = self.NONE
                                        
        return

    # Push button up event
    def button_event(self, button):
        if GPIO.input(button):
            event = self.BUTTONUP
        else:
            event = self.BUTTONDOWN
        self.callback(event)
        return

    # Get a switch state
    def getSwitchState(self, switch):
        return GPIO.input(switch)

# End of RotaryEncoder class
