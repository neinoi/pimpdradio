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

MAX_VOLUME = 80

class Controler:

    lcd = None
    mpd = None
    rootControler = None
    previousControler = None
    currentVolume = None
        
    mpc = "/usr/bin/mpc"	# Music Player Client

    def __init__(self, lcd, mpd, rootControler, previousControler=None):
        self.lcd = lcd
        self.mpd = mpd
        self.rootControler = rootControler
        self.previousControler = previousControler
        return

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
        raise NotImplementedError( "Should have implemented this" )

    def tunerUp(self):
        raise NotImplementedError( "Should have implemented this" )
    
    def tunerDown(self):
        raise NotImplementedError( "Should have implemented this" )
    
    def tunerClickDown(self):
        raise NotImplementedError( "Should have implemented this" )
    
    def tunerClickUp(self):
        raise NotImplementedError( "Should have implemented this" )

    def getVolume(self, refresh=False):
        if self.currentVolume is None or refresh is True:
            volume = 0
            try:
                stats = self.mpd.status()
                volume = int(stats.get("volume"))
            except:
                volume = 0
    
            if volume == str("None"):
                volume = 0
            
            if volume > MAX_VOLUME:
                volume = MAX_VOLUME
            
            self.currentVolume = volume
        
        return self.currentVolume

    def volumeUp(self):
        self.setVolume(self.getVolume() + 5)
        return
    
    def volumeDown(self):
        self.setVolume(self.getVolume() - 5)
        return
    
    def volumeClickDown(self):
        raise NotImplementedError( "Should have implemented this" )

    def volumeClickUp(self):
        raise NotImplementedError( "Should have implemented this" )

        
    def setVolume(self,volume):
        if volume > MAX_VOLUME:
            volume = MAX_VOLUME
        elif volume < 0:
            volume = 0
        self.currentVolume = volume
        
        self.execMpc(self.mpd.setvol(volume))

# End of MainControler class
