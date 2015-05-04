#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
'''
Created on 22 avr. 2015

@author: julien
'''

import logging
import time
import socket
import errno

from threading import Thread 

from mpd import MPDClient

class MPDService(Thread):
    '''
    classdocs
    '''

    config = None
    mpdCommands = None
    mpdListener = None
    
    eventsCallBacks = {}
    
    #noidle = False

    currentSong = None
    playlistInfo = None
    status = None
    plId = None
    Terminated = False

    def __init__(self, config):
        '''
        Constructor
        '''
        Thread.__init__(self)
        
        self.config = config
        
        self.mpdCommands = self.connect()
        self.mpdListener = self.connect()

        self.currentSong = self.mpdCommands.currentsong()
        self.playlistInfo = self.mpdCommands.playlistinfo()
        self.status = self.mpdCommands.status()
        
        logging.debug('init : currentSong : {0}'.format(self.currentSong))
        logging.debug('init : playlistInfo : {0}'.format(self.playlistInfo))
        logging.debug('init : status : {0}'.format(self.status))
            
    def run(self): 
        while not self.Terminated:
            self.waitForEvent()
            time.sleep(0.1)
        print "le thread " + self.nom + " s'est terminé proprement" 
    
    def stop(self): 
        self.Terminated = True        
        
    # Execute MPC command using mpd library - Connect client if required
    def execMpc(self, cmd, param = None):
        logging.debug('Command : {0}({1}'.format(cmd, param))
        
        retry = 2
        ret = None
        while retry > 0:
            retry -= 1
            try:
                if param is None:
                    ret = cmd()
                else:
                    ret = cmd(param)
            except socket.error, e:
                if isinstance(e.args, tuple):
                    logging.warning('errno is {0}'.format(e[0]))
                    if e[0] == errno.EPIPE:
                        # remote peer disconnected
                        logging.warning("Detected remote disconnect")
                    else:
                        # determine and handle different error
                        pass
                else:
                    print "socket error ", e
                time.sleep(0.5)
                self.reconnect()
                #ret = self.execMpc(cmd, param)
            except Exception as e:
                logging.error("Error : {0}".format(e))
                time.sleep(0.5)
                self.reconnect()
                #ret = self.execMpc(cmd, param)

        return ret


    def reconnect(self):
        logging.debug('-')
        if self.mpdCommands is not None:
            try:
                self.mpdCommands.close()
            except:
                pass

        self.mpdCommands = self.connect()

    # Connect to MPD
    def connect(self):
        logging.debug('-')
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
                mpdCli = None
                time.sleep(1)
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
            return mpdCli
        else:
            return None
                
    def getStatus(self, prop=None):
        logging.debug('-')
        if prop is None:
            return self.status
        else:
            return self.status[prop]
    
    def getCurrentSong(self, prop=None):
        logging.debug('-')
        if prop is None:
            return self.currentSong
        else:
            return self.currentSong[prop]
        
    def getPlaylistInfo(self):
        logging.debug('-')
        return self.playlistInfo

    def pauseRestart(self):
        logging.debug('-')
        
        if self.getStatus('state') == 'play':
            self.plId = int(self.getCurrentSong('id'))            
            self.execMpc(self.mpdCommands.pause)
        elif self.plId is not None:
            self.execMpc(self.mpdCommands.playid, self.plId)
            self.plId = None
        
    def changeVolume(self, increment):
        logging.debug('-')
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
        logging.debug('-')
        self.execMpc(self.mpdCommands.setvol, volume)

    def play(self, plid):
        logging.debug('-')

        self.execMpc(self.mpdCommands.play, plid)

        
    def playid(self, plid):
        logging.debug('playid({0})'.format(plid))

        self.execMpc(self.mpdCommands.playid, plid)        
    
    def stopPlayer(self):
        logging.debug('-')

        self.execMpc(self.mpdCommands.stop)

    
    def waitForEvent(self):
        #logging.debug('Noidle ? {0}'.format(self.noidle))

        #if not self.noidle:
        try:
            logging.debug('mpd.idle ...')
            events = self.mpdListener.idle()

            logging.debug('events : {0}'.format(events))
            if 'player' in events:
                self.currentSong = self.mpdListener.currentsong()
             
            if 'playlist'  in events:
                self.playlistInfo = self.mpdListener.playlistinfo()
                 
            #if 'mixer'  in events:
            self.status = self.mpdListener.status()
            
            for evt in events:
                if evt in self.eventsCallBacks:
                    callbacks = self.eventsCallBacks[evt]
                    if callbacks is not None :
                        for callback in callbacks:
                            callback()

        except Exception as e:
            logging.error(e)
            
    def registerCallBackFor(self, event, callback):
        logging.debug('-')
        cb = (callback,)
        if event in self.eventsCallBacks:
            cb = self.eventsCallBacks[event] + cb
        
        self.eventsCallBacks[event] = cb
    