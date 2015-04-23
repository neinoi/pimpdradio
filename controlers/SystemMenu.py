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

    def __init__(self, config, lcd, rootControler):

        # Tableau de tuples (id,ligne à afficher,fonction à lancer)
        options = [("Reboot", self.reboot, None),
                   ("Shutdown", self.shutdown, None)]

        MenuControler.__init__(self, config, lcd, rootControler, options)

    def reboot(self):
        self.execCommand("sudo reboot")

    def shutdown(self):
        self.execCommand("sudo halt")

    def stop(self):
        pass
