#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''

import os

from menucontroler_base import MenuControler
from RadioDisplay import RadioDisplay

Mpc = "/usr/bin/mpc"    # Music Player Client

class RadioControler(MenuControler):
    '''
    classdocs
    '''
    playlist = []
    
    def __init__(self, config, lcd, mpd, rootControler):
        self.loadStations(mpd, config.getPlaylistsDir())

        MenuControler.__init__(self, config, lcd, mpd, rootControler, self.playlist)

    def choixRadio(self, numRadio):
        self.execMpc(self.mpd.play(numRadio))
        self.rootControler.setControler(RadioDisplay(self.playlist[numRadio][0], self.config, self.lcd, self.mpd, self.rootControler, self))
        
    # Load radio stations
    def loadStations(self, mpd, playlistsDir):
        self.execMpc(mpd.clear())

        dirList = os.listdir(playlistsDir)
        for fname in dirList:
            #cmd = "load \"" + fname.strip("\n") + "\""

            fname = fname.strip("\n")
            try:
                self.execMpc(mpd.load(fname))
            except:
                print "Failed to load playlist " + fname

        self.execMpc(mpd.random(0))
        self.execMpc(mpd.consume(0))
        self.execMpc(mpd.repeat(0))

        self.createPlayList()
        self.execMpc(mpd.play(0))
        return
    
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
            #line = translate.escape(line)
            self.playlist.append((line,self.choixRadio,num))
            num = num + 1 
    