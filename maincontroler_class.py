#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Raspberry Pi Main Controler class
#
# Copyright Julien Bellion 2014-2015 (https://github.com/neinoi)
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are
# implied or given.
# The authors shall not be liable for any loss or damage however caused.
#

import threading

from time import gmtime, strftime

from controlers.controler_base import Controler
from controlers.MenuPrincipal import MenuPrincipal
from encoders.encoder_class import Encoder

class MainControler(Controler):

    currentControler = None
    timerRefresh = None

    def __init__(self, lcd, mpd):
        Controler.__init__(self, lcd, mpd, None)

        self.currentControler = MenuPrincipal(lcd, mpd, self)

        threading.Timer(1, self._refresh, [1]).start()

        return

    # This is the callback routine to handle tuner events
    def tuner_event(self, event):
        if event == Encoder.CLOCKWISE:
            self.currentControler.tunerUp()
        elif event == Encoder.ANTICLOCKWISE:
            self.currentControler.tunerDown()
        elif event == Encoder.BUTTONUP:
            self.currentControler.tunerClickUp()
        elif event == Encoder.BUTTONDOWN:
            self.currentControler.tunerClickDown()
        
        return

    # This is the callback routine to handle volume events
    def volume_event(self, event):
        if event == Encoder.CLOCKWISE:
            self.currentControler.volumeUp()
        elif event == Encoder.ANTICLOCKWISE:
            self.currentControler.volumeDown()
        elif event == Encoder.BUTTONUP:
            self.currentControler.volumeClickUp()
        elif event == Encoder.BUTTONDOWN:
            self.currentControler.volumeClickDown()

        return

    def setControler(self, newControler):
        self.currentControler = newControler
        self.currentControler.refresh()

        return


    #On rafraîchit uniquement la première ligne (Date/Heure et Volume)
    def _refresh(self,tempo = 1):
        volume = self.getVolume(True)
        
        ligneDeb = strftime("%d/%m %H:%M", gmtime())
        ligneFin = "Vol " + str(volume)
        
        while len(ligneDeb) + len(ligneFin) < 20:
            ligneDeb += ' '
            
        self.lcd.setLine1(ligneDeb + ligneFin)
        
        threading.Timer(tempo, self._refresh, [tempo]).start()
        
        return
        
# End of MainControler class
