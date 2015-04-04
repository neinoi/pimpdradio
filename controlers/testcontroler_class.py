#!/usr/bin/env python
#
# Raspberry Pi Main Controler class
#
# Copyright Julien Bellion 2014 (https://github.com/neinoi)
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are
# implied or given.
# The authors shall not be liable for any loss or damage however caused.
#

import os
from pimpdradio.encoders.encoder_class import Encoder
from controler_base import Controler

from pimpdradio.utils.translate_class import Translate

translate = Translate()

class MainControler(Controler):

    disp = None
    playlist = None

    def __init__(self, lcd, mpd):
        Controler.__init__(self, lcd, mpd)

        self.lcd.setLine1(" **** Bonjour ****  ")
        self.lcd.setLine2(" ****  Hello  ****  ")
        self.lcd.setLine3(" MPD : " + self.mpd.mpd_version)

        self.loadStations()

        return

    # This is the callback routine to handle tuner events
    def tuner_event(self, event):
        self.display_event("Tuner", event)
        return

    # This is the callback routine to handle volume events
    def volume_event(self, event):
        self.display_event("Volume", event)
        return

    def display_event(self, name, event):
        if event == Encoder.CLOCKWISE:
            message = name + " clockwise (" + str(Encoder.CLOCKWISE) + ")"
        elif event == Encoder.ANTICLOCKWISE:
            message = name + " anticlockwise (" + str(Encoder.BUTTONDOWN) + ")"
        elif event == Encoder.BUTTONDOWN:
            message = name + " button down (" + str(Encoder.BUTTONDOWN) + ")"
        elif event == Encoder.BUTTONUP:
            message = name + " button up (" + str(Encoder.BUTTONUP) + ")"

        self.lcd.setLine4(message)

        return

    # Load radio stations
    def loadStations(self):
        self.execMpc(self.mpd.clear())

        dirList = os.listdir("/var/lib/mpd/playlists")
        for fname in dirList:
            #cmd = "load \"" + fname.strip("\n") + "\""

            fname = fname.strip("\n")
            try:
                self.execMpc(self.mpd.load(fname))
            except:
                print "Failed to load playlist " + fname

        self.execMpc(self.mpd.random(0))
        self.execMpc(self.mpd.consume(0))
        self.execMpc(self.mpd.repeat(0))

        self.playlist = self.createPlayList()
        self.execMpc(self.mpd.play(0))
        return

    # Create list of tracks or stations
    def createPlayList(self):
        plist = []
        line = ""
        cmd = "playlist"
        p = os.popen(self.mpc + " " + cmd)
        while True:
            line = p.readline().strip('\n')
            if line.__len__() < 1:
                break
            line = translate.escape(line)
            plist.append(line)
        self.playlist = plist
        return self.playlist

# End of MainControler class
