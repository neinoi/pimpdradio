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

    def __init__(self, config, lcd, mpdService, rootControler):
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
            self, config, lcd, mpdService, rootControler, self.playlist)

        if radioEncours and lastPos > 0:
            threading.Timer(0.1, self.choixRadio, [lastPos]).start()
        
    def loadRadiolist(self, mpd, radioListFile, lastRadio):
        logging.debug('RadioControler..loadRadiolist')

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
                    if url.strip() == lastRadio:
                        lastPos = num

                    if url.strip().endswith('.m3u'):
                        #playlist
                        #Chargement de toutes les urls …

                        for s in self.extractUrls(url):
                            logging.debug('loading <{0}>'.format(s))
                            mpd.addid(s.strip(), num)
                            num += 1
                    else:
                        lastid = mpd.addid(url.strip(), num)
                        logging.debug("lastid : {0} => {1}".format(lastid, name.strip()))
                        #mpd.addtagid(lastid, "title", name.strip())
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
                print 'line : {0}'.format(url)
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
        

#     # Load radio stations
#     def loadStations(self, mpd, playlistName):
#         logging.debug('RadioControler..loadStations')
#         mpd.clear()
# 
#         try:
#             mpd.load(playlistName)
#         except:
#             logging.error('Failed to load playlist {0}'.format(playlistName))
# 
#         mpd.random(0)
#         mpd.consume(0)
#         mpd.repeat(0)
# 
#     # Create list of tracks or stations
#     def createPlayList(self, mpdService):
#         logging.debug('RadioControler..createPlayList')
#         self.playlist = []
#         num = 0
#         line = ""
#         pls = mpdService.getPlaylistInfo()
#         for st in pls:
#             logging.debug('In : {0}'.format(st))
#             line = ''
#             try:
#                 line = st['name']
#             except:
#                 try :
#                     line = st['title']
#                 except:
#                     line = st['file']
#             if line.__len__() < 1:
#                 break
#             # line = translate.escape(line)
#             self.playlist.append((line, self.choixRadio, num))
#             num = num + 1
# 
#         logging.debug('Playlist => {0}'.format(self.playlist))

    def stop(self):
        pass
