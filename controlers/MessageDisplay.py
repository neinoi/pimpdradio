#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''

import logging

ROTATING_DISPLAY = "... ... ... ... ... ..."

class MessageDisplay():

    def __init__(self, l2, l3, l4, lcd):
        logging.debug('Display..__init__')
        
        lcd.setLine2(l2, 'center')
        lcd.setLine3(l3, 'center')
        lcd.setLine4(l4, 'center')

    def refresh(self):
        pass
    
    def stop(self):        
        pass
