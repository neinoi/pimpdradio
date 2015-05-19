#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Raspberry Pi Main Controler class
#
# Copyright Julien Bellion 2014 (https://github.com/neinoi)
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are
# implied or given.
# The authors shall not be liable for any loss or damage however caused.
#

import logging
import os

class Controler():

    lcd = None
    rootControler = None
    previousControler = None

    mpdService = None
    config = None

    def __init__(self, config, lcd, mpdService, rootControler, previousControler=None):
        self.config = config
        self.mpdService = mpdService
        
        self.lcd = lcd
        self.rootControler = rootControler
        self.previousControler = previousControler

    # Execute system command
    def execCommand(self, cmd):
        p = os.popen(cmd)
        return p.readline().rstrip('\n')

    def refresh(self):
        logging.debug("refresh NotImplementedError")

    def testStatus(self):
        logging.debug("testStatus NotImplementedError")

    def tunerUp(self):
        logging.debug("tunerUp NotImplementedError")

    def tunerDown(self):
        logging.debug("tunerDown NotImplementedError")

    def tunerClickDown(self):
        logging.debug("tunerClickDown NotImplementedError")

    def tunerClickUp(self):
        logging.debug("tunerClickUp NotImplementedError")
        
    def getVolume(self, refresh=False):
        if self.currentVolume is None or self.currentVolume == 0:
            volume = 0
            try:
                volume = int(self.mpdService.getStatus('volume'))
            except:
                logging.warning('MPD getVolume failed')
                volume = 0

            self.currentVolume = volume

        return self.currentVolume

    def volumeUp(self):
        self.mpdService.changeVolume(1)

    def volumeDown(self):
        self.mpdService.changeVolume(-1)

    def volumeClickDown(self):
        logging.debug("volumeClickDown NotImplementedError")

    def volumeClickUp(self):
        self.mpdService.pause()

    # Get the title of the currently playing station or track from mpd
    def getCurrentTitle(self):
        title = ''
        try:
            title = str(self.mpdService.getCurrentSong()['title'])
        except:
            logging.warning('Current song : No title')

        if title == 'None':
            title = ''

        genre = ''
        try:
            genre = str(self.mpdService.getCurrentSong()['genre'])
        except:
            logging.warning('Current song : No genre')

        if genre == 'None':
            genre = ''

        if title == '':
            # Usually used if this is a podcast
            if len(genre) > 0:
                title = genre

        return title
# End of MainControler class
