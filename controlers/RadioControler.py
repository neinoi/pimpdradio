#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''

import os
import logging
import threading

from menucontroler_base import MenuControler
from RadioDisplay import RadioDisplay
from mpd import MPDClient

Mpc = "/usr/bin/mpc"    # Music Player Client


class RadioControler(MenuControler):

    '''
    classdocs
    '''
    playlist = []

    def __init__(self, config, lcd, mpdService, rootControler):
        # Test si une radio est en cours de lecture …
        radioEncours = False
        mpdFile = ''
        try:
            mpdFile = rootControler.startupSong['file']
            if mpdFile[:7] == 'http://' or mpdFile[:8] == 'https://':
                radioEncours = True
        except Exception as e:
            logging.warning('init error : {0}'.format(str(e)))

        mpd = MPDClient()    # Create the MPD client
        mpd.connect(config.getMpdHost(), config.getMpdPort())

        self.loadStations(mpd, config.getPlaylistsDir())
        self.createPlayList(mpdService)

        logging.debug('4')
        MenuControler.__init__(
            self, config, lcd, mpdService, rootControler, self.playlist)

        logging.debug('5')

        if radioEncours and len(mpd.playlistfind('file', mpdFile)) > 0:
            lastPos = int(mpd.playlistfind('file', mpdFile)[0]['pos'])
            threading.Timer(0.1, self.choixRadio, [lastPos]).start()
        logging.debug('6')

    def choixRadio(self, numRadio):
        logging.debug('numRadio : {0}'.format(numRadio))
        try:
            logging.debug('avant mpdService.play')
            self.mpdService.play(numRadio)
            logging.debug('avant changement de controler')
            self.rootControler.setControler(
                RadioDisplay(self.playlist[numRadio][0], self.config, self.lcd,
                             self.mpdService, self.rootControler, self))
        except Exception as e:
            logging.error(str(e))
        

    # Load radio stations
    def loadStations(self, mpd, playlistsDir):
        logging.debug('RadioControler..loadStations')
        mpd.clear()

        dirList = os.listdir(playlistsDir)
        for fname in dirList:
            # cmd = "load \"" + fname.strip("\n") + "\""

            fname = fname.strip("\n")
            try:
                mpd.load(fname)
            except:
                logging.error('Failed to load playlist {0}/{1}'.format(playlistsDir, fname))

        mpd.random(0)
        mpd.consume(0)
        mpd.repeat(0)

    # Create list of tracks or stations
    def createPlayList(self, mpdService):
        logging.debug('RadioControler..createPlayList')
        self.playlist = []
        num = 0
        line = ""
        pls = mpdService.getPlaylistInfo()
        for st in pls:
            line = ''
            try:
                line = st['name']
            except:
                line = st['title']
            if line.__len__() < 1:
                break
            # line = translate.escape(line)
            self.playlist.append((line, self.choixRadio, num))
            num = num + 1

    def stop(self):
        pass
