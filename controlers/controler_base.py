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
import time
from mpd import MPDClient


class Controler:

    lcd = None
    mpd = None
    config = None
    rootControler = None
    previousControler = None
    currentVolume = None

    def __init__(self, config, lcd, mpd,
                 rootControler, previousControler=None):
        self.config = config
        self.lcd = lcd
        self.mpd = mpd
        self.rootControler = rootControler
        self.previousControler = previousControler

    # Execute MPC comnmand using mpd library - Connect client if required
    def execMpc(self, cmd):
        try:
            ret = cmd
        except:
            logging.warning('MPD reconnection')
            if self.connect():
                ret = cmd
            else:
                logging.error('MPD reconnection failed')
        return ret

    # Connect to MPD
    def connect(self):
        connection = False
        retry = 2
        while retry > 0:
            self.mpd = MPDClient()    # Create the MPD client
            try:                
                self.mpd.timeout = 10
                self.mpd.idletimeout = None
                self.mpd.connect(self.config.getMpdHost(), self.config.getMpdPort())

                connection = True
                retry = 0
            except:
                time.sleep(0.5)
                # Wait for interrupt in the case of a shutdown
                if retry < 2:
                    logging.warning('LCD service restart')
                    self.execCommand("service mpd restart")
                else:
                    logging.warning('LCD service start')
                    self.execCommand("service mpd start")
                time.sleep(2)    # Give MPD time to restart
                retry -= 1

        return connection

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
        
    def stop(self):
        raise Exception('Controler.stop() must be implemented')

    def getVolume(self, refresh=False):
        if self.currentVolume is None or self.currentVolume == 0:
            volume = 0
            try:
                volume = int(self.mpd.status()['volume'])
            except:
                logging.warning('MPD getVolume failed')
                volume = 0

            self.currentVolume = volume

        return self.currentVolume

    def volumeUp(self):
        self.setVolume(self.getVolume() + 5)

    def volumeDown(self):
        self.setVolume(self.getVolume() - 5)

    def volumeClickDown(self):
        logging.debug("volumeClickDown NotImplementedError")

    def volumeClickUp(self):
        self.mpd.pause()

    def setVolume(self, volume):
        if volume > self.config.getMaxVolume():
            volume = self.config.getMaxVolume()
        elif volume < 0:
            volume = 0
        self.currentVolume = volume

        self.mpd.setvol(volume)
        self.lcd._refreshLine1()

    # Get current song information (Only for use within this module)
    def getCurrentSong(self):
        currentsong = ''
        try:
            currentsong = self.execMpc(self.mpd.currentsong())
        except:
            logging.error('Cannot get current song')            
            
        return currentsong

    # Get the title of the currently playing station or track from mpd
    def getCurrentTitle(self):
        title = ''
        currentsong = self.getCurrentSong()
        try:
            title = str(currentsong['title'])
        except:
            logging.warning('Current song : No title')

        if title == 'None':
            title = ''

        genre = ''
        try:
            genre = str(currentsong['genre'])
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
