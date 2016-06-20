#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''

import logging
import threading
import requests

from controlers.menucontroler_base import MenuControler
from controlers.Display import Display

from mpd import MPDClient

Mpc = "/usr/bin/mpc"    # Music Player Client

class RadioControler(MenuControler):

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

        if radioEncours and lastPos >= 0:
            logging.info('Radio en cours, position : {0}'.format(lastPos))
            threading.Timer(0.1, self.choixRadio, [lastPos]).start()
        
    def loadRadiolist(self, mpd, radioListFile, lastRadio):
        logging.debug('lastRadio : {0}'.format(lastRadio))
        
        addid = ('addid' in mpd.commands())

        mpd.clear()
        self.playlist = []
        num = 0
        lastPos = -1

        try:
            with open(radioListFile) as myfile:
                for line in myfile:
                    line = line.strip()
                    if line[:1] != '#' and line != '':
                        name, url = line.partition("=")[::2]
                        logging.debug('load : [{0}] {1}'.format(name.strip(), url.strip()))
    
                        self.playlist.append((name.strip(), self.choixRadio, num))
    
                        logging.debug("… playlist updated …")
    
                        if url.strip().endswith('.m3u'):
                            #playlist
                            #Chargement de toutes les urls …
                            logging.debug("… m3u …")
    
                            try:
                                for s in self.extractUrls(url):
                                    logging.debug('url : {0}'.format(s.strip()))
                                    if s.strip() == lastRadio.strip():
                                        logging.debug('*** TROUVEE !!! ***')
                                        lastPos = num
        
                                    lastid = mpd.addid(s.strip(), num)
                                    if addid:
                                        mpd.addtagid(lastid, "title", name.strip())
                                    num += 1
                            except Exception as e:
                                logging.error(e)
                        else:
                            logging.debug('url : {0}'.format(url.strip()))
                            if url.strip() == lastRadio.strip():
                                logging.debug('*** TROUVEE !!! ***')
                                lastPos = num
                            lastid = mpd.addid(url.strip(), num)
                            if addid:
                                mpd.addtagid(lastid, "title", name.strip())
                            num += 1
        except Exception as e:
            logging.warning('init error : {0}'.format(e))

        mpd.random(0)
        mpd.consume(0)
        mpd.repeat(0)

        return lastPos
    
    def extractUrls(self, m3u):

        r = requests.get(m3u.strip())
        html = r.text

        logging.debug("http : {0}".format(html))
        resp = []

        prec = ''
        for url in html.splitlines():
            logging.debug('line : {0}'.format(url))
            if url.startswith("http") and prec != url:
                logging.debug('line : {0}'.format(url))
                resp.append(url)
                prec = url

        return resp    
    
    def choixRadio(self, numRadio):
        logging.debug('numRadio : {0}'.format(numRadio))
        try:
            self.mpdService.play(numRadio)
            self.rootControler.setControler(
                Display(self.playlist[numRadio][0], self.config, self.lcd,
                             self.mpdService, self.rootControler, self))
        except Exception as e:
            logging.error(str(e))

    def stop(self):
        pass
