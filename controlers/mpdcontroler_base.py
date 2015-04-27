#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
'''
Created on 22 avr. 2015

@author: julien
'''

import logging
import time
from mpd import MPDClient

mpdCli = None

class MPDControler:
    '''
    classdocs
    '''

    config = None
    mpd = None

    def __init__(self, config):
        '''
        Constructor
        '''
        self.config = config
        
        self.connect()

        
    def check(self):
        if self.mpd is None:
            self.connect()
    
        
    # Execute MPC command using mpd library - Connect client if required
    def execMpc(self, cmd):
        try:
            ret = cmd
        except:
            self.reconnect()
            self.execMpc(cmd)
                
        return ret

    def reconnect(self):
        time.sleep(0.1)
        logging.info('Reconnection ... {0}'.format(self.connect()))

    # Connect to MPD
    def connect(self):
        connection = False
        logging.info('MPD Connection …')
        retry = 2
        while retry > 0:
            mpdCli = MPDClient()    # Create the MPD client
            try:               
                mpdCli.timeout = 10 
                mpdCli.idletimeout = None
                mpdCli.connect(self.config.getMpdHost(), self.config.getMpdPort())

                connection = True
                retry = 0
            except:
                time.sleep(0.5)
                # Wait for interrupt in the case of a shutdown
#                 if retry < 2:
#                     logging.warning('LCD service restart')
#                     self.execCommand("service mpd restart")
#                 else:
#                     logging.warning('LCD service start')
#                     self.execCommand("service mpd start")
#                 time.sleep(2)    # Give MPD time to restart
                retry -= 1

        if connection:
            self.mpd = mpdCli
        else:
            self.mpd = None
        logging.info(connection)
        return connection        
    
    def getStatus(self, prop=None):
        self.check()
        if prop is None:
            return self.execMpc(self.mpd.status())
        else:
            return self.execMpc(self.mpd.status()[prop])
    
    def getCurrentSong(self, prop=None):
        self.check()

        if prop is None:
            return self.execMpc(self.mpd.currentsong())
        else:
            return self.execMpc(self.mpd.currentsong()[prop])
        
    def pause(self):
        self.check()
        self.execMpc(self.mpd.pause())
    
    def setVolume(self, volume):
        self.check()
        self.execMpc(self.mpd.setvol(volume))
    
    def play(self, plid):
        self.check()
        self.execMpc(self.mpd.play(plid))
        
    def playid(self, plid):
        self.check()
        self.execMpc(self.mpd.playid(plid))        
    
    def stop(self):
        self.check()
        self.execMpc(self.mpd.stop())
    