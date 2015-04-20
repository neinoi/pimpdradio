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
    
    radioName = ''
    radioTitle = ''
    
    def __init__(self, nomRadio, config, lcd, mpd, rootControler, previousControler):
        Controler.__init__(self, config, lcd, mpd, rootControler, previousControler)
        self.lcd.setLine2(nomRadio,'center')
        self.radioName = self.mpd.currentsong()['name']
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
            curN = self.mpd.currentsong()['name']
            if curN != self.radioName:
                self.radioName = curN
                
                self.lcd.setLine2(curN[:20])
        except:
            pass    

        try:
            curT = self.mpd.currentsong()['title']
            if curT != self.radioTitle:
                self.radioTitle = curT
                spl = curT.split(' - ', 1)
                self.lcd.setLine3(spl[0],'center')
            
                if len(spl) > 1:
                    self.lcd.setLine4(spl[1],'center')
                else:
                    self.lcd.setLine4('')
        except:
            pass    

    def _refresh(self,tempo = 1):
        if self.timerContinue:
            self.refresh()
            
            self.timerRefresh = threading.Timer(tempo, self._refresh, [tempo])
            self.timerRefresh.start()
