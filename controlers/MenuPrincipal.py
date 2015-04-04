#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''
from menucontroler_base import MenuControler
from RadioControler import RadioControler
from SystemMenu import SystemMenu

CHOIX_RADIO = 1
CHOIX_MUSIC = 2
CHOIX_SYSTEM = 3

class MenuPrincipal(MenuControler):
    '''
    classdocs
    '''
    
    def __init__(self, config, lcd, mpd, rootControler):
        
        #Tableau de tuples (id,ligne à afficher,fonction à lancer)
        options = [("Radio",self.choix,CHOIX_RADIO),
                   ("Music",self.choix,CHOIX_MUSIC),
                   ("System",self.choix,CHOIX_SYSTEM)]
        
        MenuControler.__init__(self, config, lcd, mpd, rootControler, options)

    def choix(self, choix):
        if choix == CHOIX_RADIO:
            self.rootControler.setControler(RadioControler(self.config, self.lcd, self.mpd, self.rootControler))
        elif choix == CHOIX_MUSIC:
            print "TODO"
        elif choix == CHOIX_SYSTEM:
            self.rootControler.setControler(SystemMenu(self.config, self.lcd, self.mpd, self.rootControler))
    