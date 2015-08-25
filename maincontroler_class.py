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

import logging

from controlers.controler_base import Controler
from controlers.MenuPrincipal import MenuPrincipal
from encoders.encoder_class import Encoder


class MainControler(Controler):

    currentControler = None
    ready = False
    startupSong = None
    
    btVolumeDown = False
    btTunerDown = False

    def __init__(self, config, lcd, mpdService):
        Controler.__init__(self, config, lcd, mpdService, None)

        self.setControler(MenuPrincipal(config, lcd, mpdService, self))
        #lcd._refreshLine1()

    # This is the callback routine to handle tuner events
    def tuner_event(self, event):
        logging.info('event')
        if self.ready and self.currentControler is not None:
            if event == Encoder.CLOCKWISE:
                self.currentControler.tunerUp()
            elif event == Encoder.ANTICLOCKWISE:
                self.currentControler.tunerDown()
            elif event == Encoder.BUTTONUP:
                self.btTunerDown = False
                self.currentControler.tunerClickUp()
            elif event == Encoder.BUTTONDOWN:
                self.btTunerDown = True
                if self.btVolumeDown:
                    self.execCommand("halt")
                self.currentControler.tunerClickDown()

    # This is the callback routine to handle volume events
    def volume_event(self, event):
        logging.info('event')
        if self.ready and self.currentControler is not None:
            if event == Encoder.CLOCKWISE:
                self.currentControler.volumeUp()
            elif event == Encoder.ANTICLOCKWISE:
                self.currentControler.volumeDown()
            elif event == Encoder.BUTTONUP:
                self.btVolumeDown = False
                self.currentControler.volumeClickUp()
            elif event == Encoder.BUTTONDOWN:
                self.btVolumeDown = True
                if self.btTunerDown:
                    self.execCommand("halt")
                self.currentControler.volumeClickDown()

    def setControler(self, newControler):
        logging.debug('MainControler..current : {0}'.format(self.currentControler))
        logging.debug('MainControler..new : {0}'.format(newControler))
        if self.currentControler is not None:
            self.currentControler.stop()
            
        if newControler is not None:
            self.currentControler = newControler
            self.currentControler.refresh()

    def setReady(self, isReady):
        self.ready = isReady

        self.startupSong = self.mpdService.getCurrentSong()
        logging.debug('Startup song : {0}'.format(self.startupSong))

        if isReady:
            self.currentControler.testStatus()
            self.mpdService.run()

    def stop(self):
        pass
# End of MainControler class
