#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 janv. 2015

@author: julien
'''
# Dependencies:
# sudo apt-get install -y python3-gobject (python3-gi)
# sudo apt-get install -y python3-smbus

import datetime
import logging
import threading
from controlers.controler_base import Controler

#import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib

SERVICE_NAME = "org.bluez"
AGENT_IFACE = SERVICE_NAME + '.Agent1'
ADAPTER_IFACE = SERVICE_NAME + ".Adapter1"
DEVICE_IFACE = SERVICE_NAME + ".Device1"
PLAYER_IFACE = SERVICE_NAME + '.MediaPlayer1'
TRANSPORT_IFACE = SERVICE_NAME + '.MediaTransport1'


class BluetoothDisplay(Controler, dbus.service.Object):

    continueDisplay = True

    AGENT_PATH = "/blueplayer/agent"
    CAPABILITY = "DisplayOnly"

    bus = None
    adapter = None
    device = None
    deviceAlias = None
    player = None
    transport = None
    connected = None
    state = None
    status = None
    discoverable = None
    track = None
    
    def __init__(self, config, lcd, mpdService, rootControler):
        logging.debug('BluetoothDisplay..__init__')
        Controler.__init__(self, config, lcd, mpdService, rootControler)

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        """Initialize gobject and find any current media players"""
        self.bus = dbus.SystemBus()

        dbus.service.Object.__init__(self, dbus.SystemBus(), self.AGENT_PATH)

        self.bus.add_signal_receiver(self.playerHandler,
                bus_name="org.bluez",
                dbus_interface="org.freedesktop.DBus.Properties",
                signal_name="PropertiesChanged",
                path_keyword="path")

        self.registerAgent()

        adapter_path = self.findAdapter().object_path
        self.bus.add_signal_receiver(self.adapterHandler,
                bus_name = "org.bluez",
                path = adapter_path,
                dbus_interface = "org.freedesktop.DBus.Properties",
                signal_name = "PropertiesChanged",
                path_keyword = "path")

        self.findPlayer()
        self.refresh()

        threading.Timer(0.1, self.start, []).start()
        
        
    def start(self):
        GLib.threads_init()
        loop = GLib.MainLoop()
        try:
            loop.run()
        except Exception as e:
            loop.quit()
            print (e)
            self.stop()
        
#     def volumeClickUp(self):
#         logging.debug('BluetoothDisplay..pauseRestart')
#         self.mpdService.pauseRestart()

    def findPlayer(self):
        """Find any current media players and associated device"""
        manager = dbus.Interface(self.bus.get_object("org.bluez", "/"), "org.freedesktop.DBus.ObjectManager")
        objects = manager.GetManagedObjects()

        player_path = None
        transport_path = None
        for path, interfaces in objects.items():
            if PLAYER_IFACE in interfaces:
                player_path = path
            if TRANSPORT_IFACE in interfaces:
                transport_path = path

        if player_path:
            logging.debug("Found player on path [{}]".format(player_path))
            self.connected = True
            self.getPlayer(player_path)
            player_properties = self.player.GetAll(PLAYER_IFACE, dbus_interface="org.freedesktop.DBus.Properties")
            if "Status" in player_properties:
                self.status = player_properties["Status"]
            if "Track" in player_properties:
                self.track = player_properties["Track"]
        else:
            logging.debug("Could not find player")

        if transport_path:
            logging.debug("Found transport on path [{}]".format(player_path))
            self.transport = self.bus.get_object("org.bluez", transport_path)
            logging.debug("Transport [{}] has been set".format(transport_path))
            transport_properties = self.transport.GetAll(TRANSPORT_IFACE, dbus_interface="org.freedesktop.DBus.Properties")
            if "State" in transport_properties:
                self.state = transport_properties["State"]


    def getPlayer(self, path):
        """Get a media player from a dbus path, and the associated device"""
        self.player = self.bus.get_object("org.bluez", path)
        logging.debug("Player [{}] has been set".format(path))
        device_path = self.player.Get("org.bluez.MediaPlayer1", "Device", dbus_interface="org.freedesktop.DBus.Properties")
        self.getDevice(device_path)

    def getDevice(self, path):
        """Get a device from a dbus path"""
        self.device = self.bus.get_object("org.bluez", path)
        self.deviceAlias = self.device.Get(DEVICE_IFACE, "Alias", dbus_interface="org.freedesktop.DBus.Properties")
        
    def registerAgent(self):
        """Register BluePlayer as the default agent"""
        manager = dbus.Interface(self.bus.get_object(SERVICE_NAME, "/org/bluez"), "org.bluez.AgentManager1")
        manager.RegisterAgent(self.AGENT_PATH, self.CAPABILITY)
        manager.RequestDefaultAgent(self.AGENT_PATH)
        logging.debug("Blueplayer is registered as a default agent")

    def findAdapter(self):
        objects = self.getManagedObjects();
        bus = dbus.SystemBus()
        for path, ifaces in objects.items():
            adapter = ifaces.get(ADAPTER_IFACE)
            if adapter is None:
                continue
            obj = bus.get_object(SERVICE_NAME, path)
            return dbus.Interface(obj, ADAPTER_IFACE)
        raise Exception("Bluetooth adapter not found")


    """Utility functions from bluezutils.py"""
    def getManagedObjects(self):
        bus = dbus.SystemBus()
        manager = dbus.Interface(bus.get_object("org.bluez", "/"), "org.freedesktop.DBus.ObjectManager")
        return manager.GetManagedObjects()

# SUITE ???
    def adapterHandler(self, interface, changed, invalidated, path):
        """Handle relevant property change signals"""
        if "Discoverable" in changed:
            logging.debug("Adapter discoverable is [{}]".format(self.discoverable))
            self.discoverable = changed["Discoverable"]
            self.refresh()
                
    def playerHandler(self, interface, changed, invalidated, path):
        """Handle relevant property change signals"""
        logging.debug("Interface [{}] changed [{}] on path [{}]".format(interface, changed, path))
        iface = interface[interface.rfind(".") + 1:]

        if iface == "Device1":
            if "Connected" in changed:
                self.connected = changed["Connected"]
        if iface == "MediaControl1":
            if "Connected" in changed:
                self.connected = changed["Connected"]
                if changed["Connected"]:
                    logging.debug("MediaControl is connected [{}] and interface [{}]".format(path, iface))
                    self.findPlayer()
        elif iface == "MediaTransport1":
            if "State" in changed:
                logging.debug("State has changed to [{}]".format(changed["State"]))
                self.state = (changed["State"])
            if "Connected" in changed:
                self.connected = changed["Connected"]
        elif iface == "MediaPlayer1":
            if "Track" in changed:
                logging.debug("Track has changed to [{}]".format(changed["Track"]))
                self.track = changed["Track"]
            if "Status" in changed:
                logging.debug("Status has changed to [{}]".format(changed["Status"]))
                self.status = (changed["Status"])

        self.refresh()

    def refresh(self):
        if not self.continueDisplay:
            return

        logging.debug("Updating display for connected: [{}]; state: [{}]; status: [{}]; discoverable [{}]".format(self.connected, self.state, self.status, self.discoverable))

        lines = []
        self.l2 = " "
        self.l3 = " "
        self.l4 = " "
        if self.discoverable:
            self.l3 = "Waiting to pair"
            self.l4 = "with device"
        else:
            if self.connected:
                if self.status == "paused":
                    self.l3 = "En pause"
                else:
                    """Display track info """
                    artist = self.track["Artist"]
                    album = self.track["Album"]
                    title = self.track["Title"]

                    trackNumber = self.track["TrackNumber"]
                    numberOfTracks = self.track["NumberOfTracks"]

                    #Unused
                    #genre = self.track["Genre"]
                    duration = self.formatDuration(self.track["Duration"])
                    print ("Duration : {0}".format(duration))

                    if artist.strip() != "":
                        lines.append(artist)
                    if album.strip() != "":
                        lines.append(album)
                    if title.strip() != "":
                        lines.append(title)
                    if trackNumber > 0 and numberOfTracks > 0:
                        lines.append("{0} / {1} : {2}".format(trackNumber, numberOfTracks, duration))
                    lines.append("Durée : {0}".format(duration))
                  
        if len(lines) >= 3:
            self.l2 = lines[0]
            self.l3 = lines[1]
            self.l4 = lines[2]
        if len(lines) == 2:
            self.l3 = lines[0]
            self.l4 = lines[1]
        if len(lines) == 1:
            self.l3 = lines[0]
        
        self.lcd.setLine2(self.l2, 'center')
        self.lcd.setLine3(self.l3, 'center')
        self.lcd.setLine4(self.l4, 'center')
        

    def formatDuration(self, millis):
        d = datetime.timedelta(milliseconds=millis)
        
        hours, remainder = divmod(d.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{0}h{1}m{2}s".format(hours, minutes, seconds)
             
    def stop(self):
        self.continueDisplay = False