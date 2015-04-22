'''
Created on 22 avr. 2015

@author: julien
'''

import logging
import time
from mpd import MPDClient

class MPDControler:
    '''
    classdocs
    '''

    mpd = None
    config = None

    def __init__(self, config, mpd):
        '''
        Constructor
        '''
        self.config = config
        self.mpd = mpd
        
    # Execute MPC command using mpd library - Connect client if required
    def execMpc(self, cmd):
        try:
            ret = cmd
        except:
            logging.warning('MPD reconnection')
            if self.connect():
                try:
                    ret = cmd
                except Exception as e:
                    logging.error('MPD error on #{0} : {1}'.format(cmd,str(e)))
            else:
                logging.error('MPD reconnection failed')
        return ret

    # Connect to MPD
    def connect(self):
        connection = False
        retry = 2
        while retry > 0:
            self.mpd = MPDClient()    # Create the MPD client
            try:                
                self.mpd.timeout = 10
                self.mpd.idletimeout = None
                self.mpd.connect(self.config.getMpdHost(), self.config.getMpdPort())

                connection = True
                retry = 0
            except:
                time.sleep(0.5)
                # Wait for interrupt in the case of a shutdown
                if retry < 2:
                    logging.warning('LCD service restart')
                    self.execCommand("service mpd restart")
                else:
                    logging.warning('LCD service start')
                    self.execCommand("service mpd start")
                time.sleep(2)    # Give MPD time to restart
                retry -= 1

        return connection        