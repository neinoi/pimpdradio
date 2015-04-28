#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
'''
Created on 22 avr. 2015

@author: julien
'''

import logging
import time

from threading import Thread 
import threading

from mpd import MPDClient

class MPDService(Thread):
    '''
    classdocs
    '''

    config = None
    mpd = None
    eventsCallBacks = {}
    
    noidle = False

    currentSong = None
    playlistInfo = None
    status = None

    Terminated = False

    def __init__(self, config):
        '''
        Constructor
        '''
        Thread.__init__(self)
        
        self.config = config
        
        self.connect()
        self.currentSong = self.mpd.currentsong()
        self.playlistInfo = self.mpd.playlistinfo()
        self.status = self.mpd.status()
        
        #logging.debug('init : currentSong : {0}'.format(self.currentSong))
        #logging.debug('init : playlistInfo : {0}'.format(self.playlistInfo))
        #logging.debug('init : status : {0}'.format(self.status))

            
    def run(self): 
        while not self.Terminated:
            self.waitForEvent()
            time.sleep(0.1)
        print "le thread " + self.nom + " s'est terminé proprement" 
    
    def stop(self): 
        self.Terminated = True        
        
    def _check(self):
        self.noidle = True
        self.mpd.noidle()
        
    def _restart(self):
        self.noidle = False
        threading.Timer(0.1, self.waitForEvent, []).start()
        
        
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
        mpdCli = None
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
        
        if prop is None:
            return self.status
        else:
            return self.status[prop]
    
    def getCurrentSong(self, prop=None):
        if prop is None:
            return self.currentSong
        else:
            return self.currentSong[prop]
        
    def getPlaylistInfo(self):
        return self.playlistInfo

    def pause(self):
        self._check()
        self.execMpc(self.mpd.pause())
        self._restart()
        
    def changeVolume(self, increment):
        volume = 0
        try:
            volume = int(self.status['volume'])
        except:
            logging.error('status->Volume error : {0}'.format(self.status))
        volume += increment
        
        if volume > self.config.getMaxVolume():
            volume = self.config.getMaxVolume()
        elif volume < 0:
            volume = 0

        logging.debug('Volume => {0}'.format(volume))
        self.setVolume(volume)
    
    def setVolume(self, volume):
        logging.debug('1')
        self._check()
        logging.debug('2')
        self.execMpc(self.mpd.setvol(volume))
        logging.debug('3')
        self._restart()
        logging.debug('4')

    def play(self, plid):
        logging.debug('1')
        self._check()
        logging.debug('2')
        self.execMpc(self.mpd.play(plid))
        logging.debug('3')
        self._restart()
        
    def playid(self, plid):
        self._check()
        self.execMpc(self.mpd.playid(plid))        
        self._restart()
    
    def stopPlayer(self):
        self._check()
        self.execMpc(self.mpd.stop())
        self._restart()
    
    def waitForEvent(self):
        logging.debug('Noidle ? {0}'.format(self.noidle))

        if not self.noidle:
            logging.debug('idle ...')
            try:
                events = self.mpd.idle()
    
                logging.debug('events : {0}'.format(events))
                
                if 'player' in events:
                    self.currentSong = self.mpd.currentsong()
                 
                if 'playlist'  in events:
                    self.playlistInfo = self.mpd.playlistinfo()
                     
                if 'mixer'  in events:
                    self.status = self.mpd.status()
                
                for evt in events:
                    if evt in self.eventsCallBacks:
                        callbacks = self.eventsCallBacks[evt]
                        if callbacks is not None :
                            for callback in callbacks:
                                callback()
            except Exception as e:
                logging.error(e)
            else:
                self.waitForEvent()
    
    def registerCallBackFor(self, event, callback):
        cb = (callback,)
        if event in self.eventsCallBacks:
            cb = self.eventsCallBacks[event] + cb
        
        self.eventsCallBacks[event] = cb
    