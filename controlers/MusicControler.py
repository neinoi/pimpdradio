#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''

import logging

from menucontroler_base import MenuControler

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
        

    def changeOptions(self, options):
        self.root = False
        self.setOptions(options)

    def loadList(self, tag):
        options = []
        for g in self.mpdService.getList((tag)):
            options.append((g, self.loadAlbums, (tag,g)))
            
        self.changeOptions(options)
    
    def loadAlbums(self,search):
        options = []
        for a in self.mpdService.getList(search):
            options.append((a, self.loadAlbum, ('Album',a)+search))
            
        self.changeOptions(options)
    
    def loadAlbum(self,search):
        options = []
        for a in self.mpdService.loadAlbum(*search):
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
                
