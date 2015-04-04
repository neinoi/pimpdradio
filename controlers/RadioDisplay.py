#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''

from controler_base import Controler

class RadioDisplay(Controler):

    def __init__(self, nomRadio, config, lcd, mpd, rootControler, previousControler):
        Controler.__init__(self, config, lcd, mpd, rootControler, previousControler)
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
        curT = self.getCurrentTitle()

        spl = curT.split(' - ', 1)
        self.lcd.setLine3(spl[0],'center')
        
        if len(spl) > 1:
            self.lcd.setLine4(spl[1],'center')

        return