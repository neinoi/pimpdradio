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
            
    def __init__(self, config, lcd, mpd, rootControler, previousControler=None):
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
            if self.connect(self.mpdport):
                ret = cmd
        return ret


    # Connect to MPD
    def connect(self, port):
        connection = False
        retry = 2
        while retry > 0:
            self.mpd = MPDClient()    # Create the MPD client
            try:
                self.mpd.timeout = 10
                self.mpd.idletimeout = None
                self.mpd.connect("localhost", port)

                connection = True
                retry = 0
            except:
                time.sleep(0.5)    # Wait for interrupt in the case of a shutdown
                if retry < 2:
                    self.execCommand("service mpd restart")
                else:
                    self.execCommand("service mpd start")
                time.sleep(2)    # Give MPD time to restart
                retry -= 1

        return connection

    # Execute system command
    def execCommand(self,cmd):
        p = os.popen(cmd)
        return  p.readline().rstrip('\n')

    def refresh(self):
        print "refresh NotImplementedError"

    def testStatus(self):
        print "testStatus NotImplementedError"

    def tunerUp(self):
        print "tunerUp NotImplementedError"
    
    def tunerDown(self):
        print "tunerDown NotImplementedError"
    
    def tunerClickDown(self):
        print "tunerClickDown NotImplementedError"
    
    def tunerClickUp(self):
        print "tunerClickUp NotImplementedError"

    def getVolume(self, refresh = False):
        if self.currentVolume is None or self.currentVolume == 0:
            volume = 0
            try:
                stats = self.mpd.status()
                volume = int(stats.get("volume"))
            except:
                volume = 0
    
            if volume == str("None"):
                volume = 0
            
            self.currentVolume = volume
        
        return self.currentVolume

    def volumeUp(self):
        self.setVolume(self.getVolume() + 5)
    
    def volumeDown(self):
        self.setVolume(self.getVolume() - 5)
    
    def volumeClickDown(self):
        print "columeClickDown NotImplementedError"

    def volumeClickUp(self):
        print "volumeClickUp NotImplementedError"
        
    def setVolume(self,volume):
        if volume > self.config.getMaxVolume():
            volume = self.config.getMaxVolume()
        elif volume < 0:
            volume = 0
        self.currentVolume = volume
        
        self.execMpc(self.mpd.setvol(volume))
        self.lcd.setVolume(volume)

    # Get current song information (Only for use within this module)
    def getCurrentSong(self):
        currentsong = ''
        try:
            currentsong = self.execMpc(self.mpd.currentsong())
        except:
            # Try re-connect and status
            try:
                if self.connect(self.mpdport):
                    currentsong = self.execMpc(self.mpd.currentsong())
            except:
                pass
        return currentsong

    # Get the title of the currently playing station or track from mpd 
    def getCurrentTitle(self):
        try:
            currentsong = self.getCurrentSong()
            title = str(currentsong.get("title"))
        except:
            title = ''

        if title == 'None':
            title = ''

        try:
            genre = str(currentsong.get("genre"))
        except:
            genre = ''
        if genre == 'None':
            genre = ''

        if title == '':
            # Usually used if this is a podcast
            if len(genre) > 0:
                title = genre    

        return title
# End of MainControler class
