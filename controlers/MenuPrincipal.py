#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''
import logging
import time

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

    def __init__(self, config, lcd, mpdService, rootControler):

        # Tableau de tuples (id,ligne à afficher,fonction à lancer)
        options = [("Radio", self.choix, CHOIX_RADIO),
                   ("Music", self.choix, CHOIX_MUSIC),
                   ("System", self.choix, CHOIX_SYSTEM)]

        MenuControler.__init__(self, config, lcd, mpdService, rootControler, options)

    def choix(self, choix):
        if choix == CHOIX_RADIO:
            self.rootControler.setControler(
                RadioControler(self.config, self.lcd, self.mpdService,
                               self.rootControler))
        elif choix == CHOIX_MUSIC:
            print "TODO"
        elif choix == CHOIX_SYSTEM:
            self.rootControler.setControler(
                SystemMenu(self.config, self.lcd, self.mpdService,
                           self.rootControler))

    def testStatus(self, retry=True):
        logging.debug('startupSong : {0}'.format(self.rootControler.startupSong))
        try:
            mpdFile = self.rootControler.startupSong['file']
            logging.debug('mpdFile : {0}'.format(mpdFile))
            if mpdFile[:7] == 'http://' or mpdFile[:8] == 'https://':
                self.choix(CHOIX_RADIO)
            else:
                self.choix(CHOIX_MUSIC)

        except Exception as e:
            logging.warning('testStatus error : {0}'.format(str(e)))
            if retry:
                time.sleep(1)
                self.testStatus(False)
            else:
                self.rootControler.setControler(self)
            
        
    def stop(self):
        pass
    
    def volumeClickUp(self):
        pass
