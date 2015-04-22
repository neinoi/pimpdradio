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

    radioFile = ''
    l2 = ''
    l3 = ''
    l4 = ''
    radioTitle = ''
    radioName = ''
    plId = None

    def __init__(self, nomRadio, config, lcd, mpd,
                 rootControler, previousControler):
        #print 'RadioDisplay..__init__'
        Controler.__init__(self, config, lcd, mpd,
                           rootControler, previousControler)

        self.radioName = nomRadio
        self.l2 = nomRadio

        self.timerRefresh = threading.Timer(1, self._refresh, [1])
        self.timerRefresh.start()

    def tunerClickDown(self):
        #print 'RadioDisplay..tunerClickDown'
        pass

    def tunerClickUp(self):
        #print 'RadioDisplay..tunerClickUp'
        self.rootControler.setControler(self.previousControler)

    def volumeClickUp(self):
        if self.plId is None:
            self.plId = int(self.mpd.currentsong()['id'])
            self.mpd.stop()
        else:
            self.mpd.playid(self.plId)
            self.plId = None
        self.lcd._refreshLine1()

    def refresh(self):
        #print 'RadioDisplay..refresh'

        try:
            curSong = self.mpd.currentsong()

            if curSong['file'] != self.radioFile:
                self.radioFile = curSong['file']
                self.radioTitle = ''
                self.radioName = ''
                self.l2 = ''
                self.l3 = ''
                self.l4 = ''

            try:
                self.l2 = curSong['name']
            except:
                pass

            try:
                curT = curSong['title']
                if curT != self.radioTitle:
                    self.radioTitle = curT
                    spl = curT.split(' - ', 1)
                    self.l3 = spl[0]

                    if len(spl) > 1:
                        self.l4 = spl[1]
                    else:
                        self.l4 = ''
            except:
                pass

        except:
            pass

        self.lcd.setLine2(self.l2, 'center')
        self.lcd.setLine3(self.l3, 'center')
        self.lcd.setLine4(self.l4, 'center')

    def _refresh(self, tempo=1):
        #print 'RadioDisplay.._refresh'
        if self.timerContinue:
            self.refresh()

            self.timerRefresh = threading.Timer(tempo, self._refresh, [tempo])
            self.timerRefresh.start()
            
    def stop(self):        
        self.timerContinue = False
        try:
            self.timerRefresh.cancel()
        except:
            pass
