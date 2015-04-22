#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 31 déc. 2014

@author: julien
'''

MODE_MENU = 0
MODE_RADIO = 1
MODE_MUSIC = 2


class ScreenBase(object):

    '''
    classdocs
    '''
    mode = MODE_MENU
    mpd = None

    def __init__(self, mpd):
        '''
        Constructor
        '''
        self.mpd = mpd

    def setMode(self, mode):
        self.mode = mode

    def setMenu(self, options, current):
        self.menu_options = options
        self.menu_current = current
        self.mode = MODE_MENU

    def refreshDisplay(self):
        raise NotImplementedError('refreshDisplay => TO BE IMPLEMENTED')
