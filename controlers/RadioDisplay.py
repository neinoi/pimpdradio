#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''

from controler_base import Controler

class RadioDisplay(Controler):

    def __init__(self, nomRadio, lcd, mpd, rootControler, previousControler):
        Controler.__init__(self, lcd, mpd, rootControler, previousControler)
        self.lcd.setLine2(nomRadio,'center')
        self.lcd.setLine3('')
        self.lcd.setLine4('')
        return
        
    def tunerClickDown(self):
        return
    
    def tunerClickUp(self):
        self.rootControler.setControler(self.previousControler)
        return
    
    def refresh(self):
        return