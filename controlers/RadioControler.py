#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''

import os
import time

from menucontroler_base import MenuControler
from RadioDisplay import RadioDisplay

Mpc = "/usr/bin/mpc"    # Music Player Client


class RadioControler(MenuControler):

    '''
    classdocs
    '''
    playlist = []

    def __init__(self, config, lcd, mpd, rootControler):

        # Test si une radio est en cours de lecture …
        radioEncours = False
        mpdFile = ''
        try:
            mpdFile = rootControler.startupSong['file']
            if mpdFile[:7] == 'http://' or mpdFile[:8] == 'https://':
                radioEncours = True
        except:
            pass

        self.loadStations(mpd, config.getPlaylistsDir())
        self.createPlayList()

        MenuControler.__init__(
            self, config, lcd, mpd, rootControler, self.playlist)

        if radioEncours and len(mpd.playlistfind('file', mpdFile)) > 0:
            lastPos = int(mpd.playlistfind('file', mpdFile)[0]['pos'])
            self.choixRadio(lastPos)

    def choixRadio(self, numRadio):
        self.mpd.play(numRadio)
        self.rootControler.setControler(
            RadioDisplay(self.playlist[numRadio][0], self.config, self.lcd,
                         self.mpd, self.rootControler, self))

    # Load radio stations
    def loadStations(self, mpd, playlistsDir):
        self.execMpc(mpd.clear())

        dirList = os.listdir(playlistsDir)
        for fname in dirList:
            # cmd = "load \"" + fname.strip("\n") + "\""

            fname = fname.strip("\n")
            try:
                self.execMpc(mpd.load(fname))
            except:
                print "Failed to load playlist " + fname

        self.execMpc(mpd.random(0))
        self.execMpc(mpd.consume(0))
        self.execMpc(mpd.repeat(0))

    # Create list of tracks or stations
    def createPlayList(self):
        self.playlist = []
        num = 0
        line = ""
        cmd = "playlist"
        p = os.popen(Mpc + " " + cmd)
        while True:
            line = p.readline().strip('\n')
            if line.__len__() < 1:
                break
            # line = translate.escape(line)
            self.playlist.append((line, self.choixRadio, num))
            num = num + 1
