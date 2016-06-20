#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''

import threading

from controlers.menucontroler_base import MenuControler
from controlers.Display import Display

class MusicControler(MenuControler):

    '''
    classdocs
    '''
    playlist = []
    defaultOptions = None
    root = True

    def __init__(self, config, lcd, mpdService, rootControler, previousControler):
        
        self.defaultOptions = [("Genres", self.loadList, 'Genre'),
                               ("Artists", self.loadList, 'ArtistSort')]
        MenuControler.__init__(self, config, lcd, mpdService, 
                               rootControler, previousControler, 
                               self.defaultOptions)
        
        threading.Timer(0.1, self.displayLaunch, []).start()

    def displayLaunch(self):
        #On lit par défaut le premier morceau de la liste
        self.mpdService.play(0)
        self.rootControler.setControler(
            Display('LECTURE !!!', self.config, self.lcd, 
                    self.mpdService, self.rootControler, self))

    def changeOptions(self, options):
        self.root = False
        self.setOptions(options)

    def loadList(self, tag):
        options = []
        for g in self.mpdService.getList(tag):
            options.append((g, self.loadAlbums, ('album',tag,g)))
            
        self.changeOptions(options)
    
    def loadAlbums(self,search):
        options = []
        for a in self.mpdService.getList(*search):
            options.append((a, self.loadAlbum, a))
            
        self.changeOptions(options)
    
    def loadAlbum(self,albumName):
        options = []
        for a in self.mpdService.loadAlbum(albumName):
            options.append((a['track'] + ' ' + a['title'], self.playTitle, a['file']))
            
        self.changeOptions(options)
    
    def playTitle(self, title):
        self.mpdService.playFile(title)
    
    def volumeUp(self):
        if self.root:
            MenuControler.volumeUp()
        else:
            self.root = True
            self.changeOptions(self.defaultOptions)
            
    def stop(self):
        pass
                
