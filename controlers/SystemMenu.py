#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''
from controlers.menucontroler_base import MenuControler
from controlers.MessageDisplay import MessageDisplay,ROTATING_DISPLAY

class SystemMenu(MenuControler):

    '''
    classdocs
    '''
    defaultOptions = None

    def __init__(self, config, lcd, mpdService, rootControler, previousControler):

        self.defaultOptions = [("Redémarrer", self.reboot, None),
                   ("Arrêter", self.shutdown, None)]
        MenuControler.__init__(self, config, lcd, mpdService, 
                               rootControler, previousControler, 
                               self.defaultOptions)

    def reboot(self, param):
        self.rootControler.setControler(MessageDisplay("", "Redémarrage en cours", ROTATING_DISPLAY, self.lcd))
        self.execCommand(self.config.getShutdownCommand())
        self.execCommand("reboot")

    def shutdown(self, param):
        self.rootControler.setControler(MessageDisplay("", "Redémarrage en cours", ROTATING_DISPLAY, self.lcd))
        self.execCommand(self.config.getShutdownCommand())
        self.execCommand("halt")

    def stop(self):
        pass
