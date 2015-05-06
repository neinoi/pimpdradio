#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''

import logging
import threading
import urllib2

from menucontroler_base import MenuControler
from RadioDisplay import RadioDisplay
from mpd import MPDClient

Mpc = "/usr/bin/mpc"    # Music Player Client


class RadioControler(MenuControler):

    '''
    classdocs
    '''
    playlist = []

    def __init__(self, config, lcd, mpdService, rootControler, previousControler):
        # Test si une radio est en cours de lecture …
        radioEncours = False
        mpdFile = ''
        try:
            mpdFile = rootControler.startupSong['file']
            if mpdFile[:7] == 'http://' or mpdFile[:8] == 'https://':
                radioEncours = True
        except Exception as e:
            logging.warning('init error : {0}'.format(str(e)))

        logging.debug('Radio en cours : {0} : {1}'.format(radioEncours, mpdFile))

        mpd = MPDClient()    # Create the MPD client
        mpd.connect(config.getMpdHost(), config.getMpdPort())
        
        lastPos = self.loadRadiolist(mpd, config.getRadiolistFile(), mpdFile)

        logging.debug('lastpos : {0}'.format(lastPos))
        
        MenuControler.__init__(
            self, config, lcd, mpdService, rootControler, previousControler, self.playlist)

        if radioEncours and lastPos > 0:
            threading.Timer(0.1, self.choixRadio, [lastPos]).start()
        
    def loadRadiolist(self, mpd, radioListFile, lastRadio):
        logging.debug('RadioControler..loadRadiolist')
        
        addid = ('addid' in mpd.commands())

        mpd.clear()
        self.playlist = []
        num = 0
        lastPos = -1

        with open(radioListFile) as myfile:
            for line in myfile:
                line = line.strip()
                if line[:1] != '#' and line != '':
                    name, url = line.partition("=")[::2]
                    logging.debug('load : [{0}] {1}'.format(name.strip(), url.strip()))

                    self.playlist.append((name.strip(), self.choixRadio, num))

                    if url.strip().endswith('.m3u'):
                        #playlist
                        #Chargement de toutes les urls …

                        for s in self.extractUrls(url):
                            if s.strip() == lastRadio.strip():
                                lastPos = num

                            logging.debug('loading <{0}>'.format(s))
                            lastid = mpd.addid(s.strip(), num)
                            if addid:
                                mpd.addtagid(lastid, "title", name.strip())
                            num += 1
                    else:
                        if url.strip() == lastRadio.strip():
                            lastPos = num
                        lastid = mpd.addid(url.strip(), num)
                        logging.debug("lastid : {0} => {1}".format(lastid, name.strip()))
                        if addid:
                            mpd.addtagid(lastid, "title", name.strip())
                        num += 1


        mpd.random(0)
        mpd.consume(0)
        mpd.repeat(0)

        return lastPos
    
    def extractUrls(self, m3u):
        response = urllib2.urlopen(m3u)
        html = response.read()

        resp = []

        prec = ''
        for url in html.splitlines(True):
            if url.startswith('http') and prec != url:
                logging.debug('line : {0}'.format(url))
                resp.append(url)
                prec = url

        return resp
    
    def choixRadio(self, numRadio):
        logging.debug('numRadio : {0}'.format(numRadio))
        try:
            self.mpdService.play(numRadio)
            self.rootControler.setControler(
                RadioDisplay(self.playlist[numRadio][0], self.config, self.lcd,
                             self.mpdService, self.rootControler, self))
        except Exception as e:
            logging.error(str(e))

    def stop(self):
        pass
