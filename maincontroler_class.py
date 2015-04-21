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


from controlers.controler_base import Controler
from controlers.MenuPrincipal import MenuPrincipal
from encoders.encoder_class import Encoder

class MainControler(Controler):

    currentControler = None
    timerRefresh = None
    ready = False
    startupSong = None

    def __init__(self, config, lcd, mpd):
        Controler.__init__(self, config, lcd, mpd, None)

        self.currentControler = MenuPrincipal(config, lcd, mpd, self)
        lcd.setVolume(self.getVolume())

    # This is the callback routine to handle tuner events
    def tuner_event(self, event):
        if self.ready:
            if event == Encoder.CLOCKWISE:
                self.currentControler.tunerUp()
            elif event == Encoder.ANTICLOCKWISE:
                self.currentControler.tunerDown()
            elif event == Encoder.BUTTONUP:
                self.currentControler.tunerClickUp()
            elif event == Encoder.BUTTONDOWN:
                self.currentControler.tunerClickDown()

    # This is the callback routine to handle volume events
    def volume_event(self, event):
        if self.ready:
            if event == Encoder.CLOCKWISE:
                self.currentControler.volumeUp()
            elif event == Encoder.ANTICLOCKWISE:
                self.currentControler.volumeDown()
            elif event == Encoder.BUTTONUP:
                self.currentControler.volumeClickUp()
            elif event == Encoder.BUTTONDOWN:
                self.currentControler.volumeClickDown()

    def setControler(self, newControler):
        self.currentControler = newControler
        self.currentControler.refresh()
        
    def setReady(self, isReady):
        self.ready = isReady
        
        self.startupSong = self.mpd.currentsong()
        
        if isReady:
            self.currentControler.testStatus()
        
# End of MainControler class
