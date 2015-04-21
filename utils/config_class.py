'''
Created on 6 janv. 2015

@author: julien
'''

import ConfigParser


class Config(object):

    '''
    classdocs
    '''

    config = ConfigParser.ConfigParser()

    def __init__(self, configFile):
        self.config.read(configFile)

    def getSwitchMenuUp(self):
        return self.config.getint("SWITCHS", "MENU_UP")

    def getSwitchMenuDown(self):
        return self.config.getint("SWITCHS", "MENU_DOWN")

    def getSwitchMenuButton(self):
        return self.config.getint("SWITCHS", "MENU_BUTTON")

    def getSwitchVolumeUp(self):
        return self.config.getint("SWITCHS", "VOLUME_UP")

    def getSwitchVolumeDown(self):
        return self.config.getint("SWITCHS", "VOLUME_DOWN")

    def getSwitchVolumeButton(self):
        return self.config.getint("SWITCHS", "VOLUME_BUTTON")

    def getBoardRevision(self):
        return self.config.getint("BOARD", "REVISION")

    def getMpdHost(self):
        return self.config.get("MPD", "HOST")

    def getMpdPort(self):
        return self.config.getint("MPD", "PORT")

    # def getMpcCommand(self):
    #    return self.config.getstring("MPD","MPC_COMMAND")

    def getMaxVolume(self):
        return self.config.getint("MPD", "MAX_VOLUME")

    def getLcdWidth(self):
        return self.config.getint("LCD", "WIDTH")

    def getPlaylistsDir(self):
        return self.config.get("FILES", "PLAYLISTS")
