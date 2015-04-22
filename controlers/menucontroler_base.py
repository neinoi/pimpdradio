#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 1 janv. 2015

@author: julien
'''
from controler_base import Controler


class MenuControler(Controler):

    '''
    classdocs
    '''
    selected = -1

    # Tableau de tuples (ligne à afficher,fonction à lancer,paramètres)
    options = []

    def __init__(self, config, lcd, mpd, rootControler, options):
        Controler.__init__(self, config, lcd, mpd, rootControler)

        self.options = options
        self.current = 0

        self.lcd.clear()
        self._affOptions()

        return

    def _affOptions(self):
        first = self.current - 1
        if first + 3 > len(self.options):
            first -= 1
        if first < 0:
            first = 0

        pos = first
        if pos == self.current:
            self.lcd.setLine2('=> ' + self.options[pos][0])
        else:
            self.lcd.setLine2(self.options[pos][0])

        pos = pos + 1
        if pos < len(self.options):
            if pos == self.current:
                self.lcd.setLine3('=> ' + self.options[pos][0])
            else:
                self.lcd.setLine3(self.options[pos][0])

            pos = pos + 1
            if pos < len(self.options):
                if pos == self.current:
                    self.lcd.setLine4('=> ' + self.options[pos][0])
                else:
                    self.lcd.setLine4(self.options[pos][0])
            else:
                self.lcd.setLine4('')

        else:
            self.lcd.setLine3('')
            self.lcd.setLine4('')

    def tunerUp(self):
        self.current = self.current + 1
        if self.current >= len(self.options):
            self.current = self.current - 1

        self._affOptions()

    def tunerDown(self):
        self.current = self.current - 1
        if self.current < 0:
            self.current = 0

        self._affOptions()

    def tunerClickDown(self):
        pass

    def tunerClickUp(self):
        self.options[self.current][1](self.options[self.current][2])

    def volumeClickUp(self):
        if self.previousControler is not None:
            self.rootControler.setControler(self.previousControler)

    def refresh(self):
        # self.lcd.clear()
        self._affOptions()
