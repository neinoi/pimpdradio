#!/usr/bin/env python
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
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#             The authors shall not be liable for any loss or damage however caused.
#

from encoder_class import Encoder

import threading
import pimpdradio.gaugette.rotary_encoder
import pimpdradio.gaugette.switch

TEMPO = 0.1

class RotaryEncoder(Encoder):

    TEMPO = 0.1

    last_state = None
    callback = None

    encoder = None
    switch = None

    # Initialise rotary encoder object
    def __init__(self,pinUp,pinDown,pinSwitch,callback):
        self.callback = callback

        self.rotary = pimpdradio.gaugette.rotary_encoder.RotaryEncoder.Worker(pinUp, pinDown)
        self.rotary.start()
        self.switch = pimpdradio.gaugette.switch.Switch(pinSwitch)

        threading.Timer(TEMPO, self._test).start()

        return


    def _test(self):
        #rotary test
        delta = self.rotary.get_delta()
        if delta!=0:
            if delta > 0:
                event = self.CLOCKWISE
            else:
                event = self.ANTICLOCKWISE
            self.callback(event)

        #button test
        sw_state = self.switch.get_state()
        if sw_state != self.last_state:
            if sw_state == 0:
                event = self.BUTTONUP
            else:
                event = self.BUTTONDOWN
            self.callback(event)
            self.last_state = sw_state

        threading.Timer(TEMPO, self._test).start()
        return

# End of RotaryEncoder class









