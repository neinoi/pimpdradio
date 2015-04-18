#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''

import threading

from controler_base import Controler

class RadioDisplay(Controler):

    timerRefresh = None
    timerContinue = True
    
    def __init__(self, nomRadio, config, lcd, mpd, rootControler, previousControler):
        Controler.__init__(self, config, lcd, mpd, rootControler, previousControler)
        self.lcd.setLine2(nomRadio,'center')
        self.lcd.setLine3('','center')
        self.lcd.setLine4('','center')

        self.timerRefresh = threading.Timer(1, self._refresh, [1])
        self.timerRefresh.start()
        
        
    def tunerClickDown(self):
        pass
    
    def tunerClickUp(self):
        self.timerContinue = False
        try:
            self.timerRefresh.cancel()
        except:
            pass
        self.rootControler.setControler(self.previousControler)
    
    def refresh(self):
        try:
            curT = self.mpd.currentsong()['title']

            spl = curT.split(' - ', 1)
            self.lcd.setLine3(spl[0],'center')
        
            if len(spl) > 1:
                self.lcd.setLine4(spl[1],'center')
        except:
            pass

    def _refresh(self,tempo = 1):
        if self.timerContinue:
            self.refresh()
            
            self.timerRefresh = threading.Timer(tempo, self._refresh, [tempo])
            self.timerRefresh.start()
