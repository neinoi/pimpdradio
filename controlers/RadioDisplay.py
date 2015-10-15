#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''

import logging
from controlers.controler_base import Controler
from utils.constants import MPD_EVENT_PLAYER

class RadioDisplay(Controler):

    continueDisplay = True

    radioFile = ''
    l2 = ''
    l3 = ''
    l4 = ''
    radioTitle = ''
    radioName = ''

    def __init__(self, nomRadio, config, lcd, mpdService, rootControler, previousControler):
        logging.debug('RadioDisplay..__init__')
        Controler.__init__(self, config, lcd, mpdService, rootControler, previousControler)

        self.radioFile = self.mpdService.getCurrentSong()['file']
        self.radioName = nomRadio
        self.l2 = nomRadio

        mpdService.registerCallBackFor(MPD_EVENT_PLAYER, self.refresh)

    def tunerClickDown(self):
        logging.debug('RadioDisplay..tunerClickDown')

    def tunerClickUp(self):
        logging.debug('RadioDisplay..tunerClickUp')
        self.rootControler.setControler(self.previousControler)

    def volumeClickUp(self):
        logging.debug('RadioDisplay..pauseRestart')
        self.mpdService.pauseRestart()

    def refresh(self):
        if not self.continueDisplay:
            return 

        logging.debug('Début')
        
        try:
            if self.mpdService.getCurrentSong()['file'] != self.radioFile:
                self.radioFile = self.mpdService.getCurrentSong()['file']
                self.radioTitle = ''
                self.radioName = ''
                self.l2 = ''
                self.l3 = ''
                self.l4 = ''

            try:
                cname = self.mpdService.getCurrentSong()['name']
                if cname != 'unnamed':
                    self.l2 = cname
                else:
                    self.l2 = self.radioName
            except Exception as e:
                logging.info('RadioDisplay.refresh error : {0}'.format(str(e)))

            try:
                curT = self.mpdService.getCurrentSong()['title']
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
            
        logging.debug('Fin')
     
    def setReady(self, isReady):
        self.continueDisplay = isReady
        self.mpdService.registerCallBackFor(MPD_EVENT_PLAYER, self.refresh)        
        self.mpdService.run()
        self.refresh()
        
    def stop(self):        
        self.continueDisplay = False
