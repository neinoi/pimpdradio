#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''

import logging
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
        logging.debug('RadioDisplay..__init__')
        Controler.__init__(self, config, lcd, mpd,
                           rootControler, previousControler)

        self.radioName = nomRadio
        self.l2 = nomRadio

        self.timerRefresh = threading.Timer(1, self._refresh, [1])
        self.timerRefresh.start()

    def tunerClickDown(self):
        logging.debug('RadioDisplay..tunerClickDown')
        pass

    def tunerClickUp(self):
        logging.debug('RadioDisplay..tunerClickUp')
        self.rootControler.setControler(self.previousControler)

    def volumeClickUp(self):
        if self.plId is None:
            self.plId = int(self.execMpc(self.mpd.currentsong()['id']))
            self.execMpc(self.mpd.stop())
        else:
            self.execMpc(self.mpd.playid(self.plId))
            self.plId = None
        self.lcd._refreshLine1()

    def refresh(self):
        logging.debug('RadioDisplay..refresh')

        try:
            curSong = self.execMpc(self.mpd.currentsong())

            if curSong['file'] != self.radioFile:
                self.radioFile = curSong['file']
                self.radioTitle = ''
                self.radioName = ''
                self.l2 = ''
                self.l3 = ''
                self.l4 = ''

            try:
                self.l2 = curSong['name']
            except Exception as e:
                logging.info('RadioDisplay.refresh error : {0}'.format(str(e)))

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
            except Exception as e:
                logging.info('RadioDisplay.refresh error : {0}'.format(str(e)))

        except Exception as e:
            logging.warning('RadioDisplay.refresh error : {0}'.format(str(e)))

        self.lcd.setLine2(self.l2, 'center')
        self.lcd.setLine3(self.l3, 'center')
        self.lcd.setLine4(self.l4, 'center')

    def _refresh(self, tempo=1):
        logging.debug('RadioDisplay.._refresh')
        if self.timerContinue:
            self.refresh()

            self.timerRefresh = threading.Timer(tempo, self._refresh, [tempo])
            self.timerRefresh.start()
            
    def stop(self):        
        self.timerContinue = False
        try:
            self.timerRefresh.cancel()
        except :
            logging.debug('Inactive timer')
