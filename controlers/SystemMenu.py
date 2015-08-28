#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''
from menucontroler_base import MenuControler


class SystemMenu(MenuControler):

    '''
    classdocs
    '''
    defaultOptions = None

    def __init__(self, config, lcd, mpdService, rootControler, previousControler):

        self.defaultOptions = [("Reboot", self.reboot, None),
                   ("Shutdown", self.shutdown, None)]
        MenuControler.__init__(self, config, lcd, mpdService, 
                               rootControler, previousControler, 
                               self.defaultOptions)

    def reboot(self):
        self.execCommand("reboot")

    def shutdown(self):
        self.execCommand("halt")

    def stop(self):
        pass
