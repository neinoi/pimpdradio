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

    def __init__(self, config):
        '''
        Constructor
        '''
        self.config = config
        
        self.connect()

        
    # Execute MPC command using mpd library - Connect client if required
    def execMpc(self, cmd):
        #print 'execMpc - 1 - mpd : {0}'.format(self.mpd)
        
        if self.mpd is None:
            self.connect()
        
        #print 'execMpc - 2 - mpd : {0}'.format(self.mpd)
        
        try:
            ret = cmd
            #print 'execMpc - 3 - ret : {0}'.format(ret)
            
        except:
            #print 'execMpc - 4 - mpd : {0}'.format(self.mpd)
            self.reconnect()
            #print 'execMpc - 5 - mpd : {0}'.format(self.mpd)
            self.execMpc(cmd)
                
        #print 'execMpc - 6 - ret : {0}'.format(ret)

        return ret

    def reconnect(self):
        time.sleep(0.5)
        logging.info('Reconnection ... {0}'.format(self.connect()))

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
#                 if retry < 2:
#                     logging.warning('LCD service restart')
#                     self.execCommand("service mpd restart")
#                 else:
#                     logging.warning('LCD service start')
#                     self.execCommand("service mpd start")
#                 time.sleep(2)    # Give MPD time to restart
                retry -= 1

        return connection        
    
    def stop(self):
        logging.warning("MPD stop")
        self.mpd.close()
        self.mpd.disconnect()
    